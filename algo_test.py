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
    
    def is_path_to_goal(self, start_node: str, goal_node: str) -> bool:
        queue = deque([start_node])
        visited = {start_node}
        
        while queue:
            curr = queue.popleft()
            if curr == goal_node:
                return True
            for neighbor in self.adj.get(curr, []):
                zone_obj = next((z for z in self.hub if z['name'] == neighbor), None)
                if neighbor not in visited and "dead" not in neighbor and zone_obj['zone'] != "blocked":
                    visited.add(neighbor)
                    queue.append(neighbor)
        return False

    def get_path(self, drone) -> None:
        positions = {z['name']: z for z in self.hub}
        positions[self.parser.end[0][0]]['capacity'] = self.parser.nb_drones
        ordre_zones = {"priority": 0, "normal": 1, "restricted": 2}
        current_pos = drone['path'][-1]
        if current_pos == self.parser.end[0][0]:
            return
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
            if self.is_path_to_goal(pos, self.parser.end[0][0]):
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
        print(drones)
        return drones



if __name__ == "__main__":
        test = BFS()
        test.parse_file(sys.argv[len(sys.argv) - 1])
        test.path_for_drone()
