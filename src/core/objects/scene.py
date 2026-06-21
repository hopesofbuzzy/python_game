from abc import abstractmethod

from pygame.event import Event as PygameEvent

from src.core.objects import *
from src.core.singletones.image_loader import ImageLoader


# FSM для сцен.
class Scene:
    """
    Класс для контейнеризации игрового мира в виде сцены.
    """

    def __init__(self, event_bus, audio_loader, global_data, exit):
        self.object_registry: dict[str, GameObject] = {}
        self.z_index_object_registry = list()
        # Пул объектов для отложенного добавления.
        self._objects_to_add: dict[str, GameObject] = {}
        self._objects_to_delete: dict[str, GameObject] = {}
        # Счётчик реестра объектов.
        self.lastuid = 0
        # Выход (Инъекция)
        self.exit = exit
        # Шина событий (инъекция)
        self.event_bus = event_bus
        self.audio_loader = audio_loader
        # Смена сцены и глобальные данные.
        self.on_scene_changed: Event = Event()
        self.global_data = global_data
        # Все системы включены, запускаем сцену.
        self.ready()

    def add_object(self, obj: GameObject, obj_id: str | None = None) -> GameObject:
        """Добавляет объект в очередь на добавление в сцену."""
        if obj_id in self.object_registry:
            raise KeyError("Объект с таким obj_id уже существует")
        obj.uid = self.lastuid + 1
        self.lastuid += 1
        if obj_id is None:
            obj_id = f"{obj.uid}"
        self._objects_to_add[obj_id] = obj
        obj.on_destroy.subscribe(lambda o=obj: self.remove_object(str(o.uid), o))
        return obj

    def add_objects(self):
        """Добавляет все объекты в конце кадра на сцену."""
        for obj_id, obj in self._objects_to_add.items():
            self.object_registry[obj_id] = obj
            self.z_index_object_registry.append(obj)
        self._objects_to_add = dict()
        self.z_index_object_registry = sorted(
             self.z_index_object_registry, key=lambda x: x.z_index
        )

    def remove_object(self, obj_id, object) -> None:
        """Добавляет объект в очередь на удаление со сцены."""
        if obj_id in self.object_registry:
            self._objects_to_delete[obj_id] = object

    def cleanup(self):
        """Очистка объектов из списка на удаление в конце кадра."""
        if len(self._objects_to_delete):
            logging.debug(f"objects_to_delete: len({self._objects_to_delete})")
        # Лучше перестроить список z_index за O(n)
        self.z_index_object_registry = [
            obj
            for obj in self.z_index_object_registry
            if obj not in self._objects_to_delete.values()
        ]
        for obj_id, obj in self._objects_to_delete.items():
            if obj_id in self.object_registry:
                self.object_registry.pop(obj_id)
                obj.components.clear()
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
            object.update(delta_time)

    @abstractmethod
    def handle_input(self, event: PygameEvent):
        """Читает pygame.event"""
        ...

    def change_scene(self, scene_class):
        """Запрашивает смену сцены на scene_class."""
        self.on_scene_changed.emit(scene_class)