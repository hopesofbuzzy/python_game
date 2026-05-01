from src.core.objects.game_object import GameObject, Controller, Model, View
from src.core.systems.input import InputManager
from abc import abstractmethod
from pygame.event import Event as PygameEvent


# FSM для сцен.
class Scene:
    """Класс для контейнеризации игрового мира в виде сцены."""
    def __init__(self, input: InputManager):
        self.object_registry: dict[str, GameObject] = {}
        self.input = input
        self.ready()

    def add_object(self, obj_id: str, obj: GameObject) -> GameObject:
        if obj_id in self.object_registry:
            raise KeyError("Объект с таким obj_id уже существует")
        self.object_registry[obj_id] = obj
        return obj

    def remove_object(self, obj_id: str) -> None:
        obj = self.object_registry.pop(obj_id)
        del obj

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