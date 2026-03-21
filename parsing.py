from typing import List, Optional, Dict
from dataclasses import dataclass
from enum import Enum
import sys


class Parsing:

    def __init__(self) -> None:
        self.data: List[str] = []
        self.all_line: List[str] = []
        self.nb_drones: int = 0
        self.drone_path = []
        self.zones_path = []
        self.zones: List[dict] = []
        self.connections: List[tuple[Dict, Dict]] = []
        self.pos: List[tuple[int, int, str]] = []
        self.start: List[tuple[str, int, int]] = []
        self.end: List[tuple[str, int, int]] = []

    def read_file(self, file: str) -> None:
        with open(file, "r") as fd:
            self.data = fd.readlines()

    def check_line(self) -> None:
        for line in self.data:
            line = line.strip()
            if line == "":
                continue
            if line.startswith("#"):
                continue
            self.all_line.append(line)

    def parse_nb_drones(self, line: str) -> None:
        res = line.split(":")
        self.nb_drones = int(res[1].strip())
        if self.nb_drones < 1:
            raise ValueError("nb of drone can't be smaller than 1")
        for i in range(self.nb_drones):
            self.drone_path.append({f"drone_{i+1}": ['start']})

    def parse_zone(self, line: str) -> None:
        parts = line.split()
        name = parts[1]
        x = int(parts[2])
        y = int(parts[3])
        color = "white"
        if name == "start":
            self.start.append((name, x, y))
        if name == "goal":
            self.end.append((name, x, y))
        zone = {
                "name": name,
                "x": x,
                "y": y,
                "color": color,
                "zone": "normal",
                "capacity": 1,
                "drone": 0
            }
        if "[" in line:
            pars = line.split("[")[1].split("]")[0]
            tags = pars.split()
            for tag in tags:
                if "=" in tag:
                    key, value = tag.split("=", 1)
                    if key == "color":
                        zone['color'] = value
                    if key == "zone":
                        zone['zone'] = value
                    if key == "max_drones":
                        zone['capacity'] = int(value)
        self.zones.append(zone)
        zone_final = [zone['name'], zone]
        self.zones_path.append(zone_final)

    def parse(self) -> None:
        for line in self.all_line:
            if line.startswith("nb_drones:"):
                self.parse_nb_drones(line)
            elif line.startswith("start_hub:"):
                self.parse_zone(line)
            elif line.startswith("end_hub:"):
                self.parse_zone(line)
            elif line.startswith("hub:"):
                self.parse_zone(line)
            elif line.startswith("connection:"):
                self.parse_connection(line)

    def parse_connection(self, line: str) -> None:
        left = line.split("[")[0]
        part = left.split()[1]
        zone1, zone2 = part.split("-")
        for i in self.zones:
            if i['name'] == zone1:
                zone_a = i
            if i['name'] == zone2:
                zone_b = i
        self.connections.append((zone_a, zone_b))


class ZoneType(Enum):
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


@dataclass
class Zone:
    name: str
    x: int
    y: int
    zone_type: ZoneType = ZoneType.NORMAL
    color: Optional[str] = None
    is_start: bool = False
    is_end: bool = False


@dataclass
class Connection:
    zone1: str
    zone2: str
    max_capacity: int = 1
