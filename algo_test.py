from parsing import Parsing
from typing import List, Optional, Dict
from collections import deque
import sys


class BFS:
    def __init__(self) -> None:
        self.parser = Parsing()
        self.start: List[tuple[str, int, int]] = []
        self.end: List[tuple[str, int, int]] = []
        self.path: List[str] = []
        self.adj = {}

    def parse_file(self, file: str) -> None:
        self.parser.read_file(file)
        self.parser.check_line()
        self.parser.parse()
        self.parser.check_start_end()
        self.start = self.parser.start
        self.end = self.parser.end
        self.connection = self.parser.connections
        self.adj = self.build_adj()

    def build_adj(self):
        adj = {}
        for zone in self.parser.zones:
            adj[zone['name']] = []
        for z1, z2 in self.parser.connections:
            name1 = z1['name']
            nmae2 = z2['name']
            adj[name1].append(z2)
            adj[nmae2].append(z1)
        return adj

    def get_path(self, drone: Dict, name):
        current = drone[name]
        last = current[-1]
        if last == 'goal' or last == "impossible_goal":
            return
        queue = deque()
        if last in self.adj:
            voisins = self.adj[last]
            for voisin in voisins:
                if voisin['zone'] == "blocked":
                    continue
                if voisin['zone'] == "restricted":
                    queue.append(voisin['name'])
                else:
                    queue.appendleft(voisin['name'])
        while queue:
            current = queue.popleft()
            break


    def get_path_drone(self):
        zones = {x['name']: x for x in self.parser.zones}
        all_arrived = 0
        while all_arrived < self.parser.nb_drones:
            for drone_dict in self.parser.drone_path:
                name = list(drone_dict.keys())[0]
                self.get_path(drone_dict, name)
            break



if __name__ == "__main__":
    try:
        test = BFS()
        test.parse_file(sys.argv[len(sys.argv) - 1])
        test.get_path_drone()
    except Exception as e:
        print(e)