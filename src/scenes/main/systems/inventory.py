from src.config.plants import get_plant_range
from src.core.singletones.event_bus import EventBus, EventFlow
from src.factories.cursor_circle_factory import CursorCircleFactory
from src.scenes.main.objects import Inventory
from src.scenes.main.objects.components.inventory import (
    InventoryModelComponent,
    Slot,
)

DEFAULT_CURSOR_CIRCLE_COLOR = (255, 50, 50, 96)


class InventoryManager:
    """Менеджер инвентаря и выбора растений для посадки."""

    def __init__(
        self,
        inventory: Inventory,
        cursor_circle_factory: CursorCircleFactory,
        tile_size: int,
        event_bus: EventBus,
    ):
        self.inventory = inventory
        # Круг радиуса для выбранного слота.
        self.cursor_circle_factory = cursor_circle_factory
        self.cursor_circle = None
        self.tile_size = tile_size
        event_bus.subscribe(
            "on_inventory_changed_slot", self.on_inventory_changed_slot
        )
        event_bus.subscribe(
            "on_inventory_zero_slot_set", self.on_inventory_zero_slot_set
        )

    def on_inventory_changed_slot(self, event: EventFlow, slot: Slot):
        """Смена слота инвентаря."""
        inventory_model = self.inventory.get(InventoryModelComponent)
        if inventory_model.get_active_slot():
            inventory_model.set_zero_slot()
            self.free_cursor_circle()
        else:
            inventory_model.set_active_slot(slot)
            self.free_cursor_circle()
            self.cursor_circle = (
                self.cursor_circle_factory.create_cursor_circle(
                    get_plant_range(slot.name) * self.tile_size,
                    DEFAULT_CURSOR_CIRCLE_COLOR,
                )
            )
        event.stop()

    def free_cursor_circle(self):
        """Очищение выделения радиуса."""
        if self.cursor_circle:
            self.cursor_circle.free()
        self.cursor_circle = None

    def on_inventory_zero_slot_set(self, event: EventFlow):
        """Установка нулевого слота в инвентаре."""
        self.inventory.get(InventoryModelComponent).set_zero_slot()
        self.free_cursor_circle()
