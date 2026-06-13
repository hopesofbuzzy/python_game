from abc import abstractmethod

from pygame.event import Event as PygameEvent

from src.core.objects import *
from src.core.systems.entity_factory import EntityFactory
from src.core.systems.images import ImageLoader
from src.core.systems.level_builder import LevelBuilder


# FSM для сцен.
class Scene:
    """
    Класс для контейнеризации игрового мира в виде сцены.
    """

    def __init__(self, cursor):
        self.object_registry: dict[str, GameObject] = {}
        # Пул объектов для отложенного добавления.
        self._objects_to_add: dict[str, GameObject] = {}
        self._objects_to_delete: dict[str, GameObject] = {}
        # Счётчик реестра объектов.
        self.lastuid = 0
        # Реестр изображений для текущей сцены.
        self.il = ImageLoader()
        # Фабрика объектов.
        self.entity_factory: EntityFactory = EntityFactory(self, self.il, cursor)
        # Строитель уровней.
        self.level_builder: LevelBuilder = LevelBuilder(self, self.il, cursor)
        self.cursor = cursor
        # Все системы включены, запускаем сцену.
        self.ready()

    def add_object(self, obj: GameObject, obj_id: str | None = None) -> GameObject:
        if obj_id in self.object_registry:
            raise KeyError("Объект с таким obj_id уже существует")
        obj.uid = self.lastuid + 1
        self.lastuid += 1
        if obj_id is None:
            obj_id = f"{obj.uid}"
        self._objects_to_add[obj_id] = obj
        obj.model.free = lambda o=obj: self.remove_object(str(o.uid), 0)
        return obj

    def add_objects(self):
        """Добавляет все объекты в конце кадра на сцену."""
        for obj_id, obj in self._objects_to_add.items():
            self.object_registry[obj_id] = obj
        self._objects_to_add = dict()

    def remove_object(self, obj_id, object) -> None:
        if obj_id in self.object_registry:
            self._objects_to_delete[obj_id] = object

    def cleanup(self):
        for obj_id, obj in self._objects_to_delete.items():
            if obj_id in self.object_registry:
                self.object_registry.pop(obj_id)
                del obj
        self._objects_to_delete = dict()

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
