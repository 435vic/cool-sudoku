from terminal import get_terminal
import sys
from sudoku import Sudoku
from utils import is_key_directional
from characters import CHAR_FONTS

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
                self.draw_sudoku(numbers=False)
                self.draw_subtitle('Cargando...')
                # Generamos un nuevo sudoku aleatorio, quitamos el mensaje de cargar, y actualizamos la pantalla
                self.sud.generate_sudoku()
                self.clear_subtitle()
                self.draw_sudoku(grid=False)
                # Mover el cursor a la primera celda modificable
                col, row = self.sud.get_next_modifiable_cell(0, 0, 1, True)
                self.cursor_pos = [col, row]
                col, row = self.calc_cursor_pos(col, row)
                sys.stdout.write(term.move_xy(col, row))
                sys.stdout.flush()

            while True:
                if (self.changed_size()):
                    sys.stdout.write(term.clear)
                    self.draw_sudoku()

                key = term.inkey()
                # Si la tecla presionada es un número, sea del teclado principal o el keypad
                if (n := key).isnumeric() or (n := key).replace('KEY_KP_', '').isnumeric():
                    x, y = self.cursor_pos
                    # Cambiar el número en el tablero si es modificable
                    if self.sud.given[y][x] == 0:
                        self.sud.content[y][x] = int(n)
                        self.sud.correct[y][x] = None
                    else:
                        continue
                elif is_key_directional(key):
                    x, y = self.handle_move(key)
                    # Hacemos flush para que el cursor se mueva immediatamente, y no tengamos que renderizar todo
                    # el tablero cada vez que cambiemos celda
                    self.move_cursor_to(x, y, flush=True)
                    continue # esto se salta self.draw_sudoku()
                elif key.code == term.KEY_BACKSPACE or key.code == term.KEY_DELETE:
                    x, y = self.cursor_pos
                    # Cambiar el número en el tablero si es modificable
                    if self.sud.given[y][x] == 0:
                        self.sud.content[y][x] = 0
                elif key.code == term.KEY_SDC:
                    # Borrar todo el tablero
                    for i in range(self.sud.size):
                        for j in range(self.sud.size):
                            self.sud.content[i][j] = self.sud.given[i][j]
                    self.draw_sudoku()
                elif key.code == term.KEY_ENTER:
                    x, y = self.cursor_pos
                    x, y = self.sud.get_next_modifiable_cell(x, y, 1)
                    self.move_cursor_to(x, y, flush=True)
                    continue # esto se salta self.draw_sudoku()
                elif key == 'q' or key.code == term.KEY_ESCAPE:
                    break
                else:
                    # Si cualquier otra tecla es presionada, regresar al principio del loop (para ahorrarnos
                    # dibujar el sudoku cuando nadia haya cambiado)
                    continue

                # Sólo es necesario renderizar los números
                self.draw_sudoku(grid=False)


        self.stop()

    def handle_move(self, key):
        (x, y) = self.cursor_pos
        # Revisar números, colorear números correctos/incorrectos si es necesario
        if self.sud.update_conflicts(x, y):
            self.draw_sudoku(grid=False)
        # flecha: mover celda
        if key.code == term.KEY_UP or key == 'w':
            y = (y - 1) % self.sud.size
        elif key.code == term.KEY_DOWN or key == 's':
            y = (y + 1) % self.sud.size
        elif key.code == term.KEY_LEFT or key == 'a':
            x = (x - 1) % self.sud.size
        elif key.code == term.KEY_RIGHT or key == 'd':
            x = (x + 1) % self.sud.size
        # Shift + flecha: Buscar la siguiente celda editable
        elif key.code == term.KEY_SUP or key == 'W':
            x, y = self.sud.get_next_modifiable_cell(x, y, 0)
        elif key.code == term.KEY_SRIGHT or key == 'D':
            x, y = self.sud.get_next_modifiable_cell(x, y, 1)
        elif key.code == term.KEY_SDOWN or key == 'S':
            x, y = self.sud.get_next_modifiable_cell(x, y, 2)
        elif key.code == term.KEY_SLEFT or key == 'A':
            x, y = self.sud.get_next_modifiable_cell(x, y, 3)

        return x, y

    def move_cursor_to(self, x, y, flush=False):
        """Mueve el cursor a la celda (x, y)."""
        self.cursor_pos = [x, y]
        col, row = self.calc_cursor_pos(x, y)
        sys.stdout.write(term.move_xy(col, row))
        if flush:
            sys.stdout.flush()

    def draw_sudoku(self, grid=True, numbers=True):
        """Renderiza el tablero de Sudoku a la pantalla."""
        with term.location():
            if self.changed_size():
                # Las dimensiones de la consola cambiaron, volver a dibujar
                sys.stdout.write(term.clear)
            (sudoku_width, sudoku_height) = self.sud.rendered_size()
            
            if grid:
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
            
            if numbers:
                # Mover el cursor a la primera celda
                sys.stdout.write(term.home)
                for i in range(self.sud.size):
                    for j in range(self.sud.size):
                        (cell_x, cell_y) = self.calc_cursor_pos(j, i)
                        sys.stdout.write(term.move_xy(cell_x, cell_y))
                        # Es el número en esta celda uno predeterminado o escrito por el usuario?
                        if (n := self.sud.given[i][j]) == 0:
                            n = self.sud.content[i][j]
                            color = term.normal
                            if self.sud.correct[i][j] == True:
                                color = term.palegreen
                            elif self.sud.correct[i][j] == False:
                                color = term.lightcoral
                            sys.stdout.write(color + CHAR_FONTS['alpha'][n] + term.normal)
                        else:
                            color = term.slategray4
                            if self.sud.correct[i][j] == False:
                                color = term.firebrick4
                            sys.stdout.write(color + CHAR_FONTS['alpha'][n] + term.normal)

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
