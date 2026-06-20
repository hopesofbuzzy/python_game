import logging

from src.core.singletones.event_bus import EventBus, EventFlow
from src.scenes.main.objects.components.inventory import Slot, InventoryModelComponent
from src.scenes.main.objects import Inventory

class InventoryManager:
    def __init__(
        self,
        inventory: Inventory,
        event_bus: EventBus
    ):
        self.inventory = inventory
        event_bus.subscribe(
            "on_inventory_changed_slot",
            self.on_inventory_changed_slot
        )

    def on_inventory_changed_slot(self, event: EventFlow, slot: Slot):
        logging.info(f"Система: {slot}")
        self.inventory.get(InventoryModelComponent).set_active_slot(slot)
        event.stop()