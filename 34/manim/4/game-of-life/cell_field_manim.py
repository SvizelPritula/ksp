from typing import Callable, Generator, Generic, Optional, Tuple, TypeVar
from manim import *
from cell_field import CellField, FieldHandle


def empty_visualizer(field: FieldHandle) -> Optional[VMobject]:
    return None


T = TypeVar('T')


class MCellField(VMobject, Generic[T]):
    def __init__(self, size: Tuple[int, int, int], initializer: Callable[[Tuple[int, int, int]], T], **kwargs):
        super().__init__(**kwargs)

        self.__field = CellField(size, initializer)
        self.__visualizer = empty_visualizer
        self.__objects: list[Optional[VMobject]] = []

        for coords in self.keys():
            obj = self.__get_object(coords)
            self.__objects.append(obj)

            if obj != None:
                self.add(obj)

    def __get_real_coordinates(self, coords: Tuple[int, int, int]):
        width, height, depth = self.__field.size
        x, y, z = coords

        return x % width, y % height, z % depth

    def __coords_to_index(self, coords: Tuple[int, int, int]) -> int:
        width, height, depth = self.__field.size
        x, y, z = self.__get_real_coordinates(coords)

        return x * height * depth + y * depth + z

    def __get_object(self, coords: Tuple[int, int, int]) -> None:
        obj = self.__visualizer(FieldHandle(self.__field, coords))
        if obj == None:
            return obj

        width, height, depth = self.__field.size
        x, y, z = self.__get_real_coordinates(coords)

        obj.shift(RIGHT * (x - width / 2 + 0.5))
        obj.shift(OUT * (y - height / 2 + 0.5))
        obj.shift(DOWN * (z - depth / 2 + 0.5))

        return obj

    def __update_object(self, coords: Tuple[int, int, int]) -> None:
        new_obj = self.__get_object(coords)
        old_obj = self.__objects[self.__coords_to_index(coords)]

        if old_obj != None:
            self.remove(old_obj)

        if new_obj != None:
            self.add(new_obj)

        self.__objects[self.__coords_to_index(coords)] = new_obj

    def __update_objects(self):
        for coords in self.keys():
            self.__update_object(coords)

    def set_visualizer(self, visualizer: Callable[[FieldHandle[T]], Optional[VMobject]]) -> None:
        self.__visualizer = visualizer
        self.__update_objects()

    def keys(self) -> Generator[Tuple[int, int, int], None, None]:
        return self.__field.keys()

    def __getitem__(self, coords: Tuple[int, int, int]) -> T:
        return self.__field[coords]

    def __setitem__(self, coords: Tuple[int, int, int], state: T) -> None:
        self.__field[coords] = state
        self.__update_object(coords)

    def tick(self, updater: Callable[[FieldHandle[T]], None]):
        self.__field.tick(updater)
        self.__update_objects()


__all__ = ["MCellField"]
