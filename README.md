# Snake

## Description

This is a **Snake** game implemented in Python using the Pygame library. The game includes the following features:

- A grid-based layout for the game field.
- A snake that grows in length when it eats an apple.
- Basic game mechanics like snake movement and apple spawning.
- An optional AI mode for automated snake movement.

## Installation

To run the Snake game, you need to have both Python and Pygame installed on your computer.

1. **Install Python**: Download and install the latest version of Python from the official [Python website](https://www.python.org/downloads/).

2. **Install Pygame**: Use `pip` to install Pygame by running the following command in your terminal or command prompt:

```
pip install pygame
```

## Running the Game

1. **Clone the Repository**: clone this repository to your local machine using the following command:

```
git clone https://github.com/JaimeZepeda08/Snake.git
```

> OR download the project files from my [website](https://jaimezepeda.vercel.app/projects)

2. **Navigate to the Directory**: change to the directory containing the game code:

```
cd Snake
```

3. **Run the Game**: execute the main python file to play the game:

```
python3 main.py
```

## Controls

`Up Arrow`: Move the snake up

`Down Arrow`: Move the snake down

`Left Arrow`: Move the snake to the left

`Right Arrow`: Move the snake to the right

`Spacebar`: Activate AI mode (the snake will move automatically towards the apple)

## Game Features

### Grid

The game grid consists of a layout where the snake moves and apples spawn. The grid is managed by the `Grid` class, which handles the placement of the snake, spawning apples, and drawing the game field.

### Snake

The snake starts with a length of 1 and grows longer each time it eats an apple. The `Snake` class manages the snake's movement, growth, and interaction with the grid.

### Apples

Apples randomly spawn on the grid. When the snake eats an apple, it grows in length, and a new apple spawns at a different location.

### AI Mode

The game includes an AI mode that can be activated by pressing the spacebar. The AI uses the A\* pathfinding algorithm to find the shortest path to the apple.

## Game Over

The game ends when the snake collides with itself or the edges of the grid. The final score is based on the length of the snake.

## Possible Improvements

- Displaying score on the screen
- Implementing a different algorithm for more complex movement strategies
- Make the AI snake follow a _Hamiltonian Cycle_
