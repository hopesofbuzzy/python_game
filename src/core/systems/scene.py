from src.core.objects.game_object import GameObject

class Scene:
    """Класс для контейнеризации игрового мира в виде сцены."""
    def __init__(self):
        self.objects: list[GameObject] = list()