from src.core.objects.game_object import GameObject

class Scene:
    """Класс для контейнеризации игрового мира в виде сцены."""
    objects: list[GameObject] = list()