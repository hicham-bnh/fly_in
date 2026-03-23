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
        self.arrived = 0

    def parse_file(self, file: str) -> None:
        self.parser.read_file(file)
        self.parser.check_line()
        self.parser.parse()
        self.parser.check_start_end()
        self.start = self.parser.start
        self.end = self.parser.end
        self.connection = self.parser.connections
        self.hub = self.parser.zones
        self.adj = self.build_adj()

    def build_adj(self):
        adj = {}
        for zone in self.parser.zones:
            adj[zone['name']] = []
        for z1, z2 in self.parser.connections:
            name1 = z1['name']
            name2 = z2['name']
            if name1 == "start":
                adj[name1].append(z2['name'])
            else:
                adj[name1].append(z2['name'])
                adj[name2].append(z1['name'])
        return adj

    def get_path(self, drone) -> None:
        positions = {z['name']: z for z in self.hub}
        positions[self.parser.end[0][0]]['capacity'] = self.parser.nb_drones
        ordre_zones = {"priority": 0, "normal": 1, "restricted": 2}
        current_pos = drone['path'][-1]
        voisins = self.adj[current_pos]
        maybe = deque()
        for voisin in voisins:
            current_voisin = next(filter(
                lambda x: x['name'] == voisin, self.hub), None
                )
            if current_voisin['zone'] == "blocked" or "dead" in current_voisin['name']:
                continue
            else:
                maybe.append(current_voisin)
        voisins_final = deque(sorted(
            maybe,
            key=lambda x: (ordre_zones.get(x['zone'], 3), x['name'])
        ))
        queu = deque(node['name'] for node in voisins_final)
        while queu:
            pos = queu.popleft()
            if pos == self.parser.end[0][0] and pos in drone['visited']:
                break
            if positions[pos]['capacity'] == positions[pos]['drone']:
                continue
            if pos in drone['visited']:
                continue
            else:
                positions[pos]['drone'] += 1
                drone['visited'].append(pos)
                positions[current_pos]['drone'] -= 1
                drone['path'].append(pos)
                if pos == self.parser.end[0][0]:
                    self.arrived += 1
                return
        drone['path'].append(current_pos)


    def path_for_drone(self):
        drones = self.parser.drone_path
        while self.arrived < self.parser.nb_drones:
            for drone in drones:
                self.get_path(drone)
        for drone in drones:
            print(drone['path'])
        return drones



if __name__ == "__main__":
    try:
        test = BFS()
        test.parse_file(sys.argv[len(sys.argv) - 1])
        test.path_for_drone()
    except Exception as e:
        print(e)