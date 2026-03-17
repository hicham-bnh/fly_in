from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum


class Parsing:

    def __init__(self):
        self.data: List = []
        self.all_line: List = []
        self.nb_drones: int = 0
        self.zones: List = []
        self.connections: List = []
        self.pos = []

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

    def parse_zone(self, line: str) -> None:
        parts = line.split()
        name = parts[1]
        x = int(parts[2])
        y = int(parts[3])
        color = parts[4]
        self.pos.append((x, y, color))
        self.zones.append((name, x, y, color))

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
        capacity = 1
        if "[" in line:
            metadata = line.split("[")[1].rstrip("]")
            tags = metadata.split()
            for tag in tags:
                key, value = tag.split("=")
                if key == "max_link_capacity":
                    capacity = int(value)
        self.connections.append((zone1, zone2, capacity))


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
