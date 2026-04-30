from src.core.systems.input import InputManager
from src.core.systems.physics import PhysicsSystem
from src.core.systems.renderer import Renderer
from src.core.systems.scene import Scene

class Game:
    def __init__(self, scene: Scene):
        self.input: InputManager = InputManager()
        self.physics = PhysicsSystem()
        self.renderer = Renderer()
        self.scene: Scene = scene
        self.is_paused: bool = False
        self.is_running: bool = True

    def update(self, delta_time: float):
        self.input.update()

    def draw(self):
        self.renderer.draw()