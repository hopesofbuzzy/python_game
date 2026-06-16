import logging

import pygame

from src.core.objects import GameObject
from src.scenes.main.objects.components.inventory import InventoryModelComponent
from src.scenes.main.objects.plants import PLANTS


class Inventory(GameObject):
    ...