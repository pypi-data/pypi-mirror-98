from __future__ import annotations

from math import comb, sqrt
from typing import TYPE_CHECKING, Any, Iterable, Tuple, Type, Union

import jax.numpy as jnp
from jax.ops import index_update
from tjax import Array, Shape, field, field_names_values_metadata, fields

__all__ = ['parameter_names_values_support', 'parameter_names_support', 'Support', 'ScalarSupport',
           'VectorSupport', 'SymmetricMatrixSupport', 'SquareMatrixSupport']


class Support:
    def axes(self) -> int:
        raise NotImplementedError

    def num_elements(self, dimensions: int) -> int:
        raise NotImplementedError

    def shape(self, dimensions: int) -> Shape:
        raise NotImplementedError

    def flattened(self, x: Array) -> Array:
        raise NotImplementedError

    def unflattened(self, x: Array, dimensions: int) -> Array:
        shape = x.shape[:-1]
        return jnp.reshape(x, shape + self.shape(dimensions))


class ScalarSupport(Support):
    def axes(self) -> int:
        return 0

    def num_elements(self, dimensions: int) -> int:
        return 1

    def shape(self, dimensions: int) -> Shape:
        return ()

    def flattened(self, x: Array) -> Array:
        return jnp.reshape(x, (*x.shape, -1))


class VectorSupport(Support):
    def axes(self) -> int:
        return 1

    def num_elements(self, dimensions: int) -> int:
        return dimensions

    def shape(self, dimensions: int) -> Shape:
        return (dimensions,)

    def flattened(self, x: Array) -> Array:
        return jnp.reshape(x, (*x.shape[:-1], -1))


class SymmetricMatrixSupport(Support):
    def axes(self) -> int:
        return 2

    def num_elements(self, dimensions: int) -> int:
        return comb(dimensions + 1, 2)

    def shape(self, dimensions: int) -> Shape:
        return (dimensions, dimensions)

    def flattened(self, x: Array) -> Array:
        dimensions = x.shape[-1]
        assert x.shape[-2] == dimensions
        index = (..., *jnp.triu_indices(dimensions))
        return x[index]

    def unflattened(self, x: Array, dimensions: int) -> Array:
        k = x.shape[-1]
        sqrt_discriminant = sqrt(1 + 8 * k)
        i_sqrt_discriminant = int(sqrt_discriminant)
        if i_sqrt_discriminant != sqrt_discriminant:
            raise ValueError(f"{k} {sqrt_discriminant}")
        if i_sqrt_discriminant % 2 != 1:
            raise ValueError
        dimensions = (i_sqrt_discriminant - 1) // 2
        index = (..., *jnp.triu_indices(dimensions))
        symmetric = jnp.empty(x.shape[:-1] + (dimensions, dimensions))
        symmetric = index_update(symmetric, index, x)
        symmetric = index_update(symmetric.T, index, x)
        return symmetric


class SquareMatrixSupport(Support):
    def axes(self) -> int:
        return 2

    def num_elements(self, dimensions: int) -> int:
        return dimensions ** 2

    def shape(self, dimensions: int) -> Shape:
        return (dimensions, dimensions)

    def flattened(self, x: Array) -> Array:
        return jnp.reshape(x, (*x.shape[:-2], -1))


def distribution_parameter(support: Support) -> Any:
    return field(metadata={'support': support})


def parameter_names_values_support(x: Parametrization) -> Iterable[Tuple[str, Array, Support]]:
    for name, value, metadata in field_names_values_metadata(x, static=False):
        support = metadata['support']
        if not isinstance(support, Support):
            raise TypeError
        yield name, value, support


def parameter_names_support(x: Union[Type[Parametrization], Parametrization]) -> (
        Iterable[Tuple[str, Support]]):
    for this_field in fields(x, static=False):
        support = this_field.metadata['support']
        if not isinstance(support, Support):
            raise TypeError
        yield this_field.name, support


if TYPE_CHECKING:
    from .expectation_parametrization import Parametrization
