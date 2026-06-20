import logging
from dataclasses import dataclass
from typing import Callable

from pygame.math import Vector2

from src.config.plants import (
    PLANT_DATA,
    PLANT_SIZE,
    PLANTS_LEVEL_UPS,
)
from src.core.objects import (
    ClickHandlerComponent,
    PositionComponent,
    SpriteComponent,
)
from src.core.objects.components.component_registry import ComponentRegistry
from src.scenes.main.objects import (
    BasePlant,
    DataComponent,
    UpgradeComponent,
)


@dataclass
class BuildContext:
    create_bullet_func: Callable
    death_func: Callable
    timeout_func: Callable
    damage_func: Callable


class PlantBuilder:
    """Строитель растений."""

    def __init__(
            self,
            add_object,
            create_bullet_func,
            give_sun_func,
            remove_plant_func,
            ui_factory
        ):
        self.add_object = add_object
        self.build_context = BuildContext(
            create_bullet_func,
            remove_plant_func,
            give_sun_func,
            damage_func=lambda x: 5
        )
        self.ui_factory = ui_factory
        self._plant = None

    def with_replace(self, tile_pos: tuple):
        self.build_context.death_func(tile_pos)
        return self

    def with_plant(self, plant_name: str, position: Vector2, tile_pos: tuple):
        if plant_name in PLANT_DATA:
            plant = self.create_plant(plant_name, position, tile_pos)
            self._plant = plant
            return self
        else:
            raise KeyError("Неизвестное растение!")

    def with_upgrade(self):
        if not self._plant:
            raise ValueError("Строителю нужно растение!")
        plant_name = self._plant.get(DataComponent).name
        upgrade = UpgradeComponent(
            self._plant,
            PLANTS_LEVEL_UPS[plant_name]["plant_name"],
            PLANTS_LEVEL_UPS[plant_name]["cost"]
        )
        self._plant.add(upgrade)
        return self

    def with_button(self):
        if not self._plant:
            raise ValueError("Строителю нужно растение!")
        click_handler = self.ui_factory.create_click_handler(
            Vector2(0, 0),
            PLANT_SIZE,
            self._plant
        )
        self._plant.add_child(click_handler)
        click_handler.get(ClickHandlerComponent).on_button_pressed.subscribe(
            self._plant.get(UpgradeComponent).request_upgrade_dialog
        )
        return self

    def build(self) -> BasePlant:
        if not self._plant:
            raise ValueError("Строителю нужно растение!")
        return self._plant

    def create_plant(self, plant_name: str, position: Vector2, tile_pos: tuple):
        # Характеристики
        image_path = PLANT_DATA[plant_name]["image_path"]
        # Обязательные компоненты
        position_comp = PositionComponent(position, None)
        # Иниациализация растения
        plant = (
            BasePlant(tile_pos)
            .add(position_comp)
            .add(SpriteComponent(image_path, PLANT_SIZE, True))
            .add(DataComponent(plant_name, tuple(tile_pos)))
        )
        # Выборочные компоненты.
        comp_registry = ComponentRegistry()
        for comp in PLANT_DATA[plant_name]["components"]:
            comp = comp.copy()
            comp_type = comp.pop("type")
            component = comp_registry.create(comp_type, plant, **comp)
            plant.add(component)
            component.bind(self.build_context)
        self.add_object(plant)
        plant.tags.add("plant")
        return plant