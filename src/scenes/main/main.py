import logging

from pygame.math import Vector2

from src.core.objects import (
    Event,
    Map,
    MapControllerComponent,
    MapModelComponent,
    TextRenderComponent,
)

# Составляющие сцены.
from src.core.objects.scene import Scene
from src.core.singletones.event_bus import EventFlow, event_bus
from src.core.singletones.image_loader import image_loader
from src.core.systems.input import cursor
from src.scenes.main.factories.bullet_factory import BulletFactory
from src.scenes.main.factories.dialog_builder import DialogBuilder

# Фабрики.
from src.scenes.main.factories.enemy_factory import EnemyFactory
from src.scenes.main.factories.inventory_factory import InventoryFactory
from src.scenes.main.factories.path_factory import PathFactory
from src.scenes.main.factories.plant_builder import PlantBuilder
from src.scenes.main.factories.ui_factory import UIFactory
from src.scenes.main.level.level_builder import Level, LevelBuilder
from src.scenes.main.objects import (
    BasePlant,
    Inventory,
    InventoryModelComponent,
    UpgradeComponent,
)
from src.scenes.main.objects.components.map_level_data import MapLevelDataComponent

# Константы
from src.scenes.main.objects.plants import (
    PLANTS,
    PLANTS_CLASSES,
    PLANTS_DESCRIPTIONS,
    PLANTS_PRICES,
)
from src.scenes.main.wave_manager import WaveManager

START_SUNS = 400
SUNS_TEXT_POSITION = Vector2(0, 0)
SUNS_TEXT_SIZE = 20
UPGRADE_DIALOG_SIZE = Vector2(300, 150)
UPGRADE_BUTTON_TEXT = "Улучшить"
UPGRADE_BUTTON_FONT_SIZE = 18


class MainScene(Scene):
    def ready(self):
        # Статистика уровня.
        self.suns: int = START_SUNS
        self.on_suns_update: Event = Event()
        self.upgrade_dialogs: list = list()
        # Загрузка уровня.
        self.setup_level()
        # Фабрики объектов.
        self.setup_factories()
        self.inventory: Inventory = self.inventory_factory.create_inventory()
        # Оркестратор волн и спавна врагов.
        self.setup_waves()
        event_bus.subscribe("on_requested_upgrade_dialog", self.open_upgrade_dialog)
        event_bus.subscribe("on_requested_upgrade", self.plant_upgrade)
        event_bus.subscribe("on_plant_level_uped", self.plant_level_up)
        self.build_interface()

    def setup_factories(self):
        self.bullet_factory: BulletFactory = BulletFactory(self.add_object,)
        self.inventory_factory: InventoryFactory = InventoryFactory(self.add_object)
        self.path_factory: PathFactory = PathFactory()
        self.ui_factory: UIFactory = UIFactory(self.add_object)
        self.enemy_factory: EnemyFactory = EnemyFactory(
            self.add_object,
            self.ui_factory
        )

    def setup_level(self):
        self.level_builder: LevelBuilder = LevelBuilder(
            self.add_object,
        )
        self.level: Level = self.level_builder.load_and_create_level(Vector2(0, 0), "2")
        self.gamemap: Map = self.level.map
        self.gamemap.get(MapControllerComponent).on_tile_click.subscribe(self.plant)

    def setup_waves(self):
        path = self.path_factory.create_path_component(
            self.level.path,
            self.gamemap.get(MapModelComponent).tile_to_pos_centred
        )
        self.wave_manager: WaveManager = WaveManager(
            self.level.parsed_waves,
            self.enemy_factory.create_enemy,
            path
        )
        self.wave_manager.on_enemy_reached_end.subscribe(self.game_over)

    def build_interface(self):
        self.suns_text = self.ui_factory.create_text(
            f"Солнышки: {self.suns}",
            SUNS_TEXT_POSITION,
            SUNS_TEXT_SIZE
        )
        self.on_suns_update.subscribe(
            lambda s: self.suns_text.get(TextRenderComponent).set_text(f"Солнышки: {s}")
        )

    def update(self, delta_time: float):
        self.wave_manager.update(delta_time)
        return super().update(delta_time)

    def plant(
            self,
            event: EventFlow,
            tile_pos: Vector2,
            global_pos_centred: Vector2,
            tile_type: int,
            global_pos: Vector2
        ):
        self.close_all_upgrade_dialogs()
        """Посадка растения."""
        plant_name = self.inventory.get(InventoryModelComponent).get_active_slot()
        map_level_data = self.gamemap.get(MapLevelDataComponent)
        # Условия посадки.
        if (
            plant_name
            and self.check_suns(plant_name)
            and map_level_data.is_position_free(tuple(tile_pos))
        ):
            if map_level_data.is_position_to_place_plant(plant_name, tuple(tile_pos)):
                self.decrease_suns(self.get_plant_price(plant_name))
                # Создание растения.
                plant = (
                    PlantBuilder(
                        self.add_object,
                        self.bullet_factory,
                        self.give_sun,
                        self.gamemap.get(MapLevelDataComponent).remove_plant,
                        self.ui_factory
                    )
                    .with_plant(
                        plant_name,
                        global_pos_centred,
                        tile_pos
                    )
                    .with_upgrade()
                    .with_button()
                    .build()
                )
                self.gamemap.get(MapLevelDataComponent).add_plant(
                    tuple(tile_pos)
                )
                event.stop()

    def plant_level_up(
            self,
            event: EventFlow,
            plant: BasePlant,
            target_plant_name
    ):
        """Трансформация растения после уровня улучшения."""
        self.close_all_upgrade_dialogs()
        global_pos_centred = (
            self.gamemap
            .get(MapModelComponent)
            .tile_to_pos_centred(Vector2(plant.tile_pos))
        )
        logging.debug(f"Начинаем улучшение {target_plant_name}")
        new_plant = (
            PlantBuilder(
                self.add_object,
                self.bullet_factory,
                self.give_sun,
                self.gamemap.get(MapLevelDataComponent).remove_plant,
                self.ui_factory
            )
            .with_replace(plant.tile_pos)
            .with_plant(
                target_plant_name,
                global_pos_centred,
                plant.tile_pos
            )
            .with_upgrade()
            .with_button()
            .build()
        )
        self.gamemap.get(MapLevelDataComponent).add_plant(
            tuple(new_plant.tile_pos)
        )
        self.gamemap.get(MapLevelDataComponent).remove_plant(
            plant.tile_pos
        )
        plant.free()
        self.open_upgrade_dialog(
            EventFlow(),
            new_plant,
            new_plant.get(UpgradeComponent).request_upgrade
        )

    def open_upgrade_dialog(
            self,
            event: EventFlow,
            plant: BasePlant,
            request_upgrade_func
    ):
        self.close_all_upgrade_dialogs()
        dialog = (
            DialogBuilder(
                self.add_object,
                self.ui_factory
            )
            .with_dialog(
                Vector2(0, 0),
                UPGRADE_DIALOG_SIZE,
                plant
            )
            .with_text(PLANTS_DESCRIPTIONS[PLANTS_CLASSES[type(plant)]], 18)
            .with_button(
                UPGRADE_BUTTON_TEXT,
                UPGRADE_BUTTON_FONT_SIZE,
                request_upgrade_func
            )
            .build()
        )
        self.upgrade_dialogs.append(dialog)

    def close_all_upgrade_dialogs(self):
        for dialog in self.upgrade_dialogs:
            dialog.free()
        self.upgrade_dialogs = list()

    def plant_upgrade(
            self,
            event: EventFlow,
            plant: BasePlant,
            price: int,
            upgrade_func
    ):
        """Одноразовое улучшение растения."""
        if self.suns >= price:
            logging.debug(f"Растение улучшено: {self.suns}")
            self.decrease_suns(price)
            upgrade_func()

    def check_suns(self, plant: str) -> bool:
        return self.suns >= PLANTS_PRICES[plant]

    def get_plant_price(self, plant: str) -> int:
        return PLANTS_PRICES[plant]

    def give_sun(self, suns: int):
        """Выдача солыншек."""
        self.suns += suns
        self.on_suns_update.emit(self.suns)

    def decrease_suns(self, suns: int):
        self.suns -= suns
        logging.debug(f"Минус солнышки: {self.suns}")
        self.on_suns_update.emit(self.suns)

    def game_over(self):
        """Проигрыш."""
        self.exit()