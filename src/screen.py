from terminal import get_terminal
import sys
from sudoku import Sudoku
from time import sleep

term = get_terminal()

class SudokuScreen():
    def __init__(self):
        self.term_width = term.width
        self.term_height = term.height
        self.sud = Sudoku()

    def render(self):
        with term.fullscreen(), term.hidden_cursor(), term.cbreak():
            self.draw_sudoku()
            term.inkey()
            self.sud.generate_sudoku()
            sys.stdout.write(term.home + term.green)
            self.draw_sudoku()
            sys.stdout.write(term.normal)
            sys.stdout.flush()
            term.inkey()

        self.stop()

    def on_cell_set(self, a, b, c):
        self.draw_sudoku()

    def draw_sudoku(self):
        """Renderiza el tablero de Sudoku a la pantalla."""
        (sudoku_width, sudoku_height) = self.sud.rendered_size()
        sys.stdout.write(term.home)
        if self.changed_size():
            # Las dimensiones de la consola cambiaron, volver a dibujar
            sys.stdout.write(term.clear)
        sys.stdout.write(term.move_down((term.height - sudoku_height)//2))
        for line in self.sud.render():
            sys.stdout.write(term.center(line))

        sys.stdout.flush()

    def changed_size(self):
        """Verificar si cambió el tamaño de la consola."""
        w = term.width
        h = term.height
        if w != self.term_width or h != self.term_height:
            # Cambiaron, actualizar las variables y regresar verdadero
            self.term_width = w
            self.term_height = h
            return True
        # Las dimensiones no han cambiado
        return False


    def stop(self):
        pass
        # print("done!")
