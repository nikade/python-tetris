from graphics import *

from Utils import millisec


class Draw:
    def __init__(self, width, height, colors_dict):
        self.scoreProc = 30
        self.borderProc = 5
        self.blk = None
        self.bardak_y = None
        self.bardak_x = None
        self.width = width
        self.height = height
        self.colors_dict = colors_dict
        self.win = None
        self.init_windows()

    def init_windows(self):
        self.win = GraphWin("ТЕТЯIS", self.width, self.height)
        obj = Text(Point(260, 50), "ТЕТЯIS")
        obj.setSize(30)
        obj.setTextColor("red")
        obj.draw(self.win)

    def draw_bardak(self, bardak):
        self.blk = min(self.width * (100 - self.borderProc * 3 - self.scoreProc) // 100 // (bardak.width + 2),
                       self.height * (100 - self.borderProc * 2) // 100 // (bardak.height + 2))
        self.bardak_x = self.width * self.borderProc // 100 + \
                        (self.width * (100 - self.borderProc * 3 - self.scoreProc) // 100 - self.blk * (
                                bardak.width + 2)) // 2
        self.bardak_y = (self.height - self.blk * (bardak.height + 2)) // 2

        obj = Rectangle(Point(self.bardak_x, self.bardak_y),
                        Point(self.bardak_x + self.blk * (bardak.width + 2),
                              self.bardak_y + self.blk * (bardak.height + 1)))
        obj.setOutline("white")
        obj.setFill("white")
        obj.draw(self.win)
        for n_row, row in enumerate(bardak.content):
            for n_col, color in enumerate(row):
                if color:
                    self.__draw_box__(n_col, n_row, color)

    def __draw_box__(self, n_col, n_row, color):
        x = self.bardak_x + n_col * self.blk
        y = self.bardak_y + n_row * self.blk
        obj = Rectangle(Point(x, y), Point(x + self.blk, y + self.blk))
        obj.setOutline("white")
        obj.setFill(self.colors_dict[color])
        obj.draw(self.win)

    def clear_figure(self, figure):
        self.__draw_figure__(figure, True)

    def draw_figure(self, figure):
        self.__draw_figure__(figure, False)

    def __draw_figure__(self, figure, clear):
        for n_row, fig_row in enumerate(figure.matrix[figure.angle]):
            for n_col, color in enumerate(fig_row):
                if color:
                    self.__draw_box__(figure.col + n_col + 1, figure.row + n_row, 0 if clear else color)

    def drop_line(self, bardak, row):
        ## bardak - должен быть уже без строки
        ## todo мигание исчезающей строки
        for n_row in range(row, -1, -1):
            row = bardak.content[n_row]
            for n_col, color in enumerate(row):
                self.__draw_box__(n_col, n_row, color)
