from parsing import Parsing


if __name__ == "__main__":
    try:
        file = input("enter the path for the map : ")
        pars = Parsing()
        pars.read_file(file)
        pars.parse()
        pars.check_line()
        pars.parse()
    except Exception as e:
        print(e)