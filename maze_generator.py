#!/usr/bin/env python3

import typing
import random


class MazeGenerator:
    """Handles the creation and basic structure of the maze grid."""

    NORTH: int = 1
    EAST: int = 2
    SOUTH: int = 4
    WEST: int = 8

    OPPOSITES = {
        NORTH: SOUTH,
        EAST: WEST,
        SOUTH: NORTH,
        WEST: EAST,
    }

    MOVEMENTS = {
        NORTH: (0, -1),
        EAST: (1, 0),
        SOUTH: (0, 1),
        WEST: (-1, 0),
    }

    def __init__(
        self,
        width: int,
        height: int,
        seed: typing.Optional[int] = None,
        perfect: bool = False
    ) -> None:
        self.width: int = width
        self.height: int = height
        self.seed: typing.Optional[int] = seed
        self.perfect: bool = perfect
        self.randomizer = random.Random(seed)
        self._init_grid()

    def _init_grid(self) -> None:
        self.grid = [
            [15 for _ in range(self.width)] for _ in range(self.height)
        ]
        self.visited = [
            [False for _ in range(self.width)] for _ in range(self.height)
        ]

    def get_cell(self, x: int, y: int) -> typing.Optional[int]:
        """Return the cell value or None if the coordinates are invalid."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None

    def remove_wall(self, x: int, y: int, direction: int) -> bool:
        """Remove a wall between a cell and its neighbor."""
        if self.get_cell(x, y) is None:
            return False

        if direction not in self.OPPOSITES:
            return False

        dx, dy = self.MOVEMENTS[direction]
        nx = x + dx
        ny = y + dy

        if self.get_cell(nx, ny) is None:
            return False

        self.grid[y][x] &= ~direction
        self.grid[ny][nx] &= ~self.OPPOSITES[direction]

        return True

    def _get_unvisited_neighbors(
        self,
        x: int,
        y: int
    ) -> typing.List[typing.Tuple[int, int, int]]:
        """Return a list of valid, unvisited neighbors."""
        neighbors = []
        for direction, (dx, dy) in self.MOVEMENTS.items():
            nx = x + dx
            ny = y + dy
            if self.get_cell(nx, ny) is not None and not self.visited[ny][nx]:
                neighbors.append((direction, nx, ny))
        return neighbors

    def _apply_42_mask(self) -> None:
        """Set 42 area as visited to isolate from algorithm"""
        shape_42 = [
            "X   XXX",
            "X     X",
            "XXX XXX",
            "  X X  ",
            "  X XXX"
        ]
        center_y: int = self.height // 2
        center_x: int = self.width // 2
        start_y: int = center_y - (len(shape_42) // 2)
        start_x: int = center_x - (len(shape_42[0]) // 2)

        for i, row in enumerate(shape_42):
            for j, char in enumerate(row):
                curr_y = start_y + i
                curr_x = start_x + j
                if 0 <= curr_y < self.height and 0 <= curr_x < self.width:
                    if char == "X":
                        self.visited[curr_y][curr_x] = True

    def generate_maze(self, start_cell: typing.Tuple[int, int]) -> None:
        """Generate a maze using iterative backtracking"""

        self._apply_42_mask()

        stack = [start_cell]
        self.visited[start_cell[1]][start_cell[0]] = True

        while stack:
            x, y = stack[-1]
            neighbors = self._get_unvisited_neighbors(x, y)

            if neighbors:
                direction, nx, ny = self.randomizer.choice(neighbors)
                self.remove_wall(x, y, direction)
                self.visited[ny][nx] = True
                stack.append((nx, ny))
            else:
                stack.pop()

    def display_debug(self) -> None:
        """Display the maze grid for debugging"""
        for row in self.grid:
            print(row)
