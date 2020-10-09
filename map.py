import random


def generate_map(x: int, y: int, density: int):
    print(y)
    for h in range(y):
        for w in range(x):
            print('o', end='') if random.randint(0, y) * 2 < density else print('.', end='')
        print('\n', end='')


generate_map(30, 10, 1)
