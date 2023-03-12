import random
import time

from Draw import Draw
from Bardak import Bardak
from Figure import Figure
import Dicts
from Exceptions import CouldNotApplyFigure
from Utils import millisec

draw = Draw(500, 700, Dicts.colorsDict)
bardak = Bardak(15, 30, 9)
draw.draw_bardak(bardak)

cycle_msec = 50  # длительность одно цикла миллисекунд
down_msec = 500  # количество миллисекунд на опускание фигуры на одноу линию
down_msec_current = down_msec


def rnd_fig():
    t = random.randrange(len(Dicts.figures))
    angle = random.randrange(4)
    return Figure(t, angle, 0, (bardak.width - len(Dicts.figures[t][angle][0])) // 2, Dicts.figures[t])


def next_row_fig(figure):
    return Figure(figure.type, figure.angle, figure.row + 1, figure.col, figure.matrix)


def move_figure(figure, key):
    if key == "Up":
        return Figure(figure.type, (figure.angle + 1) % 4, figure.row, figure.col, figure.matrix)
    elif key == "Left":
        return Figure(figure.type, figure.angle, figure.row, figure.col - 1, figure.matrix)
    elif key == "Right":
        return Figure(figure.type, figure.angle, figure.row, figure.col + 1, figure.matrix)


current_figure = None
last_down_time = None
while True:
    mstart = millisec()

    if not current_figure:
        print("new figure")
        current_figure = rnd_fig()
        try:
            bardak.try_figure(current_figure)
        except CouldNotApplyFigure as e:
            # game over
            break
        draw.draw_figure(current_figure)
        last_down_time = millisec()
    else:
        if millisec() - last_down_time > down_msec_current:
            print("down")
            f = next_row_fig(current_figure)
            try:
                bardak.try_figure(f)
                draw.clear_figure(current_figure)
                current_figure = f
                draw.draw_figure(f)
                last_down_time = millisec()
            except CouldNotApplyFigure as e:
                lines = bardak.save_figure_and_return_filled_lines(current_figure)
                for line in lines:
                    bardak.drop_line(line)
                    draw.drop_line(bardak, line)
                current_figure = None
                down_msec_current = down_msec

    draw.win.update()
    key = draw.win.lastKey
    if key != "":
        print("key=", key)
        draw.win.lastKey = ""
        if current_figure:
            if key == "Down":
                down_msec_current = 0
            else:
                f = move_figure(current_figure, key)
                if f:
                    try:
                        bardak.try_figure(f)
                        draw.clear_figure(current_figure)
                        current_figure = f
                        draw.draw_figure(f)
                    except CouldNotApplyFigure as e:
                        pass

    mrest = millisec() - mstart
    # print("rest", mrest)
    if 0 < mrest < cycle_msec:
        time.sleep((cycle_msec - mrest) / 1000)
