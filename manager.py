import pygame as pg

import building
from settings import Screen


class Manager:
    
    def __init__(self, buildings=1, floors=5, elevators=3) -> None:
        pg.init()
        self.screen = pg.display.set_mode((Screen.width, Screen.hight), pg.SRCALPHA)
        pg.display.set_caption("Building Floor")
        self.buildings = [None] * buildings
        self.group = pg.sprite.Group()
        self.factory_of_buildings(floors, elevators)


    def factory_of_buildings(self, floors, elv):
        for build in range(len(self.buildings)):
            current_building = building.Building(floors, elv, building_number=build)
            self.buildings[build] = current_building
            self.group.add(current_building)

    def check_floor_click(self, mouse_pos):
        for build in self.buildings:
            for floor in build.floors:
                if floor.button.check_click(mouse_pos):
                    floor.button.change_color_temporarily()
                    build.move_elevator(floor.floor_number)

    def update(self):
        for build in self.buildings:
            build.update()
        #TODO: update Buttons

    def run(self):  
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False 
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_q:
                        running = False
                    if event.key == pg.K_a:
                        self.buildings[0].change_button_color()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    self.check_floor_click(event.pos)
                # elif event.type == pg.USEREVENT + 1:
                #     button.reset_color()
            self.screen.fill((255, 255, 255)) 
            self.update()
            self.draw(self.screen)
            pg.display.flip()
    pg.quit()

    def draw(self, screen):
        self.group.draw(screen)
