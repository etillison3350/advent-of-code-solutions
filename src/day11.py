from input import input_text
from copy import deepcopy


def getOrNone(array, x, y):
    if y < 0 or y >= len(array):
        return None
    row = array[y]
    if x < 0 or x >= len(row):
        return None
    return row[x]


def getLineOrNone(array, x, offsetX, y, offsetY):
    n = 1
    while True:
        p = getOrNone(array, x + n * offsetX, y + n * offsetY)
        if p != '.':
            return p
        n = n + 1


if __name__ == '__main__':
    inp = input_text(11, 2020)
    r = inp.split('\n')

    board = [list(k) for k in r]
    while True:
        newBoard = deepcopy(board)
        for y in range(len(board)):
            row = board[y]
            for x in range(len(row)):
                cell = row[x]
                if cell == '.':
                    continue
                adj = [getOrNone(board, x + ox, y + oy) for ox, oy in
                     [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]]
                numCells = sum(k == '#' for k in adj)
                if cell == 'L' and numCells == 0:
                    newBoard[y][x] = '#'
                elif cell == '#' and numCells >= 4:
                    newBoard[y][x] = 'L'
        if board == newBoard:
            break
        board = newBoard

    print(sum(sum(c == '#' for c in row) for row in board))

    board = [list(k) for k in r]
    while True:
        newBoard = deepcopy(board)
        for y in range(len(newBoard)):
            row = newBoard[y]
            for x in range(len(row)):
                cell = row[x]
                if cell == '.':
                    continue
                adj = [getLineOrNone(board, x, ox, y, oy) for ox, oy in
                     [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]]
                numCells = len([k for k in adj if k == '#'])
                if cell == 'L' and numCells == 0:
                    newBoard[y][x] = '#'
                elif cell == '#' and numCells >= 5:
                    newBoard[y][x] = 'L'
        if newBoard == board:
            break
        board = newBoard
    print(sum(sum(c == '#' for c in row) for row in board))



