from src.core.objects import GameObject, MovementComponent
from src.scenes.main.objects.components.health import HealthComponent

DEFAULT_ATTACK_COOLDOWN = 0.5


class AttackComponent:
    """Компонент атаки сущностей."""

    def __init__(self, entity, target_tag: str, attack: int, cooldown: float):
        self.entity = entity
        self.target_tag = target_tag
        self.attack = attack
        self.cooldown = cooldown
        self._attack_timer = 0.0
        self.in_attack: bool = False
        self.binded = False

    def bind(self, build_context):
        self.attack_func = build_context.attack_func
        self.binded = True

    def handle_collision(self, collision: GameObject):
        if self._attack_timer <= 0.0 and self.target_tag in collision.tags:
            collision.get(HealthComponent).damage(self.attack)
            self._attack_timer = self.cooldown
            self.in_attack = True
            if self.binded:
                self.attack_func(self.entity, collision)
            return True
        return False

    def update(self, delta_time):
        if self._attack_timer > 0.0:
            self.entity.get(MovementComponent).set_velocity(0, 0)
            self._attack_timer -= delta_time
        else:
            self.in_attack = False
