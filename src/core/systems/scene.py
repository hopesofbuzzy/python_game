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
        self._ready(*args)

    @abstractmethod
    def _ready(self, *args):
        ...
