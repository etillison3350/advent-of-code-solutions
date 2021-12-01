from helpers.input import input_text
from re import *


def f(d, b):
    return sum([f(d, k) * int(d[b][k]) for k in d[b].keys()]) + 1


if __name__ == '__main__':
    r = input_text(7, 2020).split('\n')

    m = [search('(\\w+ \\w+) bags contain (.+)', l).group(1, 2) for l in r]
    d = dict(m)
    for k, v in d.items():
        try:
            d[k] = dict([search('(\\d+) (\\w+ \\w+)', q).group(2, 1) for q in v.split(',')])
        except AttributeError:
            d[k] = {}
    print(f(d, 'shiny gold') - 1)

