from terminal import get_terminal
import sys
from sudoku import Sudoku
from time import sleep

term = get_terminal()

class SudokuScreen():
    def __init__(self, grade, difficulty):
        self.term_width = term.width
        self.term_height = term.height
        self.grade = grade
        self.difficulty = difficulty
        self.cursor_pos = [0, 0]
        self.sud = Sudoku(grade, difficulty)

    def render(self):
        with term.fullscreen(), term.cbreak():
            with term.hidden_cursor():
                self.draw_sudoku()
                self.draw_subtitle('Cargando...')
                # Generamos un nuevo sudoku aleatorio, quitamos el mensaje de cargar, y actualizamos la pantalla
                self.sud.generate_sudoku()
                self.clear_subtitle()
                self.draw_sudoku()
                # Mover el cursor a la primera celda modificable
                col, row = self.sud.get_next_modifiable_cell(0, 0)
                self.cursor_pos = [col, row]
                col, row = self.calc_cursor_pos(col, row)
                sys.stdout.write(term.move_xy(col, row))
                sys.stdout.flush()

            while True:
                key = term.inkey()
                # Si la tecla presionada es un número, sea del teclado principal o el keypad
                if (n := key).isnumeric() or (n := key).replace('KEY_KP_', '').isnumeric():
                    x, y = self.cursor_pos

                    # Cambiar el número en el tablero si es modificable
                    if self.sud.given[y][x] == 0:
                        self.sud.content[y][x] = int(n)
                elif key == 'q':
                    break
                else:
                    # Si cualquier otra tecla es presionada, regresar al principio del loop (para ahorrarnos
                    # dibujar el sudoku cuando nadia haya cambiado)
                    continue
                    
                self.draw_sudoku()


        self.stop()

    def on_cell_set(self, a, b, c):
        self.draw_sudoku()

    def draw_sudoku(self):
        """Renderiza el tablero de Sudoku a la pantalla."""
        with term.location():
            if self.changed_size():
                # Las dimensiones de la consola cambiaron, volver a dibujar
                sys.stdout.write(term.clear)
            (sudoku_width, sudoku_height) = self.sud.rendered_size()
            sys.stdout.write(term.home)
            # Imprimir un error si el tablero de sudoku no cabe en la consola
            if sudoku_height > self.term_height or sudoku_width > self.term_width:
                sys.stdout.write(term.move_down(term.height//2 - 1))
                sys.stdout.write(term.center(term.red('ERROR ') + 'La consola es demasiado pequeña para dibujar el tablero.'))
                sys.stdout.write(term.center(f'Favor de extender la consola al menos {sudoku_height-self.term_height} filas'))
                sys.stdout.flush()
                return
            
            sys.stdout.write(term.move_down((term.height - sudoku_height)//2))
            # Imprimir tablero vacío
            for line in self.sud.render(show_nums=False):
                sys.stdout.write(term.center(line))
            # Mover el cursor a la primera celda
            sys.stdout.write(term.home)
            for i in range(self.sud.size):
                for j in range(self.sud.size):
                    (cell_x, cell_y) = self.calc_cursor_pos(j, i)
                    sys.stdout.write(term.move_xy(cell_x, cell_y))
                    # Es el número en esta celda uno predeterminado o escrito por el usuario?
                    if (n := self.sud.given[i][j]) == 0:
                        n = self.sud.content[i][j] or ' '
                        sys.stdout.write(str(n))
                    else:
                        sys.stdout.write(term.slategray4(str(n)))

            sys.stdout.flush()
    
    def draw_subtitle(self, text):
        with term.location():
            # El texto debe de estar a la mitad del espacio entre el sudoku y el borde inferior de la consola
            sys.stdout.write(term.home + term.move_down(term.height - (term.height - self.sud.rendered_size()[1])//4))
            sys.stdout.write(term.center(text))

    def clear_subtitle(self):
        with term.location():
            sys.stdout.write(term.home + term.move_down(term.height - (term.height - self.sud.rendered_size()[1])//4))
            sys.stdout.write(term.clear_eol)

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

    def calc_cursor_pos(self, x, y):
        """Regresa la posición del cursor si estuviera en la celda Sudoku x, y. La celda 0, 0 tiene la posición 0,0."""
        (sudoku_width, sudoku_height) = self.sud.rendered_size()
        return (x*4 + (term.width-sudoku_width)//2+2, y*2 + (term.height-sudoku_height)//2+1)

    def stop(self):
        pass
        # print("done!")
