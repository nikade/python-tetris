from Exceptions import CouldNotApplyFigure


class Bardak:

    def __init__(self, width, height, border_color):
        self.width = width
        self.height = height
        self.border_color = border_color
        self.content = None
        self.clear()

    def clear(self):
        border_arr = [self.border_color]
        self.content = [border_arr + ([0] if i < self.height else border_arr) * self.width + border_arr \
                        for i in range(self.height + 1)]

    def try_figure(self, figure):
        self.apply_figure_and_return_filled_lines(figure, False)

    def save_figure_and_return_filled_lines(self, figure):
        return self.apply_figure_and_return_filled_lines(figure, True)

    def apply_figure_and_return_filled_lines(self, figure, need_save):
        new_rows = None
        if need_save:
            new_rows = self.content[figure.row:figure.row + len(figure.matrix[figure.angle])]
        for n_row, row in enumerate(figure.matrix[figure.angle]):
            for n_col, color in enumerate(row):
                if color:
                    if self.content[figure.row + n_row][n_col + figure.col + 1]:
                        raise CouldNotApplyFigure()
                    if new_rows:
                        new_rows[n_row][n_col + figure.col + 1] = color
        if new_rows:
            self.content[figure.row:figure.row + len(new_rows)] = new_rows
            return [n + figure.row for n, row in enumerate(new_rows) if not row.count(0)]
        return None

    def drop_line(self, row):
        self.content[1:row + 1] = self.content[0:row]
        self.content[0][1:self.width + 1] = [0] * self.width
