#!/usr/bin/env python3

import typing


def build_ascii_grid(
    maze_grid: typing.List[typing.List[int]],
    width: int,
    height: int,
    entry_coords: typing.Tuple[int, int],
    exit_coords: typing.Tuple[int, int],
    path: typing.Optional[typing.List[typing.Tuple[int, int]]] = None
) -> typing.List[typing.List[str]]:
    """Builds a maze with walls and empty spaces, highlighting 42 cells."""
    NORTH: int = 1
    EAST: int = 2
    SOUTH: int = 4
    WEST: int = 8
    expanded_grid: typing.List[typing.List[str]] = [
        ["#" for _ in range(width * 2 + 1)] for _ in range(height * 2 + 1)
    ]
    shape_42 = [
        "X   XXX",
        "X     X",
        "XXX XXX",
        "  X X  ",
        "  X XXX"
    ]
    start_y = (height // 2) - (len(shape_42) // 2)
    start_x = (width // 2) - (len(shape_42[0]) // 2)

    # 2. build grid
    for y in range(height):
        for x in range(width):
            cell_value: int = maze_grid[y][x]
            grid_x: int = x * 2 + 1
            grid_y: int = y * 2 + 1

            # verify if cell is part of 42
            is_42_cell = False
            if (
                start_y <= y < start_y + len(shape_42)
                and start_x <= x < start_x + len(shape_42[0])
            ):
                if shape_42[y - start_y][x - start_x] == "X":
                    is_42_cell = True

            if is_42_cell:
                expanded_grid[grid_y][grid_x] = "@"
            else:
                expanded_grid[grid_y][grid_x] = " "

            if not (cell_value & NORTH):
                expanded_grid[grid_y - 1][grid_x] = " "
            if not (cell_value & EAST):
                expanded_grid[grid_y][grid_x + 1] = " "
            if not (cell_value & SOUTH):
                expanded_grid[grid_y + 1][grid_x] = " "
            if not (cell_value & WEST):
                expanded_grid[grid_y][grid_x - 1] = " "
    if path:
        for i in range(len(path) - 1):
            x1, y1 = path[i]
            x2, y2 = path[i + 1]

            if (
                expanded_grid[y1 * 2 + 1][x1 * 2 + 1]
                not in ("E", "X", "@")
            ):
                expanded_grid[y1 * 2 + 1][x1 * 2 + 1] = "&"

            mid_x, mid_y = x1 + x2 + 1, y1 + y2 + 1
            if expanded_grid[mid_y][mid_x] not in ("E", "X", "@"):
                expanded_grid[mid_y][mid_x] = "&"

            x_last, y_last = path[-1]
            if (
                expanded_grid[y_last * 2 + 1][x_last * 2 + 1]
                not in ("E", "X", "@")
            ):
                expanded_grid[y_last * 2 + 1][x_last * 2 + 1] = "&"

    ex, ey = entry_coords
    expanded_grid[ey * 2 + 1][ex * 2 + 1] = "E"
    xx, xy = exit_coords
    expanded_grid[xy * 2 + 1][xx * 2 + 1] = "X"

    return expanded_grid


def print_maze(grid: typing.List[typing.List[str]]) -> None:
    """Prints the maze grid using Box-Drawing characters"""
    SPECIAL_COLOR: str = "\033[38;5;135m"
    RESET_COLOR: str = "\033[0m"

    BOX_CHARS = set("■│─└┌├┘┴┐┤┬┼")
    CONNECTS_RIGHT = set("─└┌├┴┬┼")

    color_palette = [196, 202, 208, 214, 220, 118, 46, 51, 33, 21, 57, 135]

    for y, row in enumerate(grid):
        rendered_row: str = ""
        for x, char in enumerate(row):
            color_index = (x + y) % len(color_palette)
            WALL_COLOR = f"\033[38;5;{color_palette[color_index]}m"

            if char in BOX_CHARS:
                padding = "─" if char in CONNECTS_RIGHT else " "
                rendered_row += f"{WALL_COLOR}{char}{padding}{RESET_COLOR}"
            elif char == "&":
                rendered_row += f"\033[38;5;220m✷ {RESET_COLOR}"
            elif char == "@":
                rendered_row += f"{SPECIAL_COLOR}🦄{RESET_COLOR}"
            elif char == " ":
                rendered_row += "  "
            elif char == "E":
                rendered_row += f"\033[38;5;46m🐍{RESET_COLOR}"
            elif char == "X":
                rendered_row += f"\033[38;5;196m🌈{RESET_COLOR}"
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
