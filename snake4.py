#!/usr/bin/python3

"""
    Program: 	Python Beginner Tutorial
		Classic Snake Game - Part 4 (snake4.py)
			 
    Author:  	M. Heidenreich, (c) 2021
      
    Description:
    This code is provided in support of the following YouTube tutorial:
    https://youtu.be/ykZpxsjQTlI
    
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
from collections import namedtuple
from threading import Thread
from time import sleep
from random import choice, randint

game_on = False
keyboard_on = True
point = namedtuple("point", "y x")
number = namedtuple("number", "value color")

directions = {
                curses.KEY_UP: point(-1, 0), curses.KEY_DOWN: point(1, 0),
                curses.KEY_RIGHT: point(0, 1), curses.KEY_LEFT: point(0, -1)
            }

colors = (
            curses.COLOR_BLUE, curses.COLOR_CYAN, curses.COLOR_GREEN,
            curses.COLOR_MAGENTA, curses.COLOR_RED, curses.COLOR_YELLOW
        )

def safe_exit():
    exit(1)

def grow_food():
    global food

    while True:
        location = point(randint(1, terminal_y-3), randint(1, terminal_x-2))

        if location not in snake and location not in food:
            value = randint(1, 9)
            color = choice(colors)

            food[location] = number(value, color)

            game_area.addstr(location.y, location.x, f"{value}", curses.color_pair(color))
            break

def start_game():
    global snake, game, game_on, bearing, food, score, color_bands

    game_area.clear()

    bearing = choice(list(directions))

    snake = [point(terminal_y//2, terminal_x//2)]
    color_bands = [number(1, choice(colors))]

    game_area.addstr(snake[0].y, snake[0].x, "\u2588", curses.color_pair(color_bands[0].color))

    score = 0
    show_score()

    food = {}
    for __ in range(terminal_y//2):
        grow_food()

    game_area.border()
    game_area.refresh()

    gameover_popup.addstr(1, 15, "Game Over!", curses.color_pair(curses.COLOR_YELLOW))
    gameover_popup.addstr(2, 5, "Press Space Bar to Play Again!", curses.color_pair(curses.COLOR_GREEN))
    gameover_popup.border()

    game_on = True
    game = Thread(target=play, daemon=True)
    game.start()

def show_score():
    global hi_score

    if score > hi_score:
        hi_score = score

    score_board.addstr(0, terminal_x-11, f"P1: {score:06d}", curses.color_pair(curses.COLOR_BLUE))
    score_board.addstr(0, terminal_x//2-5, f"HI: {hi_score:06d}", curses.color_pair(curses.COLOR_RED))
    score_board.refresh()

def play():
    global keyboard_on

    try:
        while game_on:
            move_snake()

        gameover_popup.refresh()

        if hi_score == score:
            with open("snake.hi", "w") as hi:
                hi.write(str(hi_score))

    except Exception as e:
        keyboard_on = False
        curses.endwin()
        print(f"UNEXPECTED ERROR: {e}")

def move_snake():
    global game_on, score

    growth = [color_bands[0].color]

    while growth:
        sleep(0.1)

        new_location = point(snake[0].y + directions[bearing].y, snake[0].x + directions[bearing].x)

        if new_location in food:
            grow_food()
            game_area.refresh()

            color = food[new_location].color

            growth[0] = color
            growth[:0] = [color] * food[new_location].value

            score += food[new_location].value
            color_bands.insert(0, number(score+1, color))

            show_score()

            food.pop(new_location)

        snake.insert(0, new_location)

        game_area.addstr(new_location.y, new_location.x, "\u2588", curses.color_pair(growth[-1]))

        if new_location.y in (0, terminal_y-2) or new_location.x in (0, terminal_x-1) or new_location in snake[4:]:
            
            game_on = False
            break

        growth.pop(-1)

    game_area.addstr(snake[-1].y, snake[-1].x, " ")
    snake.pop(-1)

    for band in color_bands[1:]:
        segment = len(snake) - band.value
        game_area.addstr(snake[segment].y, snake[segment].x, "\u2588", curses.color_pair(band.color))

    game_area.refresh()

try:
    signal(SIGTERM, safe_exit)

    terminal = curses.initscr()
    terminal_y, terminal_x = terminal.getmaxyx()

    if terminal_y < 20 or terminal_x < 50:
        raise RuntimeError

    curses.curs_set(0)
    curses.noecho()
    curses.start_color()
    curses.use_default_colors()

    for color in colors:
        curses.init_pair(color, color, -1)

    score_board = curses.newwin(1, terminal_x, 0, 0)
    game_area = curses.newwin(terminal_y-1, terminal_x, 1, 0)
    game_area.keypad(True)
    game_area.timeout(50)

    gameover_popup = curses.newwin(4, 40, terminal_y//2-2, terminal_x//2-20)

    score_board.bkgd(curses.A_BOLD)
    game_area.bkgd(curses.A_BOLD)
    gameover_popup.bkgd(curses.A_BOLD | curses.color_pair(curses.COLOR_RED))

    try:
        with open("snake.hi", "r") as hi:
            hi_score = int(hi.read())

    except FileNotFoundError:
        hi_score = 0

    start_game()

    while keyboard_on:
        key = game_area.getch()

        if key in directions:
            if (directions[bearing].y + directions[key].y, directions[bearing].x + directions[key].x) != (0, 0) or not score:
                bearing = key
        elif not game_on and key == 32:
            start_game()

except KeyboardInterrupt:
    pass

except RuntimeError:
    curses.endwin()
    print("ERROR: Terminal window too small!")
    print("At least 50x20 characters dimensions are required")
    print(f"Current terminal dimensions are: {terminal_x}x{terminal_y}")

finally:
    if game_on:
        game_on = False
        game.join()

    if not curses.isendwin():
        curses.endwin()
