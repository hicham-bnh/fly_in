from typing import List, Optional
from dataclasses import dataclass
from enum import Enum


class Parsing:

    def __init__(self):
        self.data: List = []
        self.all_line: List = []
        self.nb_drones: int = 0
        self.zones: List = []
        self.connections: List = []
        self.pos: List = []
        self.start: List = []
        self.end: List = []

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

    def parse_zone(self, line: str) -> None:
        parts = line.split()
        name = parts[1]
        x = int(parts[2])
        y = int(parts[3])
        color = "white"
        if name == "start":
            self.start.append((x, y))
        if name == "goal":
            self.end.append((x, y))
        if "[" in line:
            pars = line.split("[")[1].split("]")[0]
            tags = pars.split()
            zone_pars = None
            max_drone = None
            for tag in tags:
                if "=" in tag:
                    key, value = tag.split("=", 1)
                    if key == "color":
                        color = value
                    if key == "zone":
                        zone_pars = value
                    if key == "max_drones":
                        max_drone = int(value)
        self.pos.append((x, y, color))
        if zone_pars is not None and max_drone is not None:
            self.zones.append((name, x, y, color, zone_pars, max_drone))
        elif zone_pars is None and max_drone is not None:
            self.zones.append((name, x, y, color, max_drone))
        elif zone_pars is not None and max_drone is None:
            self.zones.append((name, x, y, color, zone_pars))
        else:
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
        self.connections.append((zone1, zone2))


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
