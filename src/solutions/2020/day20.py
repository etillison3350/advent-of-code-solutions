from typing import Sequence

from itertools import product

from math import sqrt

from helpers import input


dir_nums = {'t': 0, 'r': 1, 'b': 2, 'l': 3}
dir_nums_reverse = {v: k for k, v in dir_nums.items()}
dir_vecs_reverse = {(0, -1): 't', (1, 0): 'r', (0, 1): 'b', (-1, 0): 'l'}
dir_vecs = {v: k for k, v in dir_vecs_reverse.items()}


def transform(img, flip: bool, rot: int):
    if flip:
        img = [row[::-1] for row in img]
    newimg = [row.copy() for row in img]
    rot %= 4
    if rot == 0:
        return img
    for y in range(len(img)):
        for x in range(len(img[y])):
            if rot == 1:
                nx = y
                ny = len(img) - 1 - x
            elif rot == 2:
                nx = len(img[y]) - 1 - x
                ny = len(img) - 1 - y
            else:
                nx = len(img[y]) - 1 - y
                ny = x
            newimg[ny][nx] = img[y][x]
    return newimg


def run(r: Sequence[str]):
    imgs = {int(img.splitlines()[0][5:-1]): [list(row) for row in img.splitlines()[1:]] for img in r}

    borders = {}
    for k, v in imgs.items():
        b = {'t': v[0], 'b': v[-1][::-1], 'l': [k[0] for k in v][::-1], 'r': [k[-1] for k in v]}
        borders[k] = {k: ''.join(q) for k, q in b.items()}

    matches = set()
    adjacent_counts = {}

    ans = 1
    for id, border_set in borders.items():
        k = 0
        for other_id, other_borders in borders.items():
            if id == other_id:
                continue
            for border1, border2 in product(border_set.items(), other_borders.items()):
                dir1, seq1 = border1
                dir2, seq2 = border2
                if seq1 == seq2:
                    matches.add((id, other_id, dir1))
                    k += 1
                    break
                elif seq1 == seq2[::-1]:
                    matches.add((id, other_id, dir1))
                    k += 1
                    break
        if k == 2:
            ans *= id
        adjacent_counts[id] = k
    print(ans)

    img_size = int(sqrt(len(imgs)))

    img_locations = {}
    top_corner = [n for n, na in adjacent_counts.items() if na == 2][0]
    queue = [(top_corner, 0, 0)]
    placed_img_ids = set()

    while len(queue):
        id, x, y = queue.pop()
        if id in placed_img_ids:
            continue
        adjacent_info = [(direction, other_id) for matched_id, other_id, direction in matches if matched_id == id]

        orientation = [direction for direction, _ in adjacent_info]
        if (x, y) == (0, 0):
            if 't' in orientation:
                if 'r' in orientation:
                    rotation_steps = 3
                else:
                    rotation_steps = 2
            else:
                if 'r' in orientation:
                    rotation_steps = 0
                else:
                    rotation_steps = 1
            img_locations[(0, 0)] = transform(imgs[id], False, rotation_steps)
            placed_img_ids.add(id)
        else:
            if (x - 1, y) in img_locations:
                img = imgs[id]
                match_img = img_locations[(x - 1, y)]
                match = [k[-1] for k in match_img]
                for rot in range(4):
                    for flip in (True, False):
                        t_img = transform(img, flip, rot)
                        if [k[0] for k in t_img] == match:
                            img_locations[(x, y)] = t_img
                            placed_img_ids.add(id)
                            break
                    else:
                        continue
                    break
                else:
                    continue
            else:
                img = imgs[id]
                match_img = img_locations[(x, y - 1)]
                match = match_img[-1]
                for rot in range(4):
                    for flip in (True, False):
                        t_img = transform(img, flip, rot)
                        if t_img[0] == match:
                            img_locations[(x, y)] = t_img
                            placed_img_ids.add(id)
                            break
                    else:
                        continue
                    break
                else:
                    continue

        for _, adj_id in adjacent_info:
            if x + 1 < img_size:
                queue.append((adj_id, x + 1, y))
            if y + 1 < img_size:
                queue.append((adj_id, x, y + 1))
            queue.sort(key=lambda n: n[1] + n[2])

    assembled = []

    for y in range(img_size):
        for x in range(img_size):
            if (x, y) not in img_locations:
                img = [[' '] * 10] * 10
            else:
                img = img_locations[(x, y)]
            while len(assembled) < (len(img) - 2) * (y + 1):
                assembled.append([])
            for i, row in enumerate(img[1:-1]):
                assembled[y * (len(img) - 2) + i] += row[1:-1]

    sea_monster = [list(s) for s in """                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """.splitlines()]
    sea_monster_h = 3
    sea_monster_w = 20

    for rot in range(4):
        for flip in (False, True):
            num_monsters = 0
            asm_img = [row.copy() for row in transform(assembled, flip, rot)]
            for y in range(len(assembled) - sea_monster_h):
                row = asm_img[y]
                for x in range(len(row) - sea_monster_w):
                    for sy in range(sea_monster_h):
                        for sx in range(sea_monster_w):
                            if sea_monster[sy][sx] == '#' and asm_img[y + sy][x + sx] == '.':
                                break
                        else:
                            continue
                        break
                    else:
                        num_monsters += 1
                        for sy in range(sea_monster_h):
                            for sx in range(sea_monster_w):
                                if sea_monster[sy][sx] == '#':
                                    asm_img[y + sy][x + sx] = 'O'
            if num_monsters:
                count = 0
                for row in asm_img:
                    print(''.join(row))
                    for cell in row:
                        if cell == '#':
                            count += 1
                print(count)


if __name__ == '__main__':
    day, year = 20, 2020
    input.wait_for_input(day, year)

    split_seq = '\n\n'

    inp = input.input_text(day, year)
    input_lines = inp.split(split_seq)

    print('True output:')
    run(input_lines)
    print()

    print('Possible test cases:')
    test_cases = input.find_test_cases(day, year, cached=True)
    for index, tc in enumerate(test_cases):
        tc_list = tc.split(split_seq)
        tc_str = str(tc_list)
        print('Test case {}: {}{}'.format(index, tc_str[:80], '...' if len(tc_str) > 80 else ''))
        try:
            run(tc_list)
        except Exception as ex:
            print('{}: {}'.format(type(ex).__name__, ex))
        finally:
            print('Done with test case {}'.format(index))
