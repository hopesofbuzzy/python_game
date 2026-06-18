import math
import random
from collections import deque
from typing import Optional

from pygame.math import Vector2

from src.scenes.main.level.wave_generator import WaveGenerator

GENERATOR_TEMPLATE_LEVEL = "generator_template"\
# RandomWalk
RANDOM_WALK_CHANGE_PROBAB = 0.5
DIRECTIONS = ((1, 0), (0, 1), (-1, 0), (0, -1))
# PerlinNoise
GRAD = ((1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1))
CORNERS = ((0, 0), (0, 1), (1, 0), (1, 1))
NOISE_AMPLITUDE = 2.5

DEFAULT_WAVE_COUNT = 5

def perm(seed=0):
    """PerlinNoise: Таблица перетсановок для получения градиента в (x, y)."""
    rng = random.Random(seed)
    p = list(range(256))
    rng.shuffle(p)
    return p + p

def is_tile_valid(pos, size):
    return pos[0] in range(0, size[0]) and pos[1] in range(0, size[1])


class LevelGenerator:
    """Генератор уровня."""
    def __init__(self, level_loader, debug=False, seed=0):
        self.level_loader = level_loader

    def get_template_and_heights(self):
        template = self.level_loader.load_generator_template_level()
        heights = template.metadata["heights"]
        rules = {
            tile: height
            for tile, height in heights
        }
        return template, heights

    def build_tiles(self, size: tuple):
        return [
            [
                26
                for _ in range(size[0])
            ]
            for _ in range(size[1])
        ]

    def generate_map_with_path(
        self,
        map_size,
        path_length,
        path_tile,
        start_tile,
        end_tile,
        seed=0
    ):
        tiles = self.build_tiles(map_size)
        tiles = RandomWalk(
            tiles,
            path_tile,
            start_tile,
            end_tile,
            seed
        ).generate(path_length)
        return tiles

    def generate_enviroment(
        self,
        tiles,
        size,
        path_tile,
        heights,
        visited_tiles,
        seed=0,
        noise_amplitude=NOISE_AMPLITUDE,
    ):
        noise = PerlinNoise(seed)
        distance_field = DistanceField(tiles, path_tile).calculate()
        for y in range(size[1]):
            for x in range(size[0]):
                if (x, y) not in visited_tiles:
                    noise_val = noise.noise2d(x / size[0], y / size[1])
                    dist_val = distance_field[y][x]
                    print(noise_val * noise_amplitude)
                    print(x / size[0], y / size[1])
                    generated_height = dist_val + noise_val * noise_amplitude
                    generated_tile = -1
                    for tile, height in heights:
                        if generated_height >= height:
                            generated_tile = tile
                    tiles[y][x] = generated_tile
        return tiles

    def generate(
        self,
        path_length: int,
        size: tuple,
        seed=0,
        noise_amplitude=NOISE_AMPLITUDE,
        wave_count: int = DEFAULT_WAVE_COUNT
    ):
        """
            Процесс генерации уровня.

            Returns:
                raw_level: сырой уровень с картой (tiles) и данными (metadata).
                parsed_waves: сгенерированный объект волн.
        """
        template, heights = self.get_template_and_heights()
        tiles, visited = self.generate_map_with_path(
            size,
            path_length,
            template.metadata["path_tiles"][0],
            template.metadata["start_tile"],
            template.metadata["end_tile"],
            seed,
        )
        tiles = self.generate_enviroment(
            tiles,
            size,
            template.metadata["path_tiles"][0],
            heights,
            visited,
            seed,
            noise_amplitude
        )
        template.tiles = tiles
        parsed_waves = WaveGenerator().generate_waves(wave_count, seed)
        return template, parsed_waves


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
        self.seed = seed

    def generate(self, steps: int):
        """
            Процесс генерации пути.

            Args:
                steps: длина пути.

            Returns:
                tiles: карта тайлов с дорогой
                visited: координаты всех тайлов дороги
        """
        print(f"SEED: {self.seed}")
        rng = random.Random(self.seed)
        self.original_tiles = self.tiles
        while True:
            try:
                visited = set()
                self.tiles = [[num for num in row] for row in self.original_tiles]
                # Коориднаты строителя.
                bx = rng.randrange(0, len(self.tiles[0]))
                by = rng.randrange(0, len(self.tiles))
                self.tiles[by][bx] = self.start_tile
                visited.add((bx, by))
                # Направление движения.
                dx, dy = (0, 0)
                for _ in range(steps):
                    # Назад нельзя
                    posisble_directions = [d for d in DIRECTIONS if d != (-dx, -dy)]
                    while True:
                        if len(posisble_directions) == 0:
                            raise Exception("Путь блокирован!")
                        new_direction = rng.choice(posisble_directions)
                        if dx == dy == 0:
                            direction = new_direction
                        else:
                            direction = rng.choices(
                                [(dx, dy), new_direction],
                                [1 - RANDOM_WALK_CHANGE_PROBAB, RANDOM_WALK_CHANGE_PROBAB],
                                k=1
                            )[0]
                        dx, dy = direction
                        print(f"Trying move {(bx, by)} -> {(bx + dx, by + dy)}")
                        if (
                            is_tile_valid((bx + dx, by + dy), self.size)
                            and self.is_valid_path((bx + dx, by + dy), (bx, by), visited)
                        ):
                            bx, by = (bx + dx, by + dy)
                            self.tiles[by][bx] = self.draw_tile
                            visited.add((bx, by))
                            break
                        else:
                            posisble_directions.remove(new_direction)
                self.tiles[by][bx] = self.end_tile
                return self.tiles, visited
            except Exception as e:
                    print(f"Ошибка генерации пути: {e}")

    def is_valid_path(self, pos, old_pos, visited):
        """Проверка на тупик."""
        for direciton in DIRECTIONS:
            adj_x, adj_y = (direciton[0] + pos[0], direciton[1] + pos[1])
            if (
                (adj_x, adj_y) != old_pos
                and type(self.tiles[adj_y][adj_x]) is int
            ):
                if (adj_x, adj_y) in visited:
                    return False
        return True

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
    """Алгоритм вычисления поля дистанций для всех тайлов до источника (BFS)."""
    def __init__(self, tiles: list[list], source_tile: int):
        self.size = (len(tiles[0]), len(tiles))
        self.distance_field = [
            [
                None
                for x in range(self.size[0])
            ]
            for y in range(self.size[1])
        ]
        self.source_tiles = list()
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                if tiles[y][x] == source_tile:
                    self.source_tiles.append((x, y))

    def calculate(self):
        """Вычисление поля дистанций по BFS."""
        LEVEL_MARKER = None
        queue = deque(self.source_tiles + [LEVEL_MARKER])
        visited = set(self.source_tiles)
        distance = 0
        while queue:
            current = queue.popleft()
            if current == LEVEL_MARKER:
                distance += 1
                if queue:
                    queue.append(LEVEL_MARKER)
            elif current:
                self.set_tile(current, distance)
                for dx, dy in DIRECTIONS:
                    adj = current[0] + dx, current[1] + dy
                    if is_tile_valid(adj, self.size) and adj not in visited:
                        visited.add(adj)
                        queue.append(adj)
        return self.distance_field

    def set_tile(self, pos, value):
        self.distance_field[pos[1]][pos[0]] = value
