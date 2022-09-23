from terminal import get_terminal
import sys
from sudoku import Sudoku

term = get_terminal()

class SudokuScreen():
    def render(self):
        with term.fullscreen(), term.hidden_cursor(), term.cbreak():
            sud = Sudoku()
            (sudoku_width, sudoku_height) = sud.rendered_size()
            sys.stdout.write(term.home + term.move_down((term.height - sudoku_height)//2))
            for line in sud.render():
                sys.stdout.write(term.center(line))

            sys.stdout.flush()
            term.inkey()
        self.stop()

    def stop(self):
        pass
        # print("done!")
