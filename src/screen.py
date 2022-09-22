from terminal import get_terminal
import sys
from sudoku import Sudoku

term = get_terminal()

class Screen():
    """Un espacio separado a la pantalla principal, el cual tiene las dimensiones de la consola y puede ser manipulado.
    Clase abstracta."""

    def __init__(self):
        pass

    def render(self):
        self.start()
        self.stop()

    def start(self):
        raise NotImplementedError('Es obligatorio implementar esta función')

    def stop(self):
        raise NotImplementedError('Es obligatorio implementar esta función')


class SudokuScreen(Screen):
    def __init__(self):
        super().__init__()
    
    def start(self):
        with term.fullscreen(), term.hidden_cursor(), term.cbreak():
            sud = Sudoku()
            (sudoku_width, sudoku_height) = sud.rendered_size()
            sys.stdout.write(term.home + term.move_down((term.height - sudoku_height)//2))
            for line in sud.render():
                sys.stdout.write(term.center(line))

            sys.stdout.flush()
            term.inkey()

    def stop(self):
        print("done!")
