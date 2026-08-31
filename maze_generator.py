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
        self.masked = [
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

    def _restore_wall(self, x: int, y: int, direction: int) -> None:
        """Restore a wall between a cell and its neighbor."""
        dx, dy = self.MOVEMENTS[direction]
        nx = x + dx
        ny = y + dy

        self.grid[y][x] |= direction
        self.grid[ny][nx] |= self.OPPOSITES[direction]

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
                        self.masked[curr_y][curr_x] = True

    def is_masked(self, x: int, y: int) -> bool:
        """Return True if the cell belongs to the 42 pattern."""
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False
        return self.masked[y][x]

    def _gen_perfect_maze(self, start_cell: typing.Tuple[int, int]) -> None:
        """Generate a perfect maze using iterative backtracking"""
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

    def _possible_loop(self) -> typing.List[typing.Tuple[int, int, int]]:
        """Return internal walls that can potentially be removed."""
        walls: typing.List[typing.Tuple[int, int, int]] = []

        for y in range(self.height):
            for x in range(self.width):
                if self.is_masked(x, y):
                    continue
                # East wall
                if x + 1 < self.width:
                    if not self.is_masked(x + 1, y):
                        if self.grid[y][x] & self.EAST:
                            walls.append((x, y, self.EAST))

                # South wall
                if y + 1 < self.height:
                    if not self.is_masked(x, y + 1):
                        if self.grid[y][x] & self.SOUTH:
                            walls.append((x, y, self.SOUTH))

        return walls

    def _is_open_between(self, x: int, y: int, direction: int) -> bool:
        """Return True if there is no wall in the given direction."""
        return not bool(self.grid[y][x] & direction)

    def _has_open_3x3(self) -> bool:
        """Return True if the maze contains a fully open 3x3 area."""
        for y in range(self.height - 2):
            for x in range(self.width - 2):
                open_area = True

                for row in range(y, y + 3):
                    for col in range(x, x + 2):
                        if not self._is_open_between(
                            col, row, self.EAST
                        ):
                            open_area = False
                            break
                    if not open_area:
                        break

                if not open_area:
                    continue

                for row in range(y, y + 2):
                    for col in range(x, x + 3):
                        if not self._is_open_between(col, row, self.SOUTH):
                            open_area = False
                            break
                    if not open_area:
                        break

                if open_area:
                    return True

        return False

    def _get_open_directions(self, x: int, y: int) -> typing.List[int]:
        """Return the open directions of a cell."""
        cell = self.get_cell(x, y)

        if cell is None:
            return []

        directions: typing.List[int] = []

        for direction in self.MOVEMENTS:
            if not (cell & direction):
                directions.append(direction)

        return directions

    def _get_dead_ends(self) -> typing.List[typing.Tuple[int, int]]:
        """Return coordinates of cells that have only one open direction."""
        dead_ends: typing.List[typing.Tuple[int, int]] = []

        for y in range(self.height):
            for x in range(self.width):
                if self.is_masked(x, y):
                    continue

                open_directions = self._get_open_directions(x, y)

                if len(open_directions) == 1:
                    dead_ends.append((x, y))

        return dead_ends

    def _add_loops(self) -> None:
        """Add loops while preserving maze validity."""
        walls = self._possible_loop()
        self.randomizer.shuffle(walls)

        loops_added = 0
        target_loops = 2

        for x, y, direction in walls:
            if loops_added >= target_loops:
                break

            self.remove_wall(x, y, direction)

            if self._has_open_3x3():
                self._restore_wall(x, y, direction)
                continue

            loops_added += 1

    def _possible_dead_end(
        self, x: int, y: int
    ) -> typing.List[typing.Tuple[int, int, int]]:
        """Return walls that can be removed from a dead-end."""
        alleys: typing.List[typing.Tuple[int, int, int]] = []

        for direction, (dx, dy) in self.MOVEMENTS.items():
            nx = x + dx
            ny = y + dy

            if not (0 <= nx < self.width and 0 <= ny < self.height):
                continue

            if self.is_masked(nx, ny):
                continue

            if self.grid[y][x] & direction:
                alleys.append((x, y, direction))

        return alleys

    def _reduce_dead_ends(self) -> None:
        """Reduce dead-ends while preserving maze validity."""
        while True:
            dead_ends = self._get_dead_ends()

            if len(dead_ends) <= 2:
                break

            self.randomizer.shuffle(dead_ends)

            changed = False

            for x, y in dead_ends:
                alleys = self._possible_dead_end(x, y)
                self.randomizer.shuffle(alleys)

                for cx, cy, direction in alleys:
                    self.remove_wall(cx, cy, direction)

                    if self._has_open_3x3():
                        self._restore_wall(cx, cy, direction)
                        continue

                    changed = True
                    break

                if changed:
                    break

            if not changed:
                break

    def generate_maze(
        self,
        start_cell: typing.Tuple[int, int],
        exit_cell: typing.Tuple[int, int]
    ) -> None:
        """Generate a maze according to selected mode"""

        self._apply_42_mask()

        s_x, s_y = start_cell
        e_x, e_y = exit_cell

        if self.is_masked(s_x, s_y):
            raise ValueError("Entry cannot be inside the 42 pattern.")

        if self.is_masked(e_x, e_y):
            raise ValueError("Exit cannot be inside the 42 pattern.")

        self._gen_perfect_maze(start_cell)

        if not self.perfect:
            self._add_loops()
            self._reduce_dead_ends()

    def display_debug(self) -> None:
        """Display the maze grid for debugging"""
        for row in self.grid:
            print(row)
