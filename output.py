if __name__ == "__main__":
    from maze_generator import MazeGenerator
    from config_parser import read_config

    config = read_config("config.txt")

    generator = MazeGenerator(
        width=config["WIDTH"],
        height=config["HEIGHT"]
    )

    generator.generate_maze((0, 0))

    print("\n##### A-MAZE-ING #####\n")
    generator.display_debug()
