from src.core.objects import *
from src.core.systems.images import ImageLoader
from src.core.systems.entity_factory import EntityFactory

from abc import abstractmethod, ABC
from pygame.event import Event as PygameEvent


# FSM для сцен.
class Scene:
    """Класс для контейнеризации игрового мира в виде сцены."""
    def __init__(self, cursor):
        self.object_registry: dict[str, GameObject] = {}
        # Пул объектов для отложенного добавления.
        self._objects_to_add: dict[str, GameObject] = {}
        # Фабрики объектов.
        self.entity_factory: EntityFactory = EntityFactory(self)
        self.cursor = cursor
        self.last_uid = 0
        # Все системы включены, запускаем сцену.
        self.ready()

    def add_object(self, obj: GameObject, obj_id: str | None = None) -> GameObject:
        if obj_id in self.object_registry:
            raise KeyError("Объект с таким obj_id уже существует")
        obj._uid = self.last_uid + 1
        self.last_uid += 1
        if obj_id is None:
            obj_id = f"{obj._uid}"
        self._objects_to_add[obj_id] = obj
        obj.model.scene = self
        return obj

    def add_objects(self):
        """Добавляет все объекты в конце кадра на сцену."""
        for obj_id, obj in self._objects_to_add.items():
            self.object_registry[obj_id] = obj
        self._objects_to_add = dict()

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

    def update(self, delta_time: float):
        """
        Регулярно обновляет сцену.
        """
        for key, object in self.object_registry.items():
            object.model.update(delta_time)

    @abstractmethod
    def handle_input(self, event: PygameEvent):
        """Читает pygame.event"""
        ...