from src.core.objects.components.component_registry import ComponentRegistry
from src.core.objects.components.position import PositionComponent
from src.core.objects.game_object import GameObject

DEFAULT_SHOOTER_RANGE = 2
DEFAULT_SHOOTER_ATTACK = 3
DEFAULT_SHOOTER_COOLDOWN = 3.0
DEFAULT_SHOOTER_BULLET_SPEED = 150


@ComponentRegistry.register("targeting")
class TargetingComponent:
    def __init__(self, entity: GameObject, range, damage, cooldown, speed):
        self.position = entity.get(PositionComponent)
        self.range = range
        self.damage = damage
        self.cooldown = cooldown
        self.speed = speed
        self._timer: float = 0.0
        self.queue = list()

    def choose_target(self, targets: list[GameObject]):
        if targets:
            for target in targets:
                if target not in self.queue:
                    self.queue.append(target)
            if self.queue[0] not in targets:
                self.queue.pop(0)
        else:
            self.queue = list()

    def bind(self, build_context):
        self.create_bullet_func = build_context.create_bullet_func

    def update(self, delta_time):
        if self._timer < 0.0:
            if self.queue:
                target_pos = self.queue[0].get(PositionComponent).position
                direction = (target_pos - self.position.position).normalize()
                self.create_bullet_func(
                    direction, self.position.position, self.damage, self.speed
                )

                self._timer = self.cooldown
        else:
            self._timer -= delta_time
