from typing import Sequence

from itertools import product

from math import sqrt

import input


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
    adjs = {}

    ans = 1
    for n, bs in borders.items():
        k = 0
        for n2, b2 in borders.items():
            if n == n2:
                continue
            for border1, border2 in product(bs.items(), b2.items()):
                dir1, seq1 = border1
                dir2, seq2 = border2
                if seq1 == seq2:
                    matches.add((n, n2, dir1, dir2, True))
                    k += 1
                    break
                elif seq1 == seq2[::-1]:
                    matches.add((n, n2, dir1, dir2, False))
                    k += 1
                    break
        if k == 2:
            ans *= n
        adjs[n] = k
    print(ans)

    size = int(sqrt(len(imgs)))

    out = {}
    top_corner = [n for n, na in adjs.items() if na == 2][0]
    queue = [(top_corner, 0, 0)]
    mapped = set()

    while len(queue):
        curr_id, curr_x, curr_y = queue.pop()
        if curr_id in mapped:
            continue
        adjacent_info = [(direction, other, other_dir, flipped) for this, other, direction, other_dir, flipped in matches if this == curr_id]

        orientation = [direction for direction, _, _, _ in adjacent_info]
        if (curr_x, curr_y) == (0, 0):
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
            out[(0, 0)] = transform(imgs[curr_id], False, rotation_steps)
            mapped.add(curr_id)
        else:
            if (curr_x - 1, curr_y) in out:
                img = imgs[curr_id]
                match_img = out[(curr_x - 1, curr_y)]
                match = [k[-1] for k in match_img]
                for rot in range(4):
                    for flip in (True, False):
                        t_img = transform(img, flip, rot)
                        if [k[0] for k in t_img] == match:
                            out[(curr_x, curr_y)] = t_img
                            mapped.add(curr_id)
                            break
                    else:
                        continue
                    break
                else:
                    continue
            else:
                img = imgs[curr_id]
                match_img = out[(curr_x, curr_y - 1)]
                match = match_img[-1]
                for rot in range(4):
                    for flip in (True, False):
                        t_img = transform(img, flip, rot)
                        if t_img[0] == match:
                            out[(curr_x, curr_y)] = t_img
                            mapped.add(curr_id)
                            break
                    else:
                        continue
                    break
                else:
                    continue

        for _, adj_id, _, _ in adjacent_info:
            if curr_x + 1 < size:
                queue.append((adj_id, curr_x + 1, curr_y))
            if curr_y + 1 < size:
                queue.append((adj_id, curr_x, curr_y + 1))
            queue.sort(key=lambda n: n[1] + n[2])

    assembled = []

    for y in range(size):
        for x in range(size):
            if (x, y) not in out:
                img = [[' '] * 10] * 10
            else:
                img = out[(x, y)]
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
