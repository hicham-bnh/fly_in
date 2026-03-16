from typing import List


class Parsing:
    def __init__(self) -> None:
        self.drone: int = 0
        self.path: List = []
        self.connection: List = []

    def open_file(self, file):
        try:
            with open(file, "r") as fd:
                data = fd.read()
            result = data.split('\n')
            for line in result:
                if 'nb_drones' in line:
                    res = line.split(':')
                    self.drone = int(res[1])
                if '[' in line:
                    res = line.split(':')
                    self.path.append(res[1])
                if "connection" in line:
                    res = line.split(':')
                    self.connection.append(res[1])
        except Exception as e:
            print(e)
        print(self.drone)
        print(self.path)
        print(self.connection)