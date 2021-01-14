#!/usr/bin/python3

"""
    Program: 	Python Beginner Tutorial
		Classic Snake Game - Part 1 (snake1.py)
			 
    Author:  M. Heidenreich, (c) 2021

    Description:

    This code is provided in support of the following YouTube tutorial:
    https://youtu.be/kANj0hZHR54
    
    This multi-part tutorial is a tool for beginners to get into Python
    programming on Linux. Basic concepts and practices are introduced
    and explained using a classic snake game.

    THIS SOFTWARE AND LINKED VIDEO TOTORIAL ARE PROVIDED "AS IS" AND THE
    AUTHOR DISCLAIMS ALL WARRANTIES INCLUDING ALL IMPLIED WARRANTIES OF
    MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
    ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
    WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
    ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
    OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""

import curses
from signal import signal, SIGTERM, pause

def safe_exit():
    exit(1)

def start_game():
    game_area.border()
    game_area.refresh()

    pause()

try:
    signal(SIGTERM, safe_exit)

    terminal = curses.initscr()
    terminal_y, terminal_x = terminal.getmaxyx()

    if terminal_y < 20 or terminal_x < 50:
        raise RuntimeError

    curses.curs_set(0)
    curses.noecho()

    score_board = curses.newwin(1, terminal_x, 0, 0)
    game_area = curses.newwin(terminal_y-1, terminal_x, 1, 0)
    game_area.keypad(True)
    game_area.timeout(10)

    start_game()

except RuntimeError:
    curses.endwin()
    print("ERROR: Terminal window too small!")
    print("At least 50x20 characters dimensions are required")
    print(f"Current terminal dimensions are: {terminal_x}x{terminal_y}")

finally:
    if not curses.isendwin():
        curses.endwin()
