from src.core.objects.game_object import GameObject


# Базовое растение
class BasePlant(GameObject):
    """Универсальное растение."""

    ...


class Mushroom(BasePlant):
    """Небольшой грибок-стрелок"""

    ...


class LongMushroom(BasePlant):
    """Длинный грибок-снайпер"""

    ...


class BigMushroom(BasePlant):
    """Большой гриб"""

    ...


# Подсолнышко.
class Sunflower(BasePlant):
    """Подсолнышко, дающее солнышки."""

    ...
