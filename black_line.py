import pygame as pg

import global_vars

class Line(pg.sprite.Sprite):
    """
    A class representing a line used to visually separate floors in the building.
    """
    color = global_vars.LINE_COLOR
    thickness = global_vars.LINE_THICKNESS
    
    def __init__(self, bottomleft):
        super().__init__()
        self.image = pg.Surface((global_vars.FLOOR_WIDTH, self.thickness))
        self.image.fill(self.color)  
        self.rect = self.image.get_rect(bottomleft=bottomleft)
