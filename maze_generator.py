#!/usr/bin/env python3

class MazeGenerator:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        # Inicializa cada célula com 15 (1+2+4+8), ou seja, todas as paredes fechadas
        self.grid = [[15 for _ in range(width)] for _ in range(height)]

    def get_cell(self, x: int, y: int):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None

    def display_debug(self):
        """Apenas para você visualizar no terminal durante o desenvolvimento."""
        for row in self.grid:
            print(row)

# Como você não precisa do parser agora:
if __name__ == "__main__":
    maze = MazeGenerator(width=5, height=5)
    print("Grid 5x5 inicializado com valor 15 (paredes fechadas):")
    maze.display_debug()
