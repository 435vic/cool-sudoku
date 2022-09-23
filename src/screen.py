from terminal import get_terminal
import sys
from sudoku import Sudoku
from time import sleep

term = get_terminal()

class SudokuScreen():
    def render(self):
        with term.fullscreen(), term.hidden_cursor(), term.cbreak():
            self.sud = Sudoku(callback=self.on_cell_set)
            self.draw_sudoku(self.sud)
            term.inkey()
            self.sud.generate_sudoku()
            sys.stdout.write(term.home + term.green)
            self.draw_sudoku(self.sud)
            sys.stdout.write(term.normal)
            sys.stdout.flush()
            term.inkey()

        self.stop()

    def on_cell_set(self, a, b, c):
        sleep(.0001)
        self.draw_sudoku(self.sud)

    def draw_sudoku(self, board):
        """Renderiza el tablero de Sudoku a la pantalla."""
        (sudoku_width, sudoku_height) = board.rendered_size()
        sys.stdout.write(term.home + term.move_down((term.height - sudoku_height)//2))
        for line in board.render():
            sys.stdout.write(term.center(line))

        sys.stdout.flush()

    def stop(self):
        pass
        # print("done!")
