from parsing import Parsing


if __name__ == "__main__":
    try:
        file = input("enter the path for the map : ")
        pars = Parsing()
        pars.read_file(file)
        pars.parse()
        pars.check_line()
        pars.parse()
        print(pars.nb_drones)
        for i in pars.zones:
            print(i)
        for i in pars.connections:
            print(i)
    except Exception as e:
        print(e)