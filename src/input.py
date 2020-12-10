import os
from urllib.request import urlopen, Request
from datetime import date
from time import sleep


def input_text(day: int = None, year: int = None) -> str:
    today = date.today()
    if day is None:
        day = today.day
    if year is None:
        year = today.year
    while True:
        today = date.today()
        if today.year * 32 * 12 + today.month * 32 + today.day >= year * 32 * 12 + 12 * 32 + day:
            break
        sleep(1)

    file_name = 'input-{:0>4}{:0>2}.txt'.format(year, day)
    try:
        with open(file_name, 'r') as inp_file:
            return inp_file.read()
    except FileNotFoundError:
        req = Request('https://adventofcode.com/{}/day/{}/input'.format(year, day))
        with open(os.path.join(os.path.dirname(__file__), 'session.cookie'), 'r') as cookie:
            req.add_header('cookie', 'session=' + cookie.read())
        with urlopen(req) as conn:
            inp = conn.read().decode('utf-8')[:-1]
        with open(os.path.join(os.path.dirname(__file__), file_name), 'w') as out_file:
            out_file.write(inp)
        return inp
