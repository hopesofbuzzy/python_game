from src.core.objects import Model, Controller
from src.objects import *

class Slot:
    """Слот инвентаря с растением для посадки."""
    def __init__(self, model, view):
        self.model = model
        self.view = view

class InventoryModel(Model):
    """Инвентарь для выбора растений."""
    def __init__(self):
        # Заглушки
        self.slots = {
            1: Slot(MushroomModel, MushroomView),
            2: Slot(SunflowerModel, SunflowerView)
        }
        self.size = 10

class InventoryController(Controller):
    ...