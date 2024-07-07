import pygame as pg

from floor import Floor as flr
from black_line import Line
from elevator import Elevator as elv
import settings

class Building(pg.sprite.Group):
    """
    Represents a building containing multiple floors and elevators.
    Manages the elevators and their movements.
    """
    def __init__(self, build, x_position):
        """
        Initializes the Building object.
        This constructor sets up the building with the specified configuration and position.
        Args:
            build (dict): A dictionary containing the configuration for the building.
                - "floors" (int): The number of floors in the building.
                - "elevators" (int): The number of elevators in the building.
            x_position (int): The x-coordinate for the position of the building on the screen.
        """
        super().__init__()
        self.floors = [None] * build["floors"]
        self.elevators = [None] * build["elevators"]
        self.x_position = x_position
        self.create_floors()
        self.create_elevators()


    def create_floors(self):
        """
        Creates the floors for the building and adds them to the sprite group.
        Draws lines between the floors.
        """
        y_position = settings.SCREEN_HEIGHT
        line_y_position = settings.SCREEN_HEIGHT
        for i in range(len(self.floors)):
            self.floors[i] = flr(i, bottomleft=(self.x_position, y_position))
            self.add(self.floors[i])
            y_position -= flr.height + Line.thickness

            if i == 1:
                line_y_position -= flr.height
                self.add(Line(bottomleft=(self.x_position, line_y_position)))
                continue

            if i:
                line_y_position -= flr.height + Line.thickness
                self.add(Line(bottomleft=(self.x_position, line_y_position)))


    def create_elevators(self):
        """
        Creates the elevators for the building and adds them to the sprite group.
        """
        for i in range(len(self.elevators)):
            x_position = self.x_position + flr.width + (i * elv.width)
            y_position = settings.SCREEN_HEIGHT
            elevator = elv(bottomleft=(x_position, y_position))
            self.add(elevator)
            self.elevators[i] = elevator


    def _find_nearest_elevator(self, floor):
        nearest_elevator = min(
            (elevator for elevator in self.elevators),
            key=lambda elevator: elevator.arrival_time + (not elevator.free) * 2 + abs(elevator.floor - floor) / 2 if not (elevator.move_to_floors)
            else elevator.move_to_floors[-1]["arrival time"] + 2 + abs(elevator.move_to_floors[-1]["floor"] - floor) / 2
        )
        return nearest_elevator


    def call_to_elevator(self, floor):
        """
        Calls the nearest available elevator to the specified floor.
        """
        nearest_elevator = self._find_nearest_elevator(floor)
        nearest_elevator.move_to_floor(floor)
        self.floors[floor].an_elevator_was_called(nearest_elevator.arrival_time)


    def update(self):
        """
        Updates the state of the building, moving elevators as needed.
        Processes any pending elevator calls.
        """
        for elv in self.elevators:
            elv.update()
            if not elv.moving() and self.floors[elv.floor].button.color == settings.BUTTON_COLOR_TEMPORARILY:
                self.floors[elv.floor].change_color(settings.BUTTON_COLOR)

            if not elv.free:
                floor = elv.floor
                self.floors[floor].update_time_elevator(elv.arrival_time)
            if elv.move_to_floors:
                for floor in elv.move_to_floors:
                    self.floors[floor["floor"]].update_time_elevator(floor["arrival time"])
