from input import input_text
from re import *

if __name__ == '__main__':
    inp = input_text(10, 2020)
    r = inp.split('\n')

    n = [0] + [int(k) for k in r]
    n.sort()
    n.append(n[-1] + 3)

    ones = 1
    threes = 1
    for a, b in zip(n[:-1], n[1:]):
        if b - a == 1:
            ones += 1
        elif b - a == 3:
            threes += 1
    print(ones * threes)

    configs = [1]
    for i in range(1, len(n)):
        configs.append(sum([configs[f] for f in range(i - 3, i) if f >= 0 and n[i] - n[f] <= 3]))
    print(configs[-1])



