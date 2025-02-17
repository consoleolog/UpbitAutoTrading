import abc
import inspect
from typing import Any, TypeVar, Type

T = TypeVar('T')

class IOCContainer(abc.ABC):
    def __init__(self)->None:
        self.obj_map = {}

    def register(self, obj: Any)->None:
        self.obj_map[type(obj)] = obj

    def get(self, type_: Type[T]) -> T:
        impl_type = type_
        if inspect.isabstract(type_):
            impl_types = type_.__subclasses__()
            if len(impl_types) == 0:
                raise ValueError()

            impl_type = impl_types[0]
        try:
            obj = self.obj_map[impl_type]
        except KeyError:
            raise ValueError()

        return obj

    @abc.abstractmethod
    def compose(self)->None:
        pass

class Container(IOCContainer):
    def compose(self) ->None:
        # self.register()
        pass