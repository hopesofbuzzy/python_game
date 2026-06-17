from src.scenes.main.level.loader import LevelLoader


class LevelGenerator:
    """Генератор уровня."""
    def __init__(self, level_loader: LevelLoader, debug=False):
        self.level_loader = level_loader

    def generate(self):
        """Процесс генерации уровня."""
        template = self.level_loader.load_template_level()

    def wfc(self):
        """Реализация алгоритма wfcю"""
        ...