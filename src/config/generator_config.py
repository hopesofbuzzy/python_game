import random

# Конфигурация генерации уровня.
seed = int(random.random() * 1_000_000)
PATH_LENGTH = 30
SIZE = (30, 30)
NOISE_AMPLITUDE = 5

WAVE_AMOUNT = 5

# Интересные сиды:
# Кольцо: seed=57, path_length=15
# Длинная змея: seed=57, path_length=30
# Крюк: seed=338146, path_length=30
# Ближний лес: seed=583560, path_length=30