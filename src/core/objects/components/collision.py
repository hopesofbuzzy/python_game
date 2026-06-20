from pygame.math import Vector2

from src.core.objects.event import Event
from src.core.objects.game_object import GameObject
from src.core.objects.components.component_registry import ComponentRegistry


# Хитбоксы
class CollisionShape:
    """Форма коллизии."""
    def __init__(self, position: Vector2):
        self._position = position


class CircleShape(CollisionShape):
    def __init__(self, position: Vector2, radius: float):
        self.radius = radius
        super().__init__(position)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

class RectShape(CollisionShape):
    def __init__(self, position: Vector2, size: Vector2, centred: bool):
        self.size = size
        self.centred = centred
        super().__init__(position)

    @property
    def position(self):
        if self.centred:
            return self._position - self.size // 2
        else:
            return self._position

    @position.setter
    def position(self, value):
        if self.centred:
            self._position = value + self.size // 2
        else:
            self._position = value

# Компоненты.
@ComponentRegistry.register("collision")
class CollisionComponent():
    def __init__(self, _entity, shape: CollisionShape, resolvable: bool = False):
        self.entity: GameObject = _entity
        self.shape = shape
        self.resolvable = resolvable

    def bind(self, build_context):
        ...

    def handle_collision(self, other: GameObject):
        for comp_cls, comp in self.entity.components.items():
            if hasattr(comp, "handle_collision") and comp_cls is not CollisionComponent:
                comp.handle_collision(other)
        # self.collision_func(other)

class MovementComponent():
    def __init__(self, velocity: Vector2, speed: float):
        self.velocity = velocity
        self.speed = speed

    def bind(self, build_context):
        ...

    def set_velocity(self, dx: float, dy: float):
        self.velocity = Vector2(dx, dy) * self.speed

    def stop(self):
        self.velocity = Vector2(0, 0)