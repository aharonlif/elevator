import pygame as pg

import settings

class Line(pg.sprite.Sprite):
    """
    A class representing a line used to visually separate floors in the building.
    """

    color = settings.LINE_COLOR
    thickness = settings.LINE_THICKNESS
    
    def __init__(self, bottomleft):
        super().__init__()
        self.image = pg.Surface((settings.FLOOR_WIDTH, self.thickness))
        self.image.fill(self.color)  
        self.rect = self.image.get_rect(bottomleft=bottomleft)
