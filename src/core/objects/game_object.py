from typing import Self, TypeVar

from pygame.event import Event as PygameEvent

from src.core.objects.event import Event

CT = TypeVar("CT")


class GameObject:
    """
    Игровая сущность, состоящая из компонентов (EntityComponent).

    Args:
        components (dict): компоненты сущности.
        children (list[GameObject]): дочерние игровые сущности.
        z_index (int): слой отрисовки (выше z_index -> выше слой отрисовки).
        tags (set[str]): теги объекта (для маски коллизий, прицеливания и др.)
    """

    def __init__(self):
        self.uid = -1
        self.on_destroy: Event = Event()
        # Открытые характеристики
        self.components = dict()
        self.children: list[GameObject] = list()
        self.z_index: int = 1
        self.tags: set[str] = set()

    def add(self, component) -> Self:
        """Добавляет компонент."""
        self.components[type(component)] = component
        return self

    def get(self, component_type: type[CT]) -> CT:
        """Возвращает компонент заданного типа."""
        return self.components[component_type]

    def has(self, *component_types) -> bool:
        """Проверяет наличие компонента заданного типа."""
        return all(ct in self.components for ct in component_types)

    def update(self, delta_time: float):
        """Обновление сущности."""
        for _, c in self.components.items():
            if hasattr(c, "update"):
                c.update(delta_time)

    def draw(self, screen, size, local_position, camera):
        """Отрисовка сущности."""
        for _, c in self.components.items():
            if hasattr(c, "draw"):
                c.draw(screen, size, local_position, camera)

    def handle_input(self, event: PygameEvent, cursor):
        """Обработка ввода сущности."""
        for _, c in self.components.items():
            if hasattr(c, "handle_input"):
                c.handle_input(event, cursor)

    def add_child(self, child: "GameObject"):
        """Добавляет дочернюю сущность (GameObject)"""
        self.children.append(child)

    def free(self):
        """Запрос на освобождение сущности из памяти."""
        for _, c in self.components.items():
            if hasattr(c, "free"):
                c.free()
        for child in self.children:
            child.free()
        self.on_destroy.emit(self)
