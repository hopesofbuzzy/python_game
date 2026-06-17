import math
import random
from typing import Optional

from pygame.math import Vector2

GENERATOR_TEMPLATE_LEVEL = "generator_template"\
# RandomWalk
RANDOM_WALK_CHANGE_PROBAB = 0.5
DIRECTIONS = ((1, 0), (0, 1), (-1, 0), (0, -1))
# PerlinNoise
GRAD = ((1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1))
CORNERS = ((0, 0), (0, 1), (1, 0), (1, 1))

def perm(seed=0):
    """PerlinNoise: Таблица перетсановок для получения градиента в (x, y)."""
    rng = random.Random(seed)
    p = list(range(256))
    rng.shuffle(p)
    return p + p


class LevelGenerator:
    """Генератор уровня."""
    def __init__(self, level_loader, debug=False, seed=0):
        self.level_loader = level_loader

    def get_template_and_rules(self):
        template = self.level_loader.load_generator_template_level()
        rules = template.metadata["rules"]
        rules = {
            int(key): value
            for key, value in rules.items()
        }
        return template, rules

    def build_tiles(self, size: tuple):
        return [
            [
                26
                for _ in range(size[0])
            ]
            for _ in range(size[1])
        ]

    def generate(self, path_length: int, size: tuple):
        """Процесс генерации уровня."""
        template, rules = self.get_template_and_rules()
        while True:
            try:
                tiles = self.build_tiles(size)
                tiles = RandomWalk(
                    tiles,
                    template.metadata["path_tiles"][0],
                    template.metadata["start_tile"],
                    template.metadata["end_tile"]
                ).generate(path_length)
                break
            except Exception as e:
                print(f"Путь блокирован!")
        print(f"Tiles after RandomWalk: {tiles}")
        # tiles = WFC(rules, tiles, template.metadata["unallowed_to_wfc"]).generate()
        template.tiles = tiles
        return template

class RandomWalk:
    """Реализация алгоритма Random Walk для генерации пути."""
    def __init__(
        self,
        tiles: list[list],
        draw_tile: int,
        start_tile: int,
        end_tile: int,
        seed=0
    ):
        """
        Args:
            tiles: карта тайлов.
            draw_tile: тайл, которым строитель будет рисовать.
        """
        self.tiles = tiles
        self.size = (len(self.tiles[0]), len(self.tiles))
        self.draw_tile = draw_tile  # Тайл "следа" строителя.
        self.start_tile = start_tile
        self.end_tile = end_tile
        self.visited = set()
        self.rng = random.Random(seed)

    def generate(self, steps: int):
        """
            Процесс генерации пути.

            Args:
                steps: длина пути.

            Returns:
                tiles: карта тайлов с дорогой
                visited: координаты всех тайлов дороги
        """
        # Коориднаты строителя.
        bx = self.rng.randrange(0, len(self.tiles[0]))
        by = self.rng.randrange(0, len(self.tiles))
        start_position = (bx, by)
        self.tiles[by][bx] = self.start_tile
        self.visited.add((bx, by))
        # Направление движения.
        dx, dy = tuple(self.rng.choice(DIRECTIONS))
        for _ in range(steps):
            # Назад нельзя
            posisble_directions = [d for d in DIRECTIONS if d != (-dx, -dy)]
            while True:
                if len(posisble_directions) == 0:
                    raise Exception("Путь блокирован!")
                new_direction = random.choice(posisble_directions)
                direction = random.choices(
                    [(dx, dy), new_direction],
                    [1 - RANDOM_WALK_CHANGE_PROBAB, RANDOM_WALK_CHANGE_PROBAB],
                    k=1
                )[0]
                dx, dy = direction
                if (
                    self.is_tile_valid((bx + dx, by + dy))
                    and self.is_valid_path((bx + dx, by + dy), (bx, by))
                ):
                    bx, by = (bx + dx, by + dy)
                    self.tiles[by][bx] = self.draw_tile
                    self.visited.add((bx, by))
                    break
                else:
                    posisble_directions.remove(new_direction)
        self.tiles[by][bx] = self.end_tile
        return self.tiles, self.visited

    def is_valid_path(self, pos, old_pos):
        """Проверка на тупик."""
        for direciton in DIRECTIONS:
            adj_x, adj_y = (direciton[0] + pos[0], direciton[1] + pos[1])
            if (
                (adj_x, adj_y) != old_pos
                and type(self.tiles[adj_y][adj_x]) is int
            ):
                if (adj_x, adj_y) in self.visited:
                    return False
        return True

    def is_tile_valid(self, pos):
        return pos[0] in range(0, self.size[0]) and pos[1] in range(0, self.size[1])

class PerlinNoise:
    """Шум Перлина для плавности поля дистанций от пути."""
    def __init__(self, seed=0):
        self.seed = seed
        self.perm = perm(self.seed)

    def lerp(self, a, b, t):
        """Линейная интерполяция между a и b."""
        return a + t * (b - a)

    def grad(self, hash_val, x, y):
        """
        Получение скалярного произведения градиента
        и вектора от узла до точки.

        Градиент в точке считается по хэшированным координатам
        точки (perm - функция хэширования вида perm[perm[x] + y]).
    """
        grad = GRAD[hash_val % 8]
        return grad[0] * x + grad[1] * y

    def fade(self, t):
        """Функция сглаживания (нуль на 0 и 1)"""
        # 6t^5 - 15t^4 + 10t^3
        return t * t * t * (t * (t * 6 - 15) + 10)

    def noise2d(self, x, y):
        xi = math.floor(x) % 256
        yi = math.floor(y) % 256
        xf = x - math.floor(x)
        yf = y - math.floor(y)

        # Хеширование 4 углов
        p = self.perm
        aa = p[p[xi] + yi]
        ab = p[p[xi] + yi + 1]
        ba = p[p[xi + 1] + yi]
        bb = p[p[xi + 1] + yi + 1]

        # Скалярные произведения для каждого угла
        val_bl = self.grad(aa, xf, yf)
        val_br = self.grad(ba, xf - 1, yf)
        val_tl = self.grad(ab, xf, yf - 1)
        val_tr = self.grad(bb, xf - 1, yf - 1)

        # Сглаженные веса
        u, v = self.fade(xf), self.fade(yf)

        bottom = self.lerp(val_bl, val_br, u)
        top = self.lerp(val_tl, val_tr, u)
        
        # Финальная интерполяция по Y
        return self.lerp(bottom, top, v)

class DistanceField:
    """Алгоритм вычисления поля дистанций для всех тайло до пути (BFS)."""
    def __init__(self):
        ...