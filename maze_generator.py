#!/usr/bin/env python3

import typing

class MazeGenerator:
    """Handles the creation and basic structure of the maze grid."""
    
    NORTH: int = 1
    EAST: int = 2
    SOUTH: int = 4
    WEST: int = 8

    def __init__(self, width: int, height: int) -> None:
        self.width: int = width
        self.height: int = height
        self.grid = [[15 for _ in range(width)] for _ in range(height)]

    def get_cell(self, x: int, y: int) -> typing.Optional[int]:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None

    def display_debug(self):
        # Apenas para visualizar no terminal durante o desenvolvimento.
        for row in self.grid:
            print(row)


if __name__ == "__main__":
    maze = MazeGenerator(width=5, height=5)
    print("Grid 5x5 inicializado com valor 15 (paredes fechadas):")
    maze.display_debug()
