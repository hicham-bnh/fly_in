from graphic import DroneSimulation
from algo import BFS
import sys


if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            print("Usage: python main.py maps/ma_map.txt")
            sys.exit(1)
        bfs = BFS()
        bfs.parse_file(sys.argv[len(sys.argv) - 1])
        bfs.parser.check_line()
        bfs.parser.parse()
        bfs.get_path()
        graph = DroneSimulation(bfs.get_path_all_drone())
        graph.run()
    except BaseException as e:
        print(e)


