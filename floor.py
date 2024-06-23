import pygame as pg
from button import Button
from settings import Floor as f

class Floor(pg.sprite.Sprite):
    """
    Represents a floor in a building with a button for elevator calls.
    """
    width, height = f.width, f.height

    def __init__(self, floor_number, bottomleft):
        """
        Initializes the Floor object.
        
        Args:
            floor_number (int): The number of the floor.
            bottomleft (tuple): The bottom-left position of the floor.
        """
        super().__init__()
        self.image = pg.image.load("help_files/floor_image.png")
        self.image = pg.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect(bottomleft=bottomleft)
        self.floor_number = floor_number
        self.button = Button(self.floor_number)
        self.button.rect.center = self.rect.center  # Set the button's position relative to the floor
        self.draw_button()
        self.font = pg.font.SysFont(None, int(self.button.text_size / 2))

    def update_time_elevator(self, arrival_time=99):
        """
        Updates the display with the time until the elevator arrives.
        
        Args:
            arrival_time (int, optional): The time until the elevator arrives. Defaults to 99.
        """
        time_elevator = arrival_time
        print(time_elevator)
        text_surface = self.font.render(str(time_elevator), True, (20, 200, 200))
        text_rect = text_surface.get_rect(center=(self.width // 2 - self.button.size[0], self.height // 2))
        self.image.blit(text_surface, text_rect)

    def draw_button(self):
        """
        Draws the button on the floor.
        """
        button_size = self.button.size[0]  # Height equals width
        center_floor = self.width / 2 - button_size / 2, self.height / 2 - button_size / 2
        self.image.blit(self.button.image, center_floor)
