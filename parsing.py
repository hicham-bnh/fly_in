from typing import List, Any


class Parsing:
    def __init__(self, file: str) -> None:
        self.data: List[str] = []
        self.all_line: List[str] = []
        self.nb_drones: int = 0
        self.drone_path: List[Any] = []
        self.zones_path: List[str] = []
        self.zones: List[Any] = []
        self.connections: List[Any] = []
        self.pos: List[tuple[int, int, str]] = []
        self.start: List[tuple[str, int, int]] = []
        self.end: List[tuple[str, int, int]] = []
        self.valide_name: List[str] = []
        self.is_link: int = 0
        self.nmbr_link: int = 0
        self.check_connections: set[Any] = set()
        self.link_capacity: List[Any] = []
        self.read_file(file)
        self.check_line()
        self.parse()
        self.check_start_end()
        self.file = file

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
        clean_val = res[1].strip().replace(',', '.')
        self.nb_drones = int(float(clean_val))
        if self.nb_drones < 1:
            raise ValueError("nb of drone can't be smaller than 1")
        if self.nb_drones > 2147483648:
            raise ValueError("int max depaced")
        for i in range(self.nb_drones):
            self.drone_path.append(
                {
                    "id": f"D{i+1}",
                    "path": ['start'],
                    "visited": []
                    }
                )

    def parse_zone(self, line: str) -> None:
        zone_type = ["normal", "restricted", "blocked", "priority"]
        parts = line.split()
        name = parts[1]
        if name in self.valide_name:
            raise ValueError("name of hub olso exist")
        x = int(parts[2])
        y = int(parts[3])
        color = "white"
        if name == "start":
            self.start.append((name, x, y))
        if name == "goal" or name == "impossible_goal":
            self.end.append((name, x, y))
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
                        if zone_pars not in zone_type:
                            raise ValueError("zone type invalide")
                    if key == "max_drones":
                        max_drone = int(value)
                        if max_drone < 1:
                            raise ValueError("capacity must be more than 0")
        self.pos.append((x, y, color))
        if zone_pars is not None and max_drone is not None:
            zone = {
                "name": name,
                "x": x,
                "y": y,
                "color": color,
                "zone": zone_pars,
                "capacity": max_drone,
                "drone": 0
            }
            self.zones.append(zone)
        elif zone_pars is None and max_drone is not None:
            zone = {
                "name": name,
                "x": x,
                "y": y,
                "color": color,
                "zone": "normal",
                "capacity": max_drone,
                "drone": 0
            }
            self.zones.append(zone)
        elif zone_pars is not None and max_drone is None:
            zone = {
                "name": name,
                "x": x,
                "y": y,
                "color": color,
                "zone": zone_pars,
                "capacity": 1,
                "drone": 0
            }
            self.zones.append(zone)
        else:
            zone = {
                "name": name,
                "x": x,
                "y": y,
                "color": color,
                "zone": "normal",
                "capacity": 1,
                "drone": 0
            }
            self.zones.append(zone)
            self.valide_name.append(name)

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
        if "[max_link_capacity" in line:
            test = line.split(" ")[2]
            num = test.split('=')
            result = str(num[1].split(']')[0])
            self.nmbr_link = int(result)
            if self.nmbr_link < 1:
                raise ValueError("capacity link must be more than 0")
            if self.is_link >= self.nmbr_link:
                return
            left = line.split("[")[0]
            part = left.split()[1]
            zone1, zone2 = part.split("-")
            self.link_capacity.append((int(result[0]), zone2))
            self.is_link = True
            zone_a = None
            zone_b = None
            for i in self.zones:
                if i['name'] == zone1:
                    zone_a = i
                if i['name'] == zone2:
                    zone_b = i
            if zone_a is None or zone_b is None:
                raise ValueError("name connection invalide")
            check_conect = tuple(sorted((zone1, zone2)))
            if check_conect in self.check_connections:
                raise ValueError("connections is existed")
            self.connections.append((zone_a, zone_b))
            self.check_connections.add(check_conect)
            self.is_link += 1
        else:
            left = line.split("[")[0]
            part = left.split()[1]
            zone1, zone2 = part.split("-")
            if self.is_link and self.link_capacity[0] is not zone2\
                    and self.link_capacity[0][1][:-1] in zone2:
                return
            zone_a = None
            zone_b = None
            for i in self.zones:
                if i['name'] == zone1:
                    zone_a = i
                if i['name'] == zone2:
                    zone_b = i
            if zone_a is None or zone_b is None:
                raise ValueError("name connection invalide")
            check_conect = tuple(sorted((zone1, zone2)))
            if check_conect in self.check_connections:
                raise ValueError("connections is existed")
            self.connections.append((zone_a, zone_b))
            self.check_connections.add(check_conect)

    def check_start_end(self) -> None:
        if self.start == [] or self.end == []:
            raise ValueError("you must have start end goal")
