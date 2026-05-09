from src.core.objects import *
from src.core.systems.uniform_grid import UniformGrid
from src.core.systems.images import ImageLoader

from abc import abstractmethod, ABC
from pygame.event import Event as PygameEvent


# FSM для сцен.
class Scene:
    """Класс для контейнеризации игрового мира в виде сцены."""
    def __init__(self):
        self.object_registry: dict[str, GameObject] = {}
        self.image_loader = ImageLoader()
        self.last_uid = 0
        self.input = input
        # Все системы включены, запускаем сцену.
        self.ready()

    def add_object(self, obj_id: str, obj: GameObject) -> GameObject:
        if obj_id in self.object_registry:
            raise KeyError("Объект с таким obj_id уже существует")
        obj._uid = self.last_uid + 1
        self.last_uid += 1
        self.object_registry[obj_id] = obj
        return obj

    def remove_object(self, obj_id: str) -> None:
        obj = self.object_registry.pop(obj_id)
        del obj

    def cleanup(self):
        for obj_id, obj in self.object_registry.items():
            if not obj._active:
                self.remove_object(obj_id)

    @abstractmethod
    def ready(self):
        """
            Инициализация сцены.
            
            Описание объектов сцены.
        """
        ...

    @abstractmethod
    def update(self, delta_time: float):
        """
        Регулярно обновляет сцену.
        """
        ...

    @abstractmethod
    def handle_input(self, event: PygameEvent):
        """Читает pygame.event"""
        ...