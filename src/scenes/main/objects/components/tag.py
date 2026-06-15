from src.core.objects.game_object import GameObject
from src.core.objects.event import Event


class TagContactComponent:
    """Проверка контакта с объектами с тегом."""
    def __init__(self, target_tag):
        self.target_tag = target_tag
        self.on_contact: Event = Event()

    def handle_collision(self, collision: GameObject):
        if self.target_tag in collision.tags:
            self.on_contact.emit(collision)