from src.core.objects.game_object import Controller, Model2D, View2D

class Scene:
    """Класс для контейнеризации игрового мира в виде сцены."""
    controllers: dict[str, Controller] = {}
    models: dict[str, Model2D] = {}
    views: dict[str, View2D] = {}
