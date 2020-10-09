import sys
from pandas import DataFrame


class Main:
    def __init__(self, file: str = None):
        self.file = file
        self.map = []
        self.squares = []

    def get_map(self):
        try:
            with open(self.file, 'r') as f:
                f.readline()  # remove the first line which is the number of the map's lines
                for line in f.readlines():
                    self.map.append([char for char in line.strip()])

                return self.map
        except FileNotFoundError:
            return '"{}" not found.'.format(sys.argv[1])

    def get_square(self):
        square_size = 0
        for y in range(len(self.map) - 1):  # original
            # for y in range(0, len(self.map) - 9):  # testing
            for x in range(len(self.map[y]) - 1):  # original
                # for x in range(20, len(self.map[y]) - 1):  # testing
                if self.map[y][x] == '.':
                    if self.map[y + 1][x + 1] == '.' and self.map[y + 1][x] == '.' and self.map[y][x + 1] == '.':
                        max_y = len(self.map)  # default value for the height of the square
                        max_x = len(self.map[y])  # default value for length of the square

                        # get the first round in axe y
                        for y2 in range(y, len(self.map)):
                            if self.map[y2][x] == 'o':
                                max_y = y2
                                break

                        # get the first round in axe x
                        for x2 in range(x, len(self.map[y])):
                            if self.map[y][x2] == 'o':
                                max_x = x2
                                break

                        # get the min value between y and x
                        max_size = min(abs(max_y - y), abs(max_x - x))

                        max_y = max_size + y
                        max_x = max_size + x

                        # get the first round in axe y - x
                        for y2 in range(y, max_y - 1):
                            for x2 in range(x, max_x - 1):
                                if abs(y2 + 1 - max_y) == abs(x2 + 1 - max_x):
                                    if self.map[y2 + 1][x2 + 1] == 'o' and y2 + 1 < max_y and x2 + 1 < max_x:
                                        # print(y2 + 1, x2 + 1)
                                        max_y = y2 + 1
                                        max_x = x2 + 1

                        square_coords = []

                        def get_squares(start_y: int, start_x: int, y_min: int = max_y, x_min: int = max_x):
                            for y3 in range(start_y, y_min):
                                if self.map[y3][start_x] == 'o':
                                    if y3 < y_min:
                                        y_min = y3
                                        break

                            for x3 in range(start_x, x_min):
                                if self.map[start_y][x3] == 'o':
                                    if x3 < x_min:
                                        x_min = x3
                                        break

                            min_size = min(abs(y_min - y), abs(x_min - x))
                            y_min = y + min_size
                            x_min = x + min_size

                            if start_y + 1 < y_min and start_x + 1 < x_min:
                                get_squares(start_y + 1, start_x + 1, y_min, x_min)

                            square_coords.append([y_min, x_min])

                            return

                        get_squares(y + 1, x + 1)
                        min_y, min_x = min(square_coords)

                        if square_size < len(self.map[y:min_y]):
                            square_size = len(self.map[y:min_y])

                            self.squares.append([y, min_y, x, min_x])

        return self.squares

    def place_square(self):
        if len(self.squares) >= 0:
            start_y = max(self.squares)[0]
            end_y = max(self.squares)[1]
            start_x = max(self.squares)[2]
            end_x = max(self.squares)[3]

            for y in range(start_y, end_y):
                for x in range(start_x, end_x):
                    self.map[y][x] = 'x'

        return self.map


try:
    main = Main(sys.argv[1])
    main.get_map()
    main.get_square()
    print('Map :\n', DataFrame(main.place_square()))
except IndexError:
    print('No file specified')
