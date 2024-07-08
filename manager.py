from typing import List
import pygame as pg

from building import Building
import global_vars

class Manager:
    """
    Manages the game, including the screen setup, building initialization, 
    event handling, and game loop.
    """

    def __init__(self) -> None:
        """
        Initializes the Manager with the game setup including screen configuration, building creation, 
        and sprite group initialization.
        
        Args:
            buildings (int): Number of buildings to be created for the game.
                - The `buildings` parameter specifies how many building configurations to initialize.
        """
        pg.init()
        self.screen = pg.display.set_mode((global_vars.SCREEN_WIDTH, global_vars.SCREEN_HEIGHT), pg.SRCALPHA)
        pg.display.set_caption("Building Floor")  # Set the title of the game window
        self.buildings :List[Building]  = [None] * len(global_vars.BUILDINGS)
        self.group = pg.sprite.Group()        
        self.factory_of_buildings()


    def factory_of_buildings(self):
        """
        Creates and initializes buildings based on the configuration provided in `settings.BUILDINGS`.
        Each building is positioned sequentially based on the number of elevators and floors in the previous building.
        """
        for i, build in enumerate(global_vars.BUILDINGS):
            if i == 0:
                x_position = 0
            else:
                x_position = self.buildings[i-1].x_position + global_vars.FLOOR_WIDTH + global_vars.FLOOR_HIGHT * (global_vars.BUILDINGS[i-1]["elevators"])
            
            current_building = Building(build, x_position)
            self.buildings[i] = current_building
            self.group.add(current_building)


    def check_floor_click(self, mouse_pos):
        """
        Checks if a floor button is clicked and calls the elevator to move to the respective floor if needed.
        
        Args:
            mouse_pos (tuple): The position of the mouse click on the screen (x, y).
                - This position is used to determine if a floor button was clicked.
        """
        for build in self.buildings:
            for floor in build.floors:
                if floor.button.check_click(mouse_pos):
                    # Check if there is no elevator currently at this floor or scheduled to move to this floor
                    if not any(floor.floor_number == elev.target_floor or any(floor.floor_number == d.get("floor") for d in elev.floors_waiting) for elev in build.elevators):
                        build.call_to_elevator(floor.floor_number)
                    return

    def update(self):
        """
        Updates the state of all buildings and their elevators.
        Calls the `update` method on each building to refresh the state and handle any changes.
        """
        for building_ in self.buildings:
            building_.update()


    def draw(self):
        """
        Draws all sprites to the screen.
        This method is responsible for rendering the current state of all game elements.
        """
        self.group.draw(self.screen)
