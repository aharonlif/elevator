from manager import Manager

def main():
    """
    Main function to initialize the Manager with a given number of buildings, 
    floors, and elevators, and start the simulation.
    """
    # TODO: Generate random number of buildings, floors, and elevators
    buildings = [{"floors": 5, "elevators" : 3},
                 {"floors": 3, "elevators" : 1},
                 {"floors": 4, "elevators" : 2},
                 {"floors": 6, "elevators" : 3}]
    floors = 6
    elevators = 3
    manager = Manager(buildings=buildings, floors=floors, elevators=elevators)
    manager.run()

if __name__ == "__main__":
    """
    Entry point for the program. Calls the main function.
    """
    main()