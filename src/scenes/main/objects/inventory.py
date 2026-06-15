import logging

import pygame

from src.core.objects import GameObject
from src.scenes.main.objects.plants import PLANTS
from src.scenes.main.objects.components.inventory import InventoryModelComponent


class Inventory(GameObject):
    ...