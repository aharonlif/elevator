import pygame as pg
import time

import global_vars

pg.mixer.init()

class Elevator(pg.sprite.Sprite):
    """
    Represents an elevator in a building.

    Attributes:
    width (int): The width of the elevator, set from global variables.
    height (int): The height of the elevator, set from global variables.
    arrived_sound (pg.mixer.Sound): The sound to play when the elevator arrives at a floor.
    floor_travel_time (float): The time it takes for the elevator to travel between floors, set from global variables.
    image (pg.Surface): The image representing the elevator.
    rect (pg.Rect): The rectangle representing the elevator's position and size.
    y_position (float): The current Y position of the elevator.
    target_floor (int): The floor the elevator is currently moving towards.
    current_floor (int): The current floor the elevator is on.
    arrival_time (float): The time remaining until the elevator reaches the target floor.
    free (bool): A flag indicating if the elevator is free to take a new task.
    floors_waiting (list): A list of floors the elevator will move to, with their respective arrival times.

    Methods:
    add_task(floor): Sets the target floor for the elevator and starts the movement towards it, or adds it to the queue.
    start_task(floor): Starts the task of moving the elevator to the specified floor.
    update(): Updates the state of the elevator based on its current conditions.
    update_location(): Updates the location of the elevator and handles the logic for arriving at the target floor.
    update_arrival_time(): Updates the remaining time until the elevator arrives at the target floor.
    on_arrival(): Plays the arrival sound and sets the elevator's state to indicate it has arrived.
    arrived() -> bool: Checks if the elevator has arrived at the target floor.
    moving() -> bool: Checks if the elevator is currently moving.
    calculate_movement_time(floor) -> float: Calculates the movement time for the elevator to reach the specified floor.
    """
    
    width, height = global_vars.FLOOR_HIGHT, global_vars.FLOOR_HIGHT
    arrived_sound = pg.mixer.Sound("help_files/ding.mp3")
    floor_travel_time = global_vars.FLOOR_ELEVATOR_TRAVEL_TIME

    def __init__(self, bottomleft):
        super().__init__()
        self.image = pg.image.load("help_files/elv.png").convert_alpha()
        self.image = pg.transform.scale(self.image, (self.width, self.height)).convert_alpha()
        self.rect = self.image.get_rect(bottomleft=bottomleft)
        self.y_position = bottomleft[1] 
        self.target_floor = 0 
        self.current_floor = 0 
        self.arrival_time = 0 
        self.free = True
        self.floors_waiting = [] 


    def add_task(self, floor):
        """
        Sets the target floor for the elevator and starts the movement towards it, or add to queue.
        """
        if not self.free:
            if len(self.floors_waiting) == 0:
                arrival_time = self.arrival_time + global_vars.WAITING_TIME_FOR_ELEVATOR_ARRIVAL + abs(self.target_floor - floor) * self.floor_travel_time
            else:
                arrival_time = self.floors_waiting[-1]["arrival time"] + global_vars.WAITING_TIME_FOR_ELEVATOR_ARRIVAL + abs(self.floors_waiting[-1]["floor"] - floor) * self.floor_travel_time            
            self.floors_waiting.append({"floor": floor, "arrival time": arrival_time})
            return
        self.start_task(floor)
        

    def start_task(self, floor):
        """
        Starts the task of moving the elevator to the specified floor.
        """
        self.free = False
        self.target_floor = floor
        self.arrival_time = int(abs(self.target_floor - self.current_floor)) * self.floor_travel_time


    def update(self):
        """
        Updates the state of the elevator.

        This method performs several tasks based on the elevator's current state:

        - If the elevator is free:
            - Checks if there are any floors waiting in the queue. If so, it processes the next floor in the queue by setting it as the target floor and updating the arrival time. It then starts the task of moving to that floor and updates the elevator's location.
        - If the elevator is not free:
            - If the elevator has reached the target floor (i.e., it is not moving), it updates the arrival time and checks if it has arrived. If it has arrived and the sound has not been played, it triggers the arrival sound and marks that the sound has been played.
            - If the elevator is moving, it updates its location based on the elapsed time.
        """
        if self.free:           
            if len(self.floors_waiting) > 0:
                floor = self.floors_waiting[0]["floor"]
                self.arrival_time = self.floors_waiting[0]["arrival time"]
                self.floors_waiting.pop(0)
                self.start_task(floor)
            else:
                return          

        if not self.moving():
            self.update_arrival_time()
            return
        
        if self.arrived():  
            if not self.current_floor == self.target_floor:
                self.on_arrival()
            return

        self.update_location()


    def update_location(self):
        """
        Updates the location of the elevator and handles the logic for arriving at the target floor.
        """
        self.update_arrival_time()
        time_fraction = global_vars.ELAPSED_TIME / self.floor_travel_time
        y_move = time_fraction * global_vars.FLOOR_HIGHT
        self.y_position += y_move if self.current_floor > self.target_floor else -y_move
        self.rect.y =  self.y_position - self.height


    def update_arrival_time(self):
        """
        Updates the remaining time until the elevator arrives at the target floor.
        """
        self.arrival_time -= global_vars.ELAPSED_TIME

        if self.arrival_time <= -global_vars.WAITING_TIME_FOR_ELEVATOR_ARRIVAL:
            self.free = True
            self.made_a_sound = False

        for floor in self.floors_waiting:
            floor["arrival time"] -= global_vars.ELAPSED_TIME


    def on_arrival(self):
        """
        Handles the actions to perform when the elevator arrives at the target floor.
        """
        self.arrived_sound.play()
        self.made_a_sound = True
        self.arrival_time = 0
        self.current_floor = self.target_floor


    def arrived(self):
        """
        Checks if the elevator has arrived at the target floor.
        """
        floor = global_vars.FLOOR_HIGHT + global_vars.LINE_THICKNESS
        y_hight = global_vars.SCREEN_HEIGHT - self.y_position
        return (floor * self.target_floor) <= y_hight if self.target_floor > self.current_floor else (floor * self.target_floor) >= y_hight


    def moving(self) -> bool:
        return self.target_floor != self.current_floor


    def free(self):
        return self.free
    

    def calculate_movement_time(self, floor):
        """
        Calculate the movement time for the elevator to reach a specified floor.

        Parameters:
        floor (int): The target floor to calculate the movement time for.

        Returns:
        float: The estimated time for the elevator to reach the specified floor.

        Logic:
        - If there are floors waiting:
            - Calculate the arrival time based on the last floor waiting, adding the global waiting time and the time to move to the target floor.
        - If the elevator is not free:
            - Calculate the arrival time based on the current target floor, adding the global waiting time and the time to move to the target floor.
        - If the elevator is free:
            - Calculate the time based on the current floor to the target floor.

        Note: It is requested to add 2 seconds to the elevator that does not release even when time has passed since its arrival if it is not released,
                 since "self_time.arrival" is updated after the arrival of the elevator to minus.

        Movement time is calculated as half (that is "global_vars.FLOOR_TRAVEL_TIME" variable) the absolute difference between the current/target floor and the specified floor.
        """
        if len(self.floors_waiting) > 0:
            return self.floors_waiting[-1]["arrival time"] + global_vars.WAITING_TIME_FOR_ELEVATOR_ARRIVAL + abs(self.floors_waiting[-1]["floor"] - floor) * global_vars.FLOOR_ELEVATOR_TRAVEL_TIME
        
        elif not self.free:
            return self.arrival_time + global_vars.WAITING_TIME_FOR_ELEVATOR_ARRIVAL + abs(self.target_floor - floor) * global_vars.FLOOR_ELEVATOR_TRAVEL_TIME
        
        else:
            return abs(self.current_floor - floor) * global_vars.FLOOR_ELEVATOR_TRAVEL_TIME
