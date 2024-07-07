import pygame as pg

import settings


class Button():
    """
    Represents a clickable button with a number displayed on it.
    """
    radius = settings.FLOOR_WIDTH/4
    size = (radius, radius)
    color = settings.BUTTON_COLOR
    text_color = (0, 0, 0)
    text_size = int(radius*1)
    pg.font.init()


    def __init__(self, number):
        self.number = number
        self.font = pg.font.SysFont(None, self.text_size)
        self.image = self.create_button_image()
        self.rect = self.image.get_rect()
        self.clicked = False

    def create_button_image(self):
        button_surface = pg.Surface(self.size, pg.SRCALPHA)
        center = self.size[0]//2
        pg.draw.circle(button_surface, self.color, (center, center), center)
        pg.draw.circle(button_surface, self.text_color, (center, center), center, width=1)        
        text_surface = self.font.render(str(self.number), True, self.text_color)
        text_rect = text_surface.get_rect(center=(center, center))
        button_surface.blit(text_surface, text_rect)
        return button_surface

    def check_click(self, pos):
        is_clicked = self.rect.collidepoint(pos)
        return is_clicked

