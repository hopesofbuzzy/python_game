from dataclasses import dataclass
from abc import abstractmethod

class Model2D:
    def __init__(self):
        self.position: Position = Position(0, 0)
        # Радианы.
        self.rotation: float = 0

@dataclass
class Position:
    x: float
    y: float

class View2D:
    def __init__(self):
        # Прослойка цвета.
        self.modulate: tuple[int, int, int] = (255, 255, 255)

    @abstractmethod
    def draw(self):
        ...

class Controller:
    def __init__(self, model: Model2D, view: View2D):
        self.model = model

    @abstractmethod
    def handle_input(self):
        ...