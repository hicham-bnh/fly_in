from parsing import Parsing
from typing import List
from collections import deque


class BFS:
    def __init__(self) -> None:
        self.parser = Parsing()
        self.start: List[tuple[str, int, int]] = []
        self.end: List[tuple[str, int, int]] = []
        self.path: List[str] = []
        self.adj = {}
        self.arrived = 0
        self.old = None

    def parse_file(self) -> None:
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
            adj[name1].append(name2)
        return adj

    def is_path_to_goal(self, start_node: str, goal_node: str) -> bool:
        ordre_zones = {"priority": 0, "normal": 1, "restricted": 2}
        queue = deque([start_node])
        visited = {start_node}
        while queue:
            curr = queue.popleft()
            if curr == goal_node:
                return True
            voisins_valide = []
            for neighbor in self.adj.get(curr, []):
                if neighbor in visited or 'dead' in neighbor:
                    continue
                zone_obj = next(
                    (z for z in self.hub if z['name'] == neighbor), None
                    )
                if zone_obj and zone_obj['zone'] != 'blocked':
                    voisins_valide.append(zone_obj)
            voisins_trie = sorted(
                voisins_valide, key=lambda x: (
                    ordre_zones.get(x['zone'], 3), x['name'])
                    )
            for neighbor_obj in voisins_trie:
                name = neighbor_obj['name']
                visited.add(name)
                queue.append(name)
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
            if current_voisin['zone'] == "blocked" or\
                    "dead" in current_voisin['name']:
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
                if positions[pos]['zone'] == "restricted":
                    drone['path'].append(current_pos)
                positions[pos]['drone'] += 1
                drone['visited'].append(pos)
                positions[current_pos]['drone'] -= 1
                drone['path'].append(pos)
                if pos == self.parser.end[0][0]:
                    self.arrived += 1
                return
        drone['path'].append(current_pos)
        if "challenger" not in self.parser.file:
            return

    def path_for_drone(self):
        drones = self.parser.drone_path
        while self.arrived < self.parser.nb_drones:
            for drone in drones:
                self.get_path(drone)
        return drones


if __name__ == "__main__":
    test = BFS()
    max_len = 0
    test.parse_file()
    result = test.path_for_drone()
    for res in result:
        if len(res['path']) > max_len:
            max_len = len(res['path'])
    for i in range(max_len):
        for res in result:
            if len(res['path']) > i:
                print(f"{res['id']}-{res['path'][i]}", end=' ')
        print()
