# Elevators Simulation

This project simulates a building with elevators using the Pygame library. It includes the functionality for managing elevator movements, handling user input, and rendering the building and elevators.

## Files Overview

### `building_factory.py`

Contains the interface definitions for buildings and building factories:

- `IBuilding`: An abstract base class for buildings with methods `call_to_elevator` and `update`.
- `IBUildingFactory`: An abstract base class for building factories with a method `create_building`.

### `manager.py`

Manages the game, including screen setup, building initialization, event handling, and the game loop:

- `Manager`: Initializes the game, creates buildings, checks for floor button clicks, updates the game state, and draws the buildings and elevators.

###  `building`

- `Building`: The Building class represents a building with multiple floors and elevators.

### `elevator.py`

Defines the elevator class with its functionalities:

- `Elevator`: Represents an elevator, including methods to add tasks, start tasks, update state and location, handle arrival, and calculate movement time.

### `floor`

- `Floor`: The Floor class represents a floor in a building.

### `button.py`

Defines a clickable button class:

- `Button`: Represents a clickable button with a number displayed on it.

### `line.py`

Defines a line class used to visually separate floors in the building:

- `Line`: Represents a line to separate floors.

### `global_vars.py`

Contains global variables used throughout the game:

- Screen dimensions, colors, button configurations, elevator travel times, and building configurations.

### `main.py`

The main entry point for the game, containing the main game loop:

- `main()`: Initializes the game manager, runs the game loop, handles events, updates the game state, and renders the screen.

## Getting Started

### Prerequisites

- Python 3.x
- Pygame library

### Installation

1. Clone the repository:
    \```
    git clone <https://github.com/aharonlif/elevator.git>
    cd <elevator>
    \```

2. Install the required dependencies:
    \```
    pip install pygame
    \```

### Running the Simulation

1. Navigate to the project directory.
2. Run the main script:
    \```
    python main.py
    \```

## Usage

- The simulation window will display multiple buildings with elevators.
- Click on the floor buttons to call an elevator to that floor.
- The elevators will move to the requested floors and play a sound upon arrival.

## Controls
- Click on the floor buttons to call the elevator to the respective floor.
- Press Q to quit the game.
- Enjoy the simulation!