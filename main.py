from parsing import Parsing


if __name__ == "__main__":
    file = input("enter the path for the map : ")
    pars = Parsing()
    pars.open_file(file)