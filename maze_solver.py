#!/usr/bin/env python3

from collections import deque
import typing
from maze_generator import MazeGenerator


class MazeSolver:
    """Handles pathfinding in the maze using BFS"""

    def __init__(self, maze: MazeGenerator) -> None:
        self.maze = maze

    def get_neighbors(
        self, x: int, y: int
    ) -> typing.List[typing.Tuple[int, int, int]]:
        """
        Returns a list of valid neighbor coords and the wall direction to go,
        if no wall exists between current cell and neighbor.
        """
        cell_value = self.maze.get_cell(x, y)
        if cell_value is None:
            return []

        neighbors: typing.List[typing.Tuple[int, int, int]] = []

        # Directions mapping: (dx, dy, wall_bit_to_check, opposite_bit)
        # NORTH = 1, EAST = 2, SOUTH = 4, WEST = 8
        directions = [
            (0, -1, MazeGenerator.NORTH, MazeGenerator.SOUTH),
            (1, 0, MazeGenerator.EAST, MazeGenerator.WEST),
            (0, 1, MazeGenerator.SOUTH, MazeGenerator.NORTH),
            (-1, 0, MazeGenerator.WEST, MazeGenerator.EAST),
        ]

        for dx, dy, wall_bit, _ in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.maze.width and 0 <= ny < self.maze.height:
                # Se o bit da parede NAO estiver ativo, ha passagem livre
                if not (cell_value & wall_bit):
                    neighbors.append((nx, ny, wall_bit))

        return neighbors

    def path_solver(
        self,
        start: typing.Tuple[int, int],
        exit_pos: typing.Tuple[int, int]
    ) -> typing.Optional[typing.List[typing.Tuple[int, int]]]:
        """
        Finds the shortest path from start to exit using BFS.
        Returns a list of coordinates representing the path,
        or None if no path exists.
        """
        if (
            self.maze.get_cell(start[0], start[1]) is None or
            self.maze.get_cell(exit_pos[0], exit_pos[1]) is None
        ):
            return None

        queue: deque[typing.Tuple[int, int]] = deque([start])
        visited: typing.Set[typing.Tuple[int, int]] = {start}
        parent: typing.Dict[
            typing.Tuple[int, int], typing.Tuple[int, int]
        ] = {}

        path_found = False

        while queue:
            current = queue.popleft()

            if current == exit_pos:
                path_found = True
                break

            cx, cy = current
            for nx, ny, _ in self.get_neighbors(cx, cy):
                neighbor = (nx, ny)
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current
                    queue.append(neighbor)

        if not path_found:
            return None

        # Reconstruct path from exit to start
        path: typing.List[typing.Tuple[int, int]] = []
        current = exit_pos
        while current != start:
            path.append(current)
            current = parent[current]
        path.append(start)
        path.reverse()

        return path

    def path_directions(
        self, path: typing.List[typing.Tuple[int, int]]
    ) -> str:
        """Convert a coordinate path into N/E/S/W directions."""
        directions = []

        for i in range(len(path) -1):
            x1, y1 = path[i]
            x2, y2 = path[i + 1]
        
        if x2 == x1 + 1:
            directions.append("E")
        elif x2 == x1 - 1:
            directions.append("W")
        elif y2 == y1 + 1:
            directions.append("S")
        elif y2 == y1 - 1:
            directions.append("N")
        else:
            raise ValueError("Invalid path: cells are not adjacent")

        return "".join(directions)

if __name__ == "__main__":
    gen = MazeGenerator(width=5, height=5)
    solver = MazeSolver(gen)

    path = solver.path_solver((0, 0), (4, 4))
    print("Path found (expected None):", path)

    if path is not None:
        directions = solver.path_to_directions(path)
        print("Directions:", directions)
