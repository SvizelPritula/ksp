from __future__ import annotations
from typing import Callable, Generator, Generic, Tuple, TypeVar


T = TypeVar('T')


class CellField(Generic[T]):
    def __init__(self, size: Tuple[int, int, int], initializer: Callable[[Tuple[int, int, int]], T]) -> None:
        self.__size = size
        self.__states = []

        for coords in self.keys():
            self.__states.append(initializer(coords))

    @property
    def size(self) -> Tuple[int, int, int]:
        return self.__size

    def __coords_to_index(self, coords: Tuple[int, int, int]) -> int:
        width, height, depth = self.__size
        x, y, z = coords

        x, y, z = x % width, y % height, z % depth

        return x * height * depth + y * depth + z

    def keys(self) -> Generator[Tuple[int, int, int], None, None]:
        width, height, depth = self.__size

        for x in range(width):
            for y in range(height):
                for z in range(depth):
                    yield x, y, z

    def __getitem__(self, coords: Tuple[int, int, int]) -> T:
        return self.__states[self.__coords_to_index(coords)]

    def __setitem__(self, coords: Tuple[int, int, int], state: T) -> None:
        self.__states[self.__coords_to_index(coords)] = state

    def tick(self, updater: Callable[[FieldHandle[T]], T]):
        new_states = []

        for coords in self.keys():
            result = updater(FieldHandle(self, coords))
            new_states.append(result)

        self.__states = new_states


class FieldHandle(Generic[T]):
    def __init__(self, field: CellField[T], coords: Tuple[int, int, int]) -> None:
        self.__field = field
        self.__coords = coords

    @property
    def coords(self) -> Tuple[int, int, int]:
        return self.__coords

    @property
    def field(self) -> CellField[T]:
        return self.__field

    def __offset_coords(self, coords: Tuple[int, int, int]):
        xa, ya, za = coords
        xb, yb, zb = self.__coords

        x, y, z = xa + xb, ya + yb, za + zb

        return x, y, z

    def __getitem__(self, coords: Tuple[int, int, int]) -> T:
        return self.__field[self.__offset_coords(coords)]

    @property
    def state(self) -> T:
        return self[0, 0, 0]


__all__ = ["CellField", "FieldHandle"]
