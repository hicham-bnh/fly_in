from parsing import Parsing
from algo import BFS
from graphic import Graphic
import sys


if __name__ == "__main__":
    try:
        if (len(sys.argv) > 0):
            file = sys.argv[len(sys.argv) - 1]
            parse: Parsing = Parsing(file)
        else:
            file = input("path to maps :")
            parser = Parsing(file)
        algo: BFS = BFS(file)
        graph: Graphic = Graphic(parse.pos, parse.zones)
        max_len: int = 0
        algo.parse_file()
        algo.build_adj()
        graph.generate_world()
        graph.generate_map()
        graph.generate_hub_labels()
        graph.generate_drone(parse.nb_drones)
        graph.generat_connections(parse.connections)
        result = algo.path_for_drone()
        graph.assign_paths_from_data(result, speed=3.5)
        for res in result:
            if len(res['path']) > max_len:
                max_len = len(res['path'])
        for i in range(1, max_len):
            for res in result:
                if len(res['path']) > i:
                    print(f"{res['id']}-{res['path'][i]}", end=' ')
            print()
        print(f"number of turn : {i}")
        graph.run()
    except BaseException as e:
        print(e)
