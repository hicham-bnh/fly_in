from parsing import Parsing
from typing import List
from collections import deque
from typing import Dict, Any


class BFS:
    def __init__(self, file: str) -> None:
        self.parser = Parsing(file)
        self.start: List[tuple[str, int, int]] = []
        self.end: List[tuple[str, int, int]] = []
        self.path: List[str] = []
        self.adj: Dict[Any, Any] = {}
        self.arrived = 0
        self.old = None

    def parse_file(self) -> None:
        self.start = self.parser.start
        self.end = self.parser.end
        self.connection = self.parser.connections
        self.hub = self.parser.zones
        self.adj = self.build_adj()

    def build_adj(self) -> Dict[Any, Any]:
        adj: Dict[Any, Any] = {}
        for zone in self.parser.zones:
            adj[zone['name']] = []
        for z1, z2 in self.parser.connections:
            name1 = z1['name']
            name2 = z2['name']
            adj[name1].append(name2)
        return adj

    def is_path_to_goal(self, start_node: str, goal_node: str) -> float | int:
        ordre_zones = {"priority": 0, "normal": 1, "restricted": 2}
        queue = deque([(start_node, 0)])
        visited = {start_node}
        while queue:
            curr, dist = queue.popleft()
            if curr == goal_node:
                return dist
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
                queue.append((name, dist + 1))
        return float('inf')

    def get_path(self, drone: Any) -> None:
        positions = {z['name']: z for z in self.hub}
        goal = self.parser.end[0][0]
        positions[self.parser.end[0][0]]['capacity'] = self.parser.nb_drones
        current_pos = drone['path'][-1]
        if current_pos == self.parser.end[0][0]:
            return
        voisins = self.adj[current_pos]
        candidates = []
        for name in voisins:
            obj = positions[name]
            if obj['zone'] == 'blocked' or 'dead' in name:
                continue
            if obj['capacity'] == obj['drone'] and name != goal:
                continue
            if obj['name'] in drone['visited']:
                continue
            dist = self.is_path_to_goal(name, goal)
            if dist != float('inf'):
                candidates.append({
                    'name': name,
                    'dist': dist,
                    'zone_priority': {
                            "priority": 0,
                            "normal": 1,
                            "restricted": 2
                        }.get(obj['zone'], 3)
                })
        if not candidates:
            drone['path'].append(current_pos)
            if len(drone['path']) > 5 and all(
                p == current_pos for p in drone['path'][-5:]
            ):
                drone['visited'] = []
            return
        candidates.sort(key=lambda x: (
            x['dist'], x['zone_priority'], x['name'])
        )
        best_path = candidates[0]['name']
        positions[current_pos]['drone'] -= 1
        positions[best_path]['drone'] += 1
        drone['visited'].append(best_path)
        drone['path'].append(best_path)
        if best_path == goal:
            self.arrived += 1

    def path_for_drone(self) -> List[Any]:
        drones = self.parser.drone_path
        while self.arrived < self.parser.nb_drones:
            for drone in drones:
                self.get_path(drone)
        return drones
