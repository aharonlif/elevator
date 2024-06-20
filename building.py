import pygame as pg

from floor import Floor as flr
from black_line import Line
from elevator import Elevator as elv


class Building(pg.sprite.Group):
    difference_building = flr.width*2 + elv.width

    def __init__(self, y_screen, floors: int, elevators: int, building_number=0):
        super().__init__()
        self.floors = [None] * floors
        self.elevators = [None] * elevators
        self.building_position_x = 0
        self.y_screen = y_screen
        self.building_number = building_number
        self.floors_factory()
        self.elevators_factory(elevators)
        self.calls_to_the_elevator = []

        
    def floors_factory(self):
        y_position = self.y_screen
        line_position = self.y_screen
        for i in range(len(self.floors)):
            self.floors[i] = flr(i, bottomleft=(0, y_position))
            self.add(self.floors[i])
            y_position -= flr.height + Line.thickness
            if i == 0:
                line_position -= flr.height
            else:
                #TODO: a good black line
                print(i)

                line_position -= ((i-1) * (flr.height + Line.thickness))
                self.add(Line((0, line_position), (flr.width-Line.thickness, line_position)))

    def elevators_factory(self, elevators):
        for i in range(elevators):
            x_position = self.building_position_x + flr.width + (i* elv.width)
            y_position = self.y_screen
            elevator = elv(bottomleft=(x_position, y_position))
            self.add(elevator)
            self.elevators[i] = elevator

    def _find_nearest_elevator(self, floor):
        try:
            nearest_elevator = min((elevator for elevator in self.elevators if not (elevator.moving() and elevator.floor != floor)), key=lambda elevator: abs(elevator.floor - floor))
        except Exception:
            if floor  not in self.calls_to_the_elevator:
                self.calls_to_the_elevator.append(floor)
            return
        return nearest_elevator
    
    def move_elevator(self, floor):
        nearest_elevator = self._find_nearest_elevator(floor) 
        if nearest_elevator:
            nearest_elevator.move_to_floor(floor)
            return True



    def update(self):
        "run of all elevators and if need to move - move it."
        if self.calls_to_the_elevator:
            if self.move_elevator(self.calls_to_the_elevator[0]):
                self.calls_to_the_elevator.pop(0)
        for elv in self.elevators:
            elv.update_location()        