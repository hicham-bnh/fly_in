from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum


class Parsing:
    def __init__(self):
        self.data = []
        self.all_line = []

    def read_file(self, file: str) -> None:
        with open(file, "r") as fd:
            self.data = fd.readlines()

    def check_line(self) -> None:
        for line in self.data:
            if line == "":
                continue
            if line.startswith("#"):
                continue
            self.all_line.append(line)


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
    zone_type: str = ZoneType.NORMAL
    color: Optional[str] = None
    is_start: bool = False
    is_end: bool = False


@dataclass
class Connection:
    zone1: str
    zone2: str
    max_capacity: int = 1
