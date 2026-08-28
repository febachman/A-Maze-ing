#!/usr/bin/env python3

import typing
from maze_generator import MazeGenerator
from maze_solver import MazeSolver
from config_parser import read_config


def cell_hex(cell: int) -> str:
    """Convert a cell wall value to one hexadecimal digit."""
    if not 0 <= cell <= 15:
        raise ValueError("Cell value must be between 0 and 15.")
    return format(cell, "X")


def row_hex(row: typing.List[int]) -> str:
    """Convert one maze row to hexadecimal."""
    return "".join(cell_hex(cell) for cell in row)


def maze_hex(
    grid: typing.List[typing.List[int]]
) -> typing.List[str]:
    """Convert the complete maze grid to hexadecimal rows."""
    return [row_hex(row) for row in grid]


def write_output(
    filename: str,
    hex_grid: typing.List[str],
    entry: typing.Tuple[int, int],
    exit_pos: typing.Tuple[int, int],
    path_directions: str
) -> None:
    """Write maze and solution data to the output file"""

    with open(filename, "w") as file:
        for row in hex_grid:
            file.write(row + "\n")

        file.write("\n")
        file.write(f"{entry[0]},{entry[1]}\n")
        file.write(f"{exit_pos[0]},{exit_pos[1]}\n")
        file.write(path_directions + "\n")


if __name__ == "__main__":
    config = read_config("config.txt")

    generator = MazeGenerator(
        width=config["WIDTH"],
        height=config["HEIGHT"]
    )

    generator.generate_maze(config["ENTRY"])

    solver = MazeSolver(generator)

    path = solver.path_solver(
        config["ENTRY"],
        config["EXIT"]
    )

    if path is None:
        raise ValueError("No valid path found between entry and exit.")

    directions = solver.path_directions(path)

    hex_grid = maze_hex(generator.grid)

    write_output(
        config["OUTPUT_FILE"],
        hex_grid,
        config["ENTRY"],
        config["EXIT"],
        directions
    )

    print(f"Maze written to {config['OUTPUT_FILE']}.")
