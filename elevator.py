import pygame as pg
import time

import settings

class Elevator(pg.sprite.Sprite):

    width, height = settings.FLOOR_HIGHT, settings.FLOOR_HIGHT
    pg.mixer.init()
    arrived_sound = pg.mixer.Sound("help_files/ding.mp3")
    floor_travel_time = 0.5 

    def __init__(self, bottomleft):
        super().__init__()
        self.image = pg.image.load("help_files/elv.png").convert_alpha()
        self.image = pg.transform.scale(self.image, (self.width, self.height)).convert_alpha()
        self.rect = self.image.get_rect(bottomleft=bottomleft)
        self.made_a_sound = False  # Flag to check if the arrival sound was played
        self.floor = 0  # The target floor for the elevator
        self.current_floor = 0  # The current floor of the elevator
        self.movement_last_time = None
        self.arrival_time = 0  # The time remaining until the elevator reaches the target floor
        self.free = True
        self.y_position = bottomleft[1]  # The Y position of the elevator at the start
        self.move_to_floors = []  # A list of floors the elevator will move to


    def moving(self) -> bool:
        return self.floor != self.current_floor


    def move_to_floor(self, floor):
        """
        Sets the target floor for the elevator and starts the movement towards it.
        """
        if not self.free:
            if not self.move_to_floors:
                arrival_time = self.arrival_time + 2 + abs(self.floor - floor) / 2
            else:
                arrival_time = self.move_to_floors[-1]["arrival time"] + 2 + abs(self.move_to_floors[-1]["floor"] - floor) / 2            
            self.move_to_floors.append({"floor": floor, "arrival time": arrival_time})
            return
        if self.moving():
            raise TypeError("Bug in the free argument")
        self.free = False
        self.floor = floor
        self.movement_last_time = time.time()
        self.arrival_time = int(abs(self.floor - self.current_floor)) / 2


    def calculate_arrival_time(self):
        """
        Updates the remaining time until the elevator arrives at the target floor.
        """
        current_time = time.time()
        elapsed_time = current_time - self.movement_last_time
        self.arrival_time -= elapsed_time
        if self.arrival_time <= -2:
            self.free = True
        for floor in self.move_to_floors:
            floor["arrival time"] -= elapsed_time
        self.movement_last_time = current_time
        return elapsed_time


    def calculate_position_to_move(self):
        """
        Calculates the new position of the elevator based on the elapsed time.
        """
        elapsed_time = self.calculate_arrival_time()
        floors_to_move = elapsed_time / self.floor_travel_time
        y_move = floors_to_move * settings.FLOOR_HIGHT
        self.y_position += y_move if self.current_floor > self.floor else -y_move
        return self.y_position


    def update(self):
        """
        Updates the state of the elevator, including its position and whether it has arrived at the target floor.

        If the elevator is free and has a target floor, it starts moving to that floor.
        """
        if self.free:
            self.movement_last_time = 0
            self.made_a_sound = False
            
            if self.move_to_floors:
                floor = self.move_to_floors[0]["floor"]
                self.arrival_time = self.move_to_floors[0]["arrival time"]
                self.move_to_floors.pop(0)
                self.move_to_floor(floor)
            else:
                return
        self.update_location()


    def update_location(self):
        """
        Updates the location of the elevator and handles the logic for arriving at the target floor.
        """
        if not self.moving():
            if self.free:
                return False
            self.calculate_arrival_time()
            return False

        if self.arrived():  
            if not self.made_a_sound:
                self.arrived_sound.play()
                self.made_a_sound = True
                self.arrival_time = 0
                self.current_floor = self.floor
                return True

        y_position = self.calculate_position_to_move()
        self.rect.bottomleft = (self.rect.x, y_position)
        return True


    def arrived(self):
        """
        Checks if the elevator has arrived at the target floor.
        """
        floor = settings.FLOOR_HIGHT + settings.LINE_THICKNESS
        y_hight = settings.SCREEN_HEIGHT - self.y_position
        return (floor * self.floor) <= y_hight if self.floor > self.current_floor else (floor * self.floor) >= y_hight
