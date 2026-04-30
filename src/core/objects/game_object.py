class GameObject:
    def __init__(self):
        self.position: tuple[float, float] = (0, 0)
        # Радианы.
        self.rotation: float = 0
        # Прослойка цвета.
        self.modulate: tuple[int, int, int] = (255, 255, 255)