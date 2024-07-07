import pygame as pg

from button import Button
import settings

class Floor(pg.sprite.Sprite):
    """
    Represents a floor in a building with a button for elevator calls.
    """
    width, height = settings.FLOOR_WIDTH, settings.FLOOR_HIGHT

    def __init__(self, floor_number, bottomleft):
        """
        Initializes the Floor object.

        Args:
            floor_number (int): The number of the floor.
                - This is used to identify the floor and display it on the button.
            bottomleft (tuple): The bottom-left position of the floor on the screen.
                - This position is used to place the floor image on the screen.
        """
        super().__init__()
        self.image = pg.image.load("help_files/floor_image.png")
        self.image = pg.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect(bottomleft=bottomleft)
        self.floor_number = floor_number
        self.button = Button(self.floor_number)
        self.button.rect.center = self.rect.center
        self.font = pg.font.SysFont(None, int(self.button.text_size / 2))
        self.draw_button()
        self.update_time_elevator()


    def change_color(self, color):
        """
        Changes the color of the button and updates its appearance.
        """
        self.button.color = color
        self.button.image = self.button.create_button_image()
        self.draw_button()


    def an_elevator_was_called(self, arrival_time):
        self.change_color(settings.BUTTON_COLOR_TEMPORARILY)
        self.update_time_elevator(arrival_time)


    def update_time_elevator(self, arrival_time=0):
        """
        Updates the display with the time remaining until the elevator arrives at this floor.
        """
        size = settings.FLOOR_WIDTH / 6
        surface_time = pg.Surface((size, size), pg.SRCALPHA)
        center = size // 2
        pg.draw.rect(surface_time, (250, 200, 250), (0, 0, size, size))
        text_surface = self.font.render(f"{arrival_time:.1f}", True, (20, 10, 100))
        text_rect = text_surface.get_rect(center=(center, center))
        if arrival_time > 0:
            surface_time.blit(text_surface, text_rect)
        self.image.blit(surface_time, text_rect)


    def draw_button(self):
        """
        Draws the button on the floor image at the center.
        """
        button_size = self.button.size[0]  
        center_floor = (self.width / 2 - button_size / 2, self.height / 2 - button_size / 2)
        self.image.blit(self.button.image, center_floor)
