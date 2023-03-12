import random
import time

from Draw import Draw
from Bardak import Bardak
from Figure import Figure
import Dicts
from Exceptions import CouldNotApplyFigure

draw = Draw(500, 700, Dicts.colorsDict)
bardak = Bardak(15, 30, 9)
draw.draw_bardak(bardak)

all_figures = []


def add_figure():
    rnd_type = random.randrange(len(Dicts.figures))
    angle = random.randrange(4)
    row = random.randrange(bardak.height - len(Dicts.figures[rnd_type][angle]) + 1)
    col = random.randrange(bardak.width - len(Dicts.figures[rnd_type][angle][0]) + 1)
    rnd_figure = Figure(rnd_type, angle,
                        row,
                        col,
                        Dicts.figures[rnd_type]
                        )
    try:
        bardak.save_figure_and_return_filled_lines(rnd_figure)
        draw.draw_figure(rnd_figure)
        all_figures.append(rnd_figure)
    except CouldNotApplyFigure as e:
        print("error")


while True:
    draw.win.update()
    key = draw.win.lastKey
    if key != "":
        draw.win.lastKey = ""
        if key == 'q':
            break
    add_figure()
    time.sleep(0.1)

all_figures.reverse()
for f in all_figures:
    draw.win.update()
    key = draw.win.lastKey
    if key != "":
        draw.win.lastKey = ""
        if key == 'q':
            break
    draw.clear_figure(f)
    time.sleep(0.1)

bardak = Bardak(15, 30, 9)

last = None
for i in range(bardak.width // 2):
    f1 = Figure(1, 2, 5, i * 2, Dicts.figures[1])
    f2 = Figure(1, 0, 7, i * 2, Dicts.figures[1])
    bardak.save_figure_and_return_filled_lines(f1)
    draw.draw_figure(f1)
    last = bardak.save_figure_and_return_filled_lines(f2)
    draw.draw_figure(f2)
if bardak.width % 2 == 1:
    f = Figure(0, 1, 6, bardak.width - 2, Dicts.figures[0])
    last = bardak.save_figure_and_return_filled_lines(f)
    draw.draw_figure(f)

time.sleep(1)
for row in last:
    bardak.drop_line(row)
    draw.drop_line(bardak, row)
    time.sleep(0.5)
time.sleep(1)
draw.draw_bardak(bardak)
time.sleep(3)
