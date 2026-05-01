from src.core.objects.game_object import Controller, Model2D, View2D
from dataclasses import dataclass
from abc import abstractmethod

@dataclass
class GameObject:
    model: Model2D
    view: View2D
    controller: Controller

class Scene:
    """Класс для контейнеризации игрового мира в виде сцены."""
    def __init__(self, *args):
        self.object_registry: dict[str, GameObject] = {}

    def add_object(self, obj_id: str, obj: GameObject) -> GameObject:
        if obj_id in self.object_registry:
            raise KeyError("Объект с таким obj_id уже существует")
        self.object_registry[obj_id] = obj
        return obj

    def remove_object(self, obj_id: str) -> None:
        obj = self.object_registry.pop(obj_id)
        del obj