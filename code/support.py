import pygame
from os import walk
from settings import TILE_SIZE
from csv import reader

def import_cut_graphics(path):
    image = pygame.image.load(path).convert_alpha()
    w, h = image.get_size()
    row_num, col_num = h // TILE_SIZE, w // TILE_SIZE

    surf_lst = []

    for y in range(row_num):
        for x in range(col_num):
            pos = (x * TILE_SIZE, y * TILE_SIZE)
            surface = pygame.Surface((TILE_SIZE, TILE_SIZE), flags=pygame.SRCALPHA)
            surface.blit(image, (0, 0), area=pygame.Rect(pos, (TILE_SIZE, TILE_SIZE)))
            surf_lst.append(surface)
    return surf_lst

def import_data(path):
    with open(path) as f:
        data = reader(f)
        lst = []
        for row in data:
            lst.append(row)

        return lst

