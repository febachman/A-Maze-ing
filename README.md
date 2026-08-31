*This project has been created as part of the 42 curriculum by fbachman & made-luc*

# A-Maze-ing

## Description

**A-Maze-ing** is an academic project developed at **42** that explores maze generation, pathfinding, randomness, and graph-based algorithms.

The project generates a maze from a configuration file, finds a path between a defined entry and exit, displays the maze in the terminal, and exports the generated maze and its solution to an output file.

Two different maze-generation modes are available:

- **Perfect maze (`PERFECT=True`)**: generates a maze based on a single connected structure where there is one unique path between two cells.
- **Pac-Man-like maze (`PERFECT=False`)**: generates a fully connected maze with loops and a small number of dead ends, making it more suitable for a Pac-Man-like game where alternative routes are required.

The project also contains a reusable maze generator and solver, allowing the generation and pathfinding logic to remain independent from the user interface.

The main algorithms used are:

- **DFS (Depth-First Search)** with iterative backtracking for maze generation.
- **BFS (Breadth-First Search)** for finding the shortest path between the entry and exit.

The project also makes use of randomness and optional seeds so that maze generation can either be reproducible or different on each execution.

## Instructions

### Requirements

The project requires:

- Python 3
- A terminal capable of displaying the generated maze
- Git (optional, for version control)

No external Python packages are required by the project.

### Execution

The program is launched with a configuration file:

```bash
python3 a_maze_ing.py config.txt
```

After the maze is generated and solved, it is displayed in the terminal and the corresponding output file is created.

# Interactive Menu
Once the maze is displayed, the program provides the following menu:
1. Generate new maze: Generates another maze using the same dimensions, entry, exit, and generation mode (seed=None is used).
2. Show/Hide path: Toggles the visualization of the shortest path between the entry and exit calculated using BFS.
3. Change wall colors: Cycles through the available wall-color states used by the terminal display.
4. Exit: Terminates the program.

# Configuration File
FormatThe program receives its configuration through a text file. The configuration determines the maze dimensions, entry and exit positions, output file, generation mode, and optional random seed.
A configuration file contains the following parameters:

Ini, TOML
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=False
SEED=42

# Configuration Parameters
Table
ParameterDescriptionWIDTHWidth of the maze in cells.HEIGHTHeight of the maze in cells.ENTRYCoordinates of the maze entry in x,y format.EXITCoordinates of the maze exit in x,y format.OUTPUT_FILEName of the file where the generated maze is exported.PERFECTSelects the maze generation mode (True for perfect, False for Pac-Man-like).SEEDOptional integer used to initialize the random number generator.

# Technical Choices & Algorithm Selection
## Maze Generation Algorithm
- Chosen Algorithm: DFS with Iterative Backtracking
- Reason for Choice: DFS naturally produces a connected path structure while remaining simple to implement without relying on Python's recursive call stack. Graph-theoretically, a perfect maze maps directly to a spanning tree where there is exactly one path between any two vertices
- Randomized DFS: Combining DFS with self.randomizer.choice(neighbors) introduces randomness to select unvisited neighbors, producing diverse layouts while maintaining connectivity.

## Maze Solver Algorithm
- Chosen Algorithm: Breadth-First Search (BFS).
- Reason for Choice: In an unweighted grid where every step shares an identical cost, BFS guarantees that the first time the destination is reached, the path found contains the absolute minimum number of moves.

## Reusable Maze Generator Module
### Module Overview
The MazeGenerator class is designed as a reusable component independent of the terminal interface.
### Core Responsibilities
- Creating the initial grid and managing cell/wall bit-values.
- Handling wall removal and restoration, plus the 42 mask pattern.
- Managing perfect maze generation, loop insertion, and dead-end reduction.

### Main Methods
- get_cell(x, y): Returns the value of a cell or None when coordinates are outside the maze
- remove_wall(x, y, direction): Removes a wall between a cell and its valid neighbor and updates both cells.
- _gen_perfect_maze(start_cell): Generates the maze using randomized DFS with iterative backtracking
- _add_loops(): Adds loops to the non-perfect mode while checking the 3x3 constraint.
- _reduce_dead_ends(): Attempts to reduce the number of dead ends while preserving maze validity
- is_masked(x, y): Checks whether a cell belongs to the 42 pattern.
- generate_maze(start_cell, exit_cell): Coordinates the generation process according to the selected PERFECT mode.

# Team and Project Management
## Team Roles & Division of Responsibilities
Developed collaboratively by a two-member team.
- Team Member 1: Mainly responsible for the configuration parser, terminal display, and box-drawing visualization.
- Team Member 2: Mainly responsible for the BFS and DFS algorithms, maze generation (PERFECT=True and PERFECT=False modes), solver, and output generation
- Joint Responsibilities: Consolidation and integration in a_maze_ing.py, architecture discussions, testing, and debugging.

## Anticipated Planning & Evolution
The project was implemented incrementally:
1. Configuration Parser: Establish the format and validation of the configuration file.
2. Maze Matrix Structure: Build the internal representation of the maze (PERFECT=True).
3. Maze Solver: Implement BFS and establish pathfinding between entry and exit.
4. Output: Convert the internal maze representation to hexadecimal and generate the output file
5. Display: Add the terminal visualization of the generated maze, path, and wall colors.
6. Non-perfect Generation: Implement loops and dead-end reduction for Pac-Man-like requirements
7. Interactive Menu: Integrate generation, visualization, and user interaction into the final application.

## Reflection on Development
- What Worked Well: Modular architecture worked well because each major responsibility could be developed and tested independently. Separating generation from solving made algorithms easier to reason about. Using a dedicated random generator allowed seeds to be used for reproducibility. Hexadecimal representation provided a compact output format.
- What Could Be Improved: The integration phase could have been planned earlier and more continuously to preempt edge-case issues.

# Tools Used
- Terminal: Running the application, testing configurations, and debugging behavior.
- Visual Studio Code: Writing, organizing, and reviewing the source code.
- GitHub: Version control, collaboration, and project management.
- Python 3: Implementation language (random, typing, collections.deque, sys, os).

# Resources & AI Usage
## External References
- Breadth-First Search (BFS): IME USP Graph Algorithms — Applied to graph traversal and shortest-path behavior in an unweighted graph (maze_solver.py). (https://www.ime.usp.br/~pf/algoritmos_para_grafos/aulas/bfs.html)
- Depth-First Search (DFS): IME USP Graph Algorithms — Used to understand DFS and its application to the maze-generation algorithm.(https://www.ime.usp.br/~pf/algoritmos_para_grafos/aulas/dfs.html)
- BFS vs DFS: GeeksforGeeks Difference Between BFS and DFS — Useful for comparing characteristics and understanding why the different algorithms have different roles. (https://www.geeksforgeeks.org/dsa/difference-between-bfs-and-dfs/)

## AI Usage Details
Artificial intelligence served as a support tool during development:
- Documentation: Helping structure and write project documentation, including this README.
- Debugging Assistance: Helping identify possible issues and reason about unexpected behavior
- Algorithm Explanations: Providing explanations and comparisons of concepts such as DFS, BFS, backtracking, graph connectivity, and shortest-path algorithms.
The team remained responsible for understanding algorithms, adapting the implementation to project requirements, and validating the resulting behavior.