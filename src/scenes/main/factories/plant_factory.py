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


class PlantFactory:
    """Фабрика растений."""

    def __init__(
            self,
            add_object,
            bullet_factory,
            ui_factory,
            event_bus
        ):
        self.add_object = add_object
        self.build_context = BuildContext(
            create_bullet_func=bullet_factory.create_bullet,
            death_func=(lambda plant: event_bus.fire("on_plant_death", plant)),
            timeout_func=(lambda suns: event_bus.fire("on_given_sun", suns)),
            damage_func=(lambda x: 5)
        )
        self.ui_factory = ui_factory

    def _add_button(self, plant):
        """Создаёт кнопку растения.."""
        click_handler = self.ui_factory.create_click_handler(
            Vector2(0, 0),
            PLANT_SIZE,
            plant
        )
        click_handler.get(ClickHandlerComponent).on_button_pressed.subscribe(
            plant.get(UpgradeComponent).request_upgrade_dialog
        )
        plant.add_child(click_handler)
        return click_handler

    def create_plant(self, plant_name: str, position: Vector2, tile_pos: tuple):
        """Создаёт растение с выборочными компонентами."""
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
        plant.add(UpgradeComponent(
                plant,
                PLANTS_LEVEL_UPS[plant_name]["plant_name"],
                PLANTS_LEVEL_UPS[plant_name]["cost"]
            ))
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
        # Кнопка
        self._add_button(plant)
        return plant