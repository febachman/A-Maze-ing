#!/usr/bin/env python3

import sys
from typing import Tuple
from config_parser import read_config
from maze_generator import MazeGenerator
from maze_solver import MazeSolver
from output import maze_hex, write_output
from display import build_ascii_grid, print_maze


def main() -> None:
    # 1. arg validation
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: python3 a_maze_ing.py <config.txt>\n")
        sys.exit(1)

    config_path: str = sys.argv[1]

    # 2. reading and parsing
    try:
        config = read_config(config_path)
    except FileNotFoundError:
        sys.stderr.write(
            f"Error: Configuration file '{config_path}' not found.\n"
        )
        sys.exit(1)
    except Exception as e:
        sys.stderr.write(f"Error reading configuration file: {e}\n")
        sys.exit(1)

    width: int = config.get("WIDTH", 0)
    height: int = config.get("HEIGHT", 0)
    entry_raw = config.get("ENTRY")
    exit_raw = config.get("EXIT")
    output_file: str = config.get("OUTPUT_FILE", "maze.txt")

    try:
        if entry_raw is None or exit_raw is None:
            raise ValueError("Missing ENTRY or EXIT key")
        entry: Tuple[int, int] = (int(entry_raw[0]), int(entry_raw[1]))
        exit_pos: Tuple[int, int] = (int(exit_raw[0]), int(exit_raw[1]))
    except (IndexError, TypeError, ValueError):
        sys.stderr.write(
            "Error: ENTRY or EXIT coordinates are missing or invalid.\n"
        )
        sys.exit(1)

    # validation entry and exit
    if not (0 <= entry[0] < width and 0 <= entry[1] < height):
        sys.stderr.write(
            f"Error: ENTRY coordinates {entry} are "
            f"outside maze bounds ({width}x{height}).\n"
        )
        sys.exit(1)

    if not (0 <= exit_pos[0] < width and 0 <= exit_pos[1] < height):
        sys.stderr.write(
            f"Error: EXIT coordinates {exit_pos} are "
            f"outside maze bounds ({width}x{height}).\n"
        )
        sys.exit(1)

    if entry == exit_pos:
        sys.stderr.write(
            "Error: ENTRY and EXIT coordinates must be different.\n"
        )
        sys.exit(1)

    # 3. maze generator
    try:
        generator = MazeGenerator(width=width, height=height)
        generator.generate_maze(entry)
    except Exception as e:
        sys.stderr.write(f"Error generating maze: {e}\n")
        sys.exit(1)

    # 4. path solver (bfs)
    try:
        solver = MazeSolver(generator)
        path = solver.path_solver(entry, exit_pos)

        if path is None:
            sys.stderr.write(
                "Error: No valid path found between ENTRY and EXIT.\n"
            )
            sys.exit(1)

        directions = solver.path_directions(path)
    except Exception as e:
        sys.stderr.write(f"Error solving maze: {e}\n")
        sys.exit(1)

    # export hex
    try:
        hex_grid = maze_hex(generator.grid)
        write_output(output_file, hex_grid, entry, exit_pos, directions)
        print(f"Maze successfully generated and written to '{output_file}'.")
    except Exception as e:
        sys.stderr.write(f"Error writing output file '{output_file}': {e}\n")
        sys.exit(1)

    # 6. visual ASCII
    try:
        print("\n--- Maze Render ---")
        ascii_grid = build_ascii_grid(
            generator.grid, width, height, entry, exit_pos
        )
        print_maze(ascii_grid)
    except Exception as e:
        sys.stderr.write(f"Error displaying maze: {e}\n")


if __name__ == "__main__":
    main()
