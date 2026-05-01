from src.core.systems.scene import Scene

class MovementSystem:
    def update(self, scene: Scene):
        for object in scene.object_registry:
            
        # Двигаем объекты