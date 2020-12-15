import os
from typing import List
from urllib.request import urlopen, Request
from datetime import date
from time import sleep

import json
from bs4 import BeautifulSoup


def wait_for_input(day: int = None, year: int = None):
    today = date.today()
    if day is None:
        day = today.day
    if year is None:
        year = today.year
    num_waits = 0
    while True:
        today = date.today()
        if today.year * 32 * 12 + today.month * 32 + today.day >= year * 32 * 12 + 12 * 32 + day:
            break
        sleep(1)
        if num_waits % 60 == 0:
            print('Waiting until {}-12-{}...'.format(year, day))
        num_waits += 1


def input_text(day: int = None, year: int = None) -> str:
    today = date.today()
    if day is None:
        day = today.day
    if year is None:
        year = today.year

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


def find_test_cases(day: int = None, year: int = None, cached = False) -> List[str]:
    today = date.today()
    if day is None:
        day = today.day
    if year is None:
        year = today.year

    file_name = 'testcases-{:0>4}{:0>2}.json'.format(year, day)
    if cached:
        try:
            with open(file_name, 'r') as tc_file:
                return ['\n'.join(tc) for tc in json.load(tc_file)]
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    req = Request('https://adventofcode.com/{}/day/{}'.format(year, day))
    with open(os.path.join(os.path.dirname(__file__), 'session.cookie'), 'r') as cookie:
        req.add_header('cookie', 'session=' + cookie.read())
    with urlopen(req) as conn:
        inp = conn.read().decode('utf-8')
    page = BeautifulSoup(inp, 'html.parser')
    possible_test_cases = [elem.get_text().strip() for elem in page.find_all('pre')]
    with open(file_name, 'w') as tc_file:
        json.dump([tc.splitlines() for tc in possible_test_cases], tc_file, indent=2)
    return possible_test_cases
