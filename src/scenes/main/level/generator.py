import random
from typing import Optional

from pygame.math import Vector2

GENERATOR_TEMPLATE_LEVEL = "generator_template"
RANDOM_WALK_CHANGE_PROBAB = 0.9
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

    def generate(self, size: tuple):
        """Процесс генерации уровня."""
        template, rules = self.get_template_and_rules()
        tiles = WFC(rules, size).generate()
        template.tiles = tiles
        return template

class RandomWalk:
    """Реализация алгоритма Random Walk для генерации пути."""
    def __init__(
        self,
        tiles: list[list],
        draw_tile: int
    ):
        self.tiles = tiles
        self.draw_tile = draw_tile  # Тайл "следа" строителя.

    def generate(self, steps: int):
        # Коориднаты строителя.
        bx = random.randrange(0, len(self.tiles[0]))
        by = random.randrange(0, len(self.tiles))
        # Направление движения.
        dx, dy = random.choice(DIRECTIONS)
        for _ in range(steps):
            ...
class WFC:
    """Реализация алгоритма Wave Function Collapse для генерации окружения."""

    def __init__(self, rules: dict[int, list[int]], size: tuple):
        self.tiles: list[list] = [
            [
                set(rules.keys()).copy()
                for _ in range(size[0])
            ]
            for _ in range(size[1])
        ]
        self.rules = rules
        self.size = size
        self.collapsed = set()

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
        self.set_tile(pos, random.choice(list(tile)) if type(tile) is set else tile)
        self.collapsed.add(pos)
        self.propogate(pos)

    def propogate(self, pos):
        """Распространение схлопывания."""
        bfs = [pos,]
        while bfs:
            current = bfs.pop()
            allowed = self.get_allowed_tiles(current)
            print(f"Allowed tiles for {current}: {allowed}")
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