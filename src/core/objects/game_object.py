from abc import ABC
from typing import Optional, Self, Type, TypeVar

from pygame.event import Event as PygameEvent

from src.core.objects.event import Event

CT = TypeVar('CT')

class GameObject(ABC):
    def __init__(self):
        self.components = dict()
        self.uid = -1
        self.children: list[GameObject] = list()
        self.on_destroy: Event = Event()
        self.z_index: int = 1
        self.tags: set[str] = set()

    def add(self, component) -> Self:
        self.components[type(component)] = component
        return self

    def get(self, component_type: Type[CT]) -> CT:
        return self.components[component_type]

    def has(self, *component_types) -> bool:
        return all(ct in self.components for ct in component_types)

    def update(self, delta_time: float):
        for c_type, c in self.components.items():
            if hasattr(c, "update"):
                c.update(delta_time)

    def draw(self, screen, size, local_position, camera):
        for c_type, c in self.components.items():
            if hasattr(c, "draw"):
                c.draw(screen, size, local_position, camera)

    def handle_input(self, event: PygameEvent, cursor):
        for c_type, c in self.components.items():
            if hasattr(c, "handle_input"):
                c.handle_input(event, cursor)

    def add_child(self, child):
        self.children.append(child)

    def free(self):
        for c_type, c in self.components.items():
            if hasattr(c, "free"):
                c.free()
        for child in self.children:
            child.free()
        self.on_destroy.emit(self)