import logging
from pygame.math import Vector2

from src.core.objects.scene import Scene
from src.core.singletones.event_bus import EventFlow
from src.factories.bullet_factory import BulletFactory
from src.core.objects.components.ui import ClickHandlerComponent

from src.factories.ui_factory import UIFactory


BACKGROUND_MUSIC = "res/sfx/win_2.wav"
START_BUTTON_TEXT = "В меню"
START_BUTTON_FONT_SIZE = 30
START_BUTTON_COLOR = (150, 200, 150)
START_BUTTON_POSITION = Vector2(0, 500)
START_BUTTON_SIZE = Vector2(150, 60)
WIN_NAME = "Ферма спасена! <3"
WIN_NAME_POSITION = Vector2(0, 50)
WIN_NAME_FONT_SIZE = 50
WIN_NAME_LINESPACE = -10
STATS_TEXT_POSITION = WIN_NAME_POSITION + Vector2(0, 200)
STATS_TEXT_FONT_SIZE = 25
STATS_TEXT_LINESPACE = 5

class WinScene(Scene):
    def ready(self):
        self.setup_factories()
        self.setup_music()
        self.setup_ui()
        self.event_bus.subscribe("on_game_started", self.start_game)

    def setup_factories(self):
        """Настраивает мелкие фабрики."""
        self.ui_factory: UIFactory = UIFactory(self.add_object, self.event_bus)

    def setup_music(self):
        """Настраивает музыку."""
        self.audio_loader.load_music(BACKGROUND_MUSIC)
        self.audio_loader.play_music(1)


    def setup_ui(self):
        """Настраивает интерфейс."""
        self.ui_factory.create_text(
            WIN_NAME,
            WIN_NAME_POSITION,
            WIN_NAME_FONT_SIZE,
            linespace=WIN_NAME_LINESPACE
        )
        stats_text = (
            f"Пройдено волн: {self.global_data["waves"]}\n"
            f"Уничтожено монстров {self.global_data["enemies_destroyed"]}\n"
            f"Счёт солнышек в конце: {self.global_data["suns"]}\n"
        )
        self.ui_factory.create_text(
            stats_text,
            STATS_TEXT_POSITION,
            STATS_TEXT_FONT_SIZE,
            linespace=STATS_TEXT_LINESPACE
        )
        button = self.ui_factory.create_button(
            START_BUTTON_TEXT,
            START_BUTTON_FONT_SIZE,
            START_BUTTON_POSITION,
            START_BUTTON_SIZE,
            None,
            START_BUTTON_COLOR
        )
        button.get(ClickHandlerComponent).on_button_pressed.subscribe(self.start_game)

    def start_game(self, _event: EventFlow):
        from src.scenes.menu.menu import MenuScene
        self.change_scene(MenuScene)