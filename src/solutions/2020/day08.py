from input import input_text
from re import *

if __name__ == '__main__':
    inp = input_text(8, 2020)
#     r = """nop +0
# # acc +1
# # jmp +4
# # acc +3
# # jmp -3
# # acc -99
# # acc +1
# # jmp -4
# # acc +6""".split('\n')
    p = inp.split('\n')

    for k in range(len(p)):
        print(k)
        r = p.copy()
        if r[k][:3] == 'acc':
            continue
        elif r[k][:3] == 'nop':
            r[k] = 'jmp' + r[k][3:]
        else:
            r[k] = 'nop' + r[k][3:]

        acc = 0
        run_lines = []
        i = 0
        valid = True
        while i < len(r):
            l = r[i]
            # print(l)
            if i in run_lines:
                valid = False
                break
            run_lines.append(i)
            if l[:3] == 'nop':
                i += 1
                continue
            elif l[:3] == 'acc':
                acc += int(l[4:])
                i += 1
                continue
            else:
                i += int(l[4:])
        if valid:
            print(acc)
            break



