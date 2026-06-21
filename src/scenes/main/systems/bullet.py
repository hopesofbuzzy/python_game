from src.core.singletones.event_bus import EventBus, EventFlow
from src.scenes.main.objects.bullet import Bullet


class BulletController:
    def __init__(self, event_bus: EventBus):
        event_bus.subscribe("on_bullet_attacked", self.on_bullet_attacked)
        event_bus.subscribe("on_bullet_timeout", self.remove_bullet)

    def remove_bullet(self, _event: EventFlow, bullet: Bullet):
        bullet.free()

    def on_bullet_attacked(self, _event: EventFlow, bullet: Bullet, other):
        bullet.free()
