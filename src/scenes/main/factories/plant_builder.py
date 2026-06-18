import logging

from pygame.math import Vector2

from src.core.objects import (
    ClickHandlerComponent,
    CollisionComponent,
    PositionComponent,
    RectShape,
    SpriteComponent,
    TargetingComponent,
)
from src.scenes.main.objects import (
    BasePlant,
    BigMushroom,
    CycleTimerComponent,
    HealthComponent,
    LongMushroom,
    Mushroom,
    PlantDataComponent,
    Sunflower,
    UpgradeComponent,
)

from src.config.plants import PLANT_SIZE, PLANT_HITBOX_SIZE, PLANTS_LEVEL_UPS, PLANT_DATA



class PlantBuilder:
    """Строитель растений."""

    def __init__(
            self,
            add_object,
            bullet_factory,
            give_sun,
            remove_plant,
            ui_factory
        ):
        self.add_object = add_object
        self.give_sun = give_sun
        self.bullet_factory = bullet_factory
        self.remove_plant = remove_plant
        self.ui_factory = ui_factory
        self._plant = None

    def with_replace(self, tile_pos: tuple):
        self.remove_plant(tile_pos)
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
        plant_name = self._plant.get(PlantDataComponent).name
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
        targeting = PLANT_DATA[plant_name]["targeting"]
        image_path = PLANT_DATA[plant_name]["image_path"]
        # Компоненты
        position_comp = PositionComponent(position, None)
        # Иниациализация растения
        plant = (
            BasePlant(tile_pos)
            .add(position_comp)
            .add(SpriteComponent(image_path, PLANT_SIZE, True))
            .add(PlantDataComponent(plant_name, targeting))
        )
        if targeting:
            # Характеристики
            range = PLANT_DATA[plant_name]["range"]
            attack = PLANT_DATA[plant_name]["attack"]
            cooldown = PLANT_DATA[plant_name]["cooldown"]
            # Добавление остаточных компонентов
            targeting_comp = TargetingComponent(
                position_comp,
                range,
                attack,
                cooldown,
                PLANT_DATA[plant_name]["bullet_speed"]
            )
            plant.add(targeting_comp)
            targeting_comp.on_shoot.subscribe(self.bullet_factory.create_bullet)
        else:
            # Характеристики
            cooldown = PLANT_DATA[plant_name]["cooldown"]
            given_sun = PLANT_DATA[plant_name]["given_sun"]
            health = PLANT_DATA[plant_name]["health"]
            # Добавление остаточных компонентов
            timer_comp = CycleTimerComponent(cooldown, given_sun)
            health_comp = HealthComponent(health)
            collision_comp = CollisionComponent(
                RectShape(
                    Vector2(0, 0), PLANT_HITBOX_SIZE, True
                ),
                False
            )
            plant.add(collision_comp)
            plant.add(timer_comp)
            plant.add(health_comp)
            remove_plant_func = self.remove_plant
            health_comp.on_death.subscribe(
                lambda: remove_plant_func(plant.tile_pos)
            )
            health_comp.on_death.subscribe(lambda: plant.free())
            timer_comp.on_timeout.subscribe(self.give_sun)
        self.add_object(plant)
        plant.tags.add("plant")
        return plant