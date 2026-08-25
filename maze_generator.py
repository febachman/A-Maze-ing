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

    def remove_wall(self, x: int, y: int, direction: int) -> bool:
        if self.get_cell(x, y) is None:
            return False
        # dicionário de opostos ~relação parede com parede
        # ex se remover a parece north de uma célula
        # precisa remover a parede south da célula de cima
        opposites = {
            self.NORTH: self.SOUTH,
            self.EAST: self.WEST,
            self.SOUTH: self.NORTH,
            self.WEST: self.EAST,
        }
        # dicionário de movimentos ~relação direção com coordenada
        # para qual célula vou se seguir nessa direção
        movements = {
            self.NORTH: (0, -1),
            self.EAST: (1, 0),
            self.SOUTH: (0, 1),
            self.WEST: (-1, 0),
        }

        if direction not in opposites:
            return False

        dx, dy = movements[direction]
        nx = x + dx
        ny = y + dy

        if self.get_cell(nx, ny) is None:
            return False

        self.grid[y][x] &= ~direction
        self.grid[ny][nx] &= ~opposites[direction]

        return True

    def display_debug(self) -> None:
        # Apenas para visualizar no terminal durante o desenvolvimento.
        for row in self.grid:
            print(row)


if __name__ == "__main__":
    maze = MazeGenerator(width=5, height=5)
    maze.remove_wall(0, 0, MazeGenerator.EAST)
    maze.display_debug()
