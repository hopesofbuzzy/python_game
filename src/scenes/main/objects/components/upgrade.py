from src.scenes.main.objects import PLANTS_LEVEL_UPS

class UpgradeComponent:
    def __init__(self):
        self.suns: int = 0

    def upgrade(self, suns: int):
        self.suns += suns