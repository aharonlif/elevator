from typing import List
import pygame as pg

from building import Building
from building_factory import IBUildingFactory, IBuilding
import global_vars


class BUildingFactory(IBUildingFactory):
    def __init__(self) -> None:
        super().__init__()
    def create_building(self, building_config, x_position) ->IBuilding:
        return Building(building_config, x_position)
    

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
        self.building_factory = BUildingFactory()
       
        self.create_buildings()


    def create_buildings(self):
        """
        Creates and initializes buildings based on the configuration provided in `settings.BUILDINGS`.
        Each building is positioned sequentially based on the number of elevators and floors in the previous building.
        """
        for i, build in enumerate(global_vars.BUILDINGS):
            if i == 0:
                x_position = 0
            else:
                x_position = self.buildings[i-1].x_position + global_vars.FLOOR_WIDTH + global_vars.FLOOR_HIGHT * (global_vars.BUILDINGS[i-1]["elevators"])
            
            current_building = self.building_factory.create_building(build, x_position)
            self.buildings[i] = current_building
            self.group.add(current_building)


    def check_click(self, mouse_pos):
        for building_ in self.buildings:
            if building_.check_click(mouse_pos):
                return

    def update(self):
        for building_ in self.buildings:
            building_.update()


    def draw(self):
        self.group.draw(self.screen)
