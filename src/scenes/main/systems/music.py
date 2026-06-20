from src.core.singletones.audio_loader import AudioLoader
from src.core.singletones.event_bus import EventBus, EventFlow

BACKGROUND_MUSIC = "res/music/background_1.mp3"
BULLET_SPAWN_SFX = "res/sfx/bullet_spawn_1.mp3"
PLANT_SPAWN_SFX = "res/sfx/plant_spawn_1.wav"

class MusicManager:
    """Менеджер музыки и sfx на главной сцене."""
    def __init__(self, audio_loader: AudioLoader, event_bus: EventBus):
        self.audio_loader = audio_loader
        event_bus.subscribe("on_bullet_created", self.on_bullet_created)
        event_bus.subscribe("on_plant_created", self.on_plant_created)
        self.audio_loader.load_music(BACKGROUND_MUSIC)
        self.audio_loader.play_music(-1)

    def on_bullet_created(self, _event: EventFlow):
        self.audio_loader.load_sfx(BULLET_SPAWN_SFX).sound.play()

    def on_plant_created(self, _event: EventFlow):
        self.audio_loader.load_sfx(PLANT_SPAWN_SFX).sound.play()