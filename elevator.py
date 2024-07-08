import pygame as pg
import time

import global_vars

pg.mixer.init()

class Elevator(pg.sprite.Sprite):
    width, height = global_vars.FLOOR_HIGHT, global_vars.FLOOR_HIGHT
    arrived_sound = pg.mixer.Sound("help_files/ding.mp3")
    floor_travel_time = 0.5 

    def __init__(self, bottomleft):
        super().__init__()
        self.image = pg.image.load("help_files/elv.png").convert_alpha()
        self.image = pg.transform.scale(self.image, (self.width, self.height)).convert_alpha()
        self.rect = self.image.get_rect(bottomleft=bottomleft)
        self.made_a_sound = False  # Flag to check if the arrival sound was played
        self.target_floor = 0  # The target floor for the elevator
        self.current_floor = 0  # The current floor of the elevator
        self.arrival_time = 0  # The time remaining until the elevator reaches the target floor
        self.free = True # Free to move
        self.y_position = bottomleft[1]  # The Y position of the elevator at the start
        self.floors_waiting = []  # A list of floors the elevator will move to


    def moving(self) -> bool:
        return self.target_floor != self.current_floor


    def add_task(self, floor):
        """
        Sets the target floor for the elevator and starts the movement towards it, or add to queue.
        """
        if not self.free:
            if len(self.floors_waiting) == 0:
                arrival_time = self.arrival_time + 2 + abs(self.target_floor - floor) / 2
            else:
                arrival_time = self.floors_waiting[-1]["arrival time"] + 2 + abs(self.floors_waiting[-1]["floor"] - floor) / 2            
            self.floors_waiting.append({"floor": floor, "arrival time": arrival_time})
            return
        self.start_task(floor)
        

    def start_task(self, floor):
        self.free = False
        self.target_floor = floor
        self.arrival_time = int(abs(self.target_floor - self.current_floor)) / 2


    def update_arrival_time(self):
        """
        Updates the remaining time until the elevator arrives at the target floor.
        """
        self.arrival_time -= global_vars.ELAPSED_TIME

        if self.arrival_time <= -2:
            self.free = True
            self.movement_last_time = 0
            self.made_a_sound = False

        for floor in self.floors_waiting:
            floor["arrival time"] -= global_vars.ELAPSED_TIME



    def calculate_position_to_move(self):
        """
        Calculates the new position of the elevator based on the elapsed time.
        """
        self.update_arrival_time()
        time_fraction = global_vars.ELAPSED_TIME / self.floor_travel_time
        y_move = time_fraction * global_vars.FLOOR_HIGHT
        self.y_position += y_move if self.current_floor > self.target_floor else -y_move
        return self.y_position


    def update(self):
        """
        Updates the state of the elevator, including its position and whether it has arrived at the target floor.

        If the elevator is free and has a target floor, it starts moving to that floor.
        """
        if self.free:           
            if self.floors_waiting:
                floor = self.floors_waiting[0]["floor"]
                self.arrival_time = self.floors_waiting[0]["arrival time"]
                self.floors_waiting.pop(0)
                self.start_task(floor)
            else:
                return
        self.update_location()


    def update_location(self):
        """
        Updates the location of the elevator and handles the logic for arriving at the target floor.
        """
        if self.free:
            return 
        
        if not self.moving():
            self.update_arrival_time()
            return 

        if self.arrived():  
            if not self.made_a_sound:
                self.arrived_sound.play()
                self.made_a_sound = True
                self.arrival_time = 0
                self.current_floor = self.target_floor
                return True

        y_position = self.calculate_position_to_move()
        self.rect.bottomleft = (self.rect.x, y_position)


    def arrived(self):
        """
        Checks if the elevator has arrived at the target floor.
        """
        floor = global_vars.FLOOR_HIGHT + global_vars.LINE_THICKNESS
        y_hight = global_vars.SCREEN_HEIGHT - self.y_position
        return (floor * self.target_floor) <= y_hight if self.target_floor > self.current_floor else (floor * self.target_floor) >= y_hight
