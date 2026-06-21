import logging
from pygame.math import Vector2

from src.core.objects.scene import Scene
from src.core.singletones.event_bus import EventFlow
from src.factories.bullet_factory import BulletFactory
from src.core.objects.components.ui import ClickHandlerComponent

from src.factories.ui_factory import UIFactory

from src.scenes.main.main import MainScene

BACKGROUND_MUSIC = "res/music/background_2.mp3"
START_BUTTON_TEXT = "Начать игру"
START_BUTTON_FONT_SIZE = 30
START_BUTTON_COLOR = (150, 200, 150)
START_BUTTON_POSITION = Vector2(0, 300)
START_BUTTON_SIZE = Vector2(150, 60)
GAME_NAME = "Монстры, \nцветы \nи что-то ещё"
GAME_NAME_POSITION = Vector2(0, 50)
GAME_NAME_FONT_SIZE = 50
GAME_NAME_LINESPACE = -10

class MenuScene(Scene):
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
        self.audio_loader.play_music(-1)


    def setup_ui(self):
        """Настраивает интерфейс."""
        self.ui_factory.create_text(
            GAME_NAME,
            GAME_NAME_POSITION,
            GAME_NAME_FONT_SIZE,
            GAME_NAME_LINESPACE
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
        self.change_scene(MainScene)