#!/usr/bin/env python3

import typing


def build_ascii_grid(
    maze_grid: typing.List[typing.List[int]],
    width: int,
    height: int,
    entry_coords: typing.Tuple[int, int],
    exit_coords: typing.Tuple[int, int]
) -> typing.List[typing.List[str]]:
    """Builds an maze with walls and empty spaces."""
    NORTH: int = 1
    EAST: int = 2
    SOUTH: int = 4
    WEST: int = 8
    expanded_grid: typing.List[typing.List[str]] = [
        ["#" for _ in range(width * 2 + 1)] for _ in range(height * 2 + 1)
    ]
    for y in range(height):
        for x in range(width):
            cell_value: int = maze_grid[y][x]

            grid_x: int = x * 2 + 1
            grid_y: int = y * 2 + 1

            expanded_grid[grid_y][grid_x] = " "

            if not (cell_value & NORTH):
                expanded_grid[grid_y - 1][grid_x] = " "

            if not (cell_value & EAST):
                expanded_grid[grid_y][grid_x + 1] = " "

            if not (cell_value & SOUTH):
                expanded_grid[grid_y + 1][grid_x] = " "

            if not (cell_value & WEST):
                expanded_grid[grid_y][grid_x - 1] = " "

    shape_42 = [
        "# # ###",
        "# #   #",
        "### ###",
        "  # #  ",
        "  # ###"
    ]
    center_y: int = len(expanded_grid) // 2
    center_x: int = len(expanded_grid[0]) // 2
    start_y: int = center_y - (len(shape_42) // 2)
    start_x: int = center_x - (len(shape_42[0]) // 2)
    for i, row_shape in enumerate(shape_42):
        for j, char in enumerate(row_shape):
            curr_y = start_y + i
            curr_x = start_x + j
            if (
                0 < curr_y < len(expanded_grid) - 1
                and 0 < curr_x < len(expanded_grid[0]) - 1
            ):
                if char == "#":
                    expanded_grid[curr_y][curr_x] = "@"
                elif char == " ":
                    expanded_grid[curr_y][curr_x] = " "
    ex, ey = entry_coords
    expanded_grid[ey * 2 + 1][ex * 2 + 1] = "E"
    xx, xy = exit_coords
    expanded_grid[xy * 2 + 1][xx * 2 + 1] = "X"

    return expanded_grid


def print_maze(grid: typing.List[typing.List[str]]) -> None:
    """Prints the maze grid using Box-Drawing characters"""
    WALL_COLOR: str = "\033[38;5;33m"
    SPECIAL_COLOR: str = "\033[38;5;135m"
    RESET_COLOR: str = "\033[0m"

    BOX_CHARS = set("■│─└┌├┘┴┐┤┬┼")
    CONNECTS_RIGHT = set("─└┌├┴┬┼")
    for row in grid:
        rendered_row: str = ""
        for char in row:
            if char in BOX_CHARS:
                padding = "─" if char in CONNECTS_RIGHT else " "
                rendered_row += f"{WALL_COLOR}{char}{padding}{RESET_COLOR}"
            elif char == "@":
                rendered_row += f"{SPECIAL_COLOR}@@{RESET_COLOR}"
            elif char == " ":
                rendered_row += "  "
            elif char == "E":
                rendered_row += f"\033[38;5;46mE {RESET_COLOR}"
            elif char == "X":
                rendered_row += f"\033[38;5;196mX {RESET_COLOR}"
            else:
                rendered_row += str(char) + " "
        print(rendered_row)


def convert_to_box_drawing(
        grid: typing.List[typing.List[str]]
) -> typing.List[typing.List[str]]:
    BOX_CHARS_DICT = {
        0: '■',  1: '│',  2: '─',  3: '└',
        4: '│',  5: '│',  6: '┌',  7: '├',
        8: '─',  9: '┘', 10: '─', 11: '┴',
        12: '┐', 13: '┤', 14: '┬', 15: '┼'
    }
    height: int = len(grid)
    width: int = len(grid[0])
    ref_grid = [row[:] for row in grid]
    for y in range(height):
        for x in range(width):
            if ref_grid[y][x] == "#":
                mask: int = 0
                if y > 0 and ref_grid[y-1][x] == "#":
                    mask += 1
                if x < width - 1 and ref_grid[y][x+1] == "#":
                    mask += 2
                if y < height - 1 and ref_grid[y+1][x] == "#":
                    mask += 4
                if x > 0 and ref_grid[y][x-1] == "#":
                    mask += 8
                grid[y][x] = BOX_CHARS_DICT[mask]
    return grid
