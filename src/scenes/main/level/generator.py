import random
from typing import Optional

from pygame.math import Vector2

GENERATOR_TEMPLATE_LEVEL = "generator_template"
RANDOM_WALK_CHANGE_PROBAB = 0.5
DIRECTIONS = ((0, 1), (0, -1), (1, 0), (-1, 0))

class LevelGenerator:
    """Генератор уровня."""
    def __init__(self, level_loader, debug=False):
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
                set()
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
        tiles = WFC(rules, tiles, template.metadata["unallowed_to_wfc"]).generate()
        template.tiles = tiles
        return template

class RandomWalk:
    """Реализация алгоритма Random Walk для генерации пути."""
    def __init__(
        self,
        tiles: list[list],
        draw_tile: int,
        start_tile: int,
        end_tile: int
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

    def generate(self, steps: int):
        """
            Процесс генерации пути.

            Args:
                steps: длина пути.
        """
        # Коориднаты строителя.
        bx = random.randrange(0, len(self.tiles[0]))
        by = random.randrange(0, len(self.tiles))
        start_position = (bx, by)
        self.tiles[by][bx] = self.start_tile
        self.visited.add((bx, by))
        # Направление движения.
        dx, dy = tuple(random.choice(DIRECTIONS))
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
        return self.tiles

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

class WFC:
    """Реализация алгоритма Wave Function Collapse для генерации окружения."""

    def __init__(
        self,
        rules: dict[int, list[int]],
        tiles: list[list],
        unallowed_to_use: list
    ):
        """
        Args:
            rules: правила для всех типов тайлов.
            tiles: карта тайлов.
        """
        self.tiles = tiles
        self.size = (len(self.tiles[0]), len(self.tiles))
        self.collapsed = set()
        self.rules = rules
        self.unallowed_to_use = unallowed_to_use
        # Подготавливаем карту для генерации (учитываем уже схлопнутые тайлы).
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                if type(self.tiles[y][x]) is not set:
                    self.collapsed.add((x, y))
                else:
                    self.tiles[y][x] = set(rules.keys())
        self.propogate(list(self.collapsed))

    def generate(self):
        while len(self.collapsed) != self.size[0] * self.size[1]:
            self.observe()
        return self.tiles

    def observe(self):
        """Поиск несхлопнутой ячейки с наименьшей энтропией."""
        lowest_entropy = 100
        pos = tuple()
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                if (
                    self.get_entropy((x, y)) < lowest_entropy
                    and (x, y) not in self.collapsed
                ):
                    pos = (x, y)
                    lowest_entropy = self.get_entropy((x, y))
        self.collapse(pos)

    def collapse(self, pos):
        """Схлопывание ячейки."""
        tile = self.get_tile(pos)
        
        self.set_tile(
            pos,
            random.choice([variant for variant in tile if variant not in self.unallowed_to_use])
            if type(tile) is set
            else tile
        )
        self.collapsed.add(pos)
        self.propogate([pos,])

    def propogate(self, bfs):
        """Распространение схлопывания."""
        while bfs:
            current = bfs.pop()
            allowed = self.get_allowed_tiles(current)
            # print(f"Allowed tiles for {current}: {allowed}")
            for pos in DIRECTIONS:
                # Сосед текущей ячейки.
                adj = (current[0] + pos[0], current[1] + pos[1])
                if self.is_tile_valid(adj):
                    if not adj in self.collapsed:
                        if self.update_allowed_tiles(adj, allowed):
                            # Если схлопывание повлияло - добавляем в очередь.
                            bfs.append(adj)

    def is_tile_valid(self, pos):
        return pos[0] in range(0, self.size[0]) and pos[1] in range(0, self.size[1])

    def get_tile(self, pos):
        if not self.is_tile_valid(pos):
            raise ValueError(f"Тайл не существует: {pos}")
        return self.tiles[pos[1]][pos[0]]

    def get_entropy(self, pos):
        tile = self.get_tile(pos)
        return len(tile) if type(tile) is set else 1

    def set_tile(self, pos, value):
        self.tiles[pos[1]][pos[0]] = value

    def get_allowed_tiles(self, pos) -> set:
        tile = self.get_tile(pos)
        allowed: set[int] = set()
        if type(tile) is set:
            for variant in tile:
                allowed = allowed.union(set(self.rules[variant]))
            return allowed
        else:
            return set(self.rules[tile])

    def update_allowed_tiles(self, target_pos, allowed: set):
        target_variants = self.get_tile(target_pos)
        if target_variants:
            target_variants = set(target_variants)
            intersec = allowed.intersection(target_variants)
            if len(intersec) == 0:
                print(self.tiles)
                raise ValueError(
                    f"Противоречие: {target_pos}: {target_variants}, {allowed}"
                )
            self.set_tile(target_pos, intersec)
            return len(intersec) != len(target_variants)