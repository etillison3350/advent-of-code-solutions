from input import input_text
from re import *

if __name__ == '__main__':
    inp = input_text(9, 2020)
    r = inp.split('\n')

    d = 25

    n = [int(k) for k in r]

    for i in range(d, len(n)):
        found = False
        for j in range(i - d, i):
            for k in range(j + 1, i):
                if n[j] + n[k] == n[i]:
                    found = True
                    break
            if found:
                break
        if not found:
            v = n[i]
            print(v)
            break

    for i in range(len(n)):
        for j in range(i + 1, len(n)):
            if sum(n[i:j]) == v:
                print(n[i:j])
                print(min(n[i:j]) + max(n[i:j]))


