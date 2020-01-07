import numpy.random as nprandom

PORTION_SIZE = 30
MIN_WIDTH = 300
MAX_WIDTH = 400
MAP_HEIGHT = 32


def get_floor():
    def is_gap():
        if nprandom.uniform() < 0.5:
            gap_size = nprandom.randint(4, PORTION_SIZE // 3)
            return (
            nprandom.randint(1, PORTION_SIZE - 1 - gap_size), gap_size)  # unde incepe prapastia si ce lungimme are

    gap = is_gap()
    if not gap:
        return (False, ['T'] * PORTION_SIZE)
    gap_start, gap_size = gap
    gap_line = (['T'] * gap_start) + ([' '] * gap_size) + (['T'] * (PORTION_SIZE - gap_start - gap_size))
    return (True, gap_line)


def add_pipe(portion):
    def pipe_base(): return [' '] * (PORTION_SIZE // 2 - 1 - PORTION_SIZE % 2) + ['T'] * 3 + [' '] * (
                PORTION_SIZE // 2 - 2 + PORTION_SIZE % 2)

    def pipe_top(): return [' '] * (PORTION_SIZE // 2 - 2 - PORTION_SIZE % 2) + ['T'] * 5 + [' '] * (
                PORTION_SIZE // 2 - 3 + PORTION_SIZE % 2)

    portion.append(pipe_base())
    portion.append(pipe_base())
    portion.append(pipe_base())
    portion.append(pipe_base())
    portion.append(pipe_top())
    portion.append(pipe_top())


def get_portion():
    portion_size = nprandom.randint(4, PORTION_SIZE // 2)
    portion_start = nprandom.randint(1, PORTION_SIZE - 1 - portion_size)
    monster_number = nprandom.randint(-1, portion_size // 5)
    coin_number = nprandom.randint(-1, portion_size // 4)
    monster_pos = [nprandom.randint(0, portion_size) for _ in range(0, monster_number)]
    coin_pos = [nprandom.randint(0, portion_size) for _ in range(0, coin_number)]
    portion = ([' '] * portion_start) + (['T'] * portion_size) + ([' '] * (PORTION_SIZE - portion_start - portion_size))

    coin_monster_portion = [' '] * PORTION_SIZE
    for mp in monster_pos:
        coin_monster_portion[portion_start + mp] = 'E'
    for cp in coin_pos:
        coin_monster_portion[portion_start + cp] = 'B'
    return (portion, coin_monster_portion)


def complete_portion(portion):
    portion_height = len(portion)
    for _ in range(portion_height, MAP_HEIGHT):
        portion.append([' '] * PORTION_SIZE)


def print_portion(portion):
    for h in range(MAP_HEIGHT - 1, -1, -1):
        print(''.join(portion[h]))




def build_map(map_name):
    map_width = nprandom.randint(MIN_WIDTH, MAX_WIDTH)
    map_width -= map_width % PORTION_SIZE
    harta = []
    for i in range(map_width // PORTION_SIZE):
        portion = []
        pipe = False
        if i == 0:
            is_gap = True
            while is_gap:
                is_gap, floor = get_floor()
        else:
            is_gap, floor = get_floor()
        if is_gap:
            floor_range = 3
            portions_range = 6
        else:
            floor_range = 2
            portions_range = 3
            if nprandom.random() < 0.0:
                portions_range = 11
                pipe = True
        for _ in range(floor_range):
            portion.append(floor)

        if is_gap:
            portion.append([' '] * PORTION_SIZE)
            portion.append([' '] * PORTION_SIZE)
            portion.append([' '] * PORTION_SIZE)
            portion.append([' '] * PORTION_SIZE)
        elif pipe:
            add_pipe(portion)
        portion_prob = 0.0
        for i in range(portions_range, MAP_HEIGHT, 6):
            if nprandom.uniform() < portion_prob:
                por, coin_monster_por = get_portion()
                portion.append(por)
                portion.append([' '] * PORTION_SIZE)
                portion.append(coin_monster_por)
                portion.append([' '] * PORTION_SIZE)
                portion.append([' '] * PORTION_SIZE)
                portion.append([' '] * PORTION_SIZE)
                portion.append([' '] * PORTION_SIZE)

                portion_prob -= 0.1
            else:
                break

        complete_portion(portion)
        harta.append(portion)

    # Inlocuieste cu unul gol
    open('./maps/'+map_name+'.map', 'w').close()

    map_string = ''
    harta[0][10][20] = 'P'
    harta[-1][4][PORTION_SIZE - 3] = 'F'
    harta[-1][4][PORTION_SIZE - 2] = ' '
    harta[-1][4][PORTION_SIZE - 4] = ' '
    harta[-1][3][PORTION_SIZE - 4] = ' '
    harta[-1][3][PORTION_SIZE - 3] = ' '
    harta[-1][3][PORTION_SIZE - 2] = ' '

    for h in range(MAP_HEIGHT - 1, -1, -1):
        for map_portion in harta:
            map_string += ''.join(map_portion[h])
        map_string += '\n'
    with open('./maps/'+map_name+'.map', 'w') as fd:
        fd.write(map_string)


