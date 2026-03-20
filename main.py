from parsing import Parsing
import sys


if __name__ == "__main__":
    try:
        pars = Parsing()
        pars.read_file(sys.argv[1])
        pars.parse()
        pars.check_line()
        pars.parse()
        print(pars.nb_drones)
        for i in pars.zones:
            print(i)
        for i in pars.connections:
            print(i)
        print()
        print(pars.pos)
    except Exception as e:
        print(e)
