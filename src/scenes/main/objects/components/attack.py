import logging

from src.core.objects.game_object import GameObject
from src.core.objects.event import Event
from src.scenes.main.objects.components.health import HealthComponent

DEFAULT_ATTACK_COOLDOWN = 0.5

class AttackComponent:
    def __init__(
            self,
            movement,
            target_tag: str,
            attack: int,
            cooldown: float
        ):
        self.movement = movement
        self.target_tag = target_tag
        self.attack = attack
        self.cooldown = cooldown
        self._attack_timer = 0.0
        self.in_attack: bool = False
        self.on_attack: Event = Event()

    def handle_collision(self, collision: GameObject):
        if self._attack_timer <= 0.0:
            if self.target_tag in collision.tags:
                collision.get(HealthComponent).damage(self.attack)
                self._attack_timer = self.cooldown
                self.in_attack = True
                self.on_attack.emit()
                return True
        return False

    def update(self, delta_time):
        if self._attack_timer > 0.0:
            self.movement.set_velocity(0, 0)
            self._attack_timer -= delta_time
        else:
            self.in_attack = False