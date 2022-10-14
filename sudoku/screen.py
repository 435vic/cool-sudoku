"""Clases para la renderización y administración de pantallas de tamaño completo en la consola."""
# pylint: disable=too-many-statements,too-many-branches

import sys
import time
from .terminal import get_terminal
from .sudoku import Sudoku
from .utils import is_key_directional, format_time, pause
from .characters import CHAR_FONTS, SUDOKU_TITLE_INGAME, SUDOKU_TITLE_SMALL

term = get_terminal()

class SudokuScreen():
    """Pantalla principal con el juego de Sudoku."""
    def __init__(self, grade, difficulty):
        self.term_width = term.width
        self.term_height = term.height
        self.grade = grade
        self.difficulty = difficulty
        self.cursor_pos = (0, 0) # La posición del cursor respectivo a las celdas del Sudoku.
        # Bandera que indica si se editó una celda.
        # Se utiliza para que el número se guarde hasta mover el cursor o presionar enter.
        self.edited_cell = False
        # El tiempo de inicio. Se usará para medir el tiempo que toma el usuario en resolver el Sudoku
        # Se empezará a medir en cuanto se genere el Sudoku
        self.start_time = None # None indica que el sudoku no se ha generado
        # Si el Sudoku fue completado
        self.completed = False
        # Si verificar los números al presionar una tecla
        self.show_feedback = False
        # El sudoku
        self.sudoku = Sudoku(grade, difficulty)
        (sudoku_width, sudoku_height) = self.sudoku.rendered_size()
        # Esta variable guarda la posición de la esquina superior izquierda del Sudoku.
        # La posición default es exactamente en el centro de la pantalla
        self.sudoku_home = (
            (self.term_width - sudoku_width) // 2,
            (self.term_height - sudoku_height) // 2
        )

    def get_time(self):
        """Obtiene el tiempo transcurrido en segundos desde que se empezó el sudoku."""
        if self.start_time is None: # El sudoku no se ha generado, el tiempo es cero
            return 0
        return int(time.time()) - self.start_time

    def get_formatted_time(self):
        """Retorna el tiempo transcurrido del Sudoku en un formato legible."""
        return format_time(self.get_time())

    def render(self):
        """Ciclo principal de la pantalla. Dibuja el tablero y otros elementos a la pantalla."""
        with term.fullscreen(), term.cbreak():
            self.draw_sudoku(numbers=False) # Dibujamos sólo la cuadrícula
            self.draw_subtitle('Cargando...')
            # Generamos un nuevo sudoku aleatorio, quitamos el mensaje de cargar, y actualizamos la pantalla
            self.sudoku.generate_sudoku()
            # Se terminó de generar, y el usuario podrá empezar a editarlo. Empezamos el tiempo
            self.start_time = int(time.time())
            self.clear_subtitle()
            self.draw_sudoku(grid=False) # Dibujamos sólo los números del Sudoku
            # Mover el cursor a la primera celda modificable, para el punto de partida del cursor
            col, row = self.sudoku.get_next_modifiable_cell(0, 0, 1, True)
            self.cursor_pos = [col, row]
            # Calculamos las coordenadas reales del cursor si estuviera en la celda que calculamos
            col, row = self.calc_cursor_pos(col, row)
            sys.stdout.write(term.move_xy(col, row))
            # Dibujar título
            self.draw_title()
            self.draw_controls()

            while True:
                # Si se completó el sudoku salir
                if self.completed:
                    return
                # En caso de que la consola cambió de tamaño volvemos a dibujar todo
                if self.changed_size():
                    sys.stdout.write(term.clear)
                    # Actualizar la variable con la posición del sudoku
                    sudoku_width, sudoku_height = self.sudoku.rendered_size()
                    self.sudoku_home = (
                        (self.term_width - sudoku_width) // 2,
                        (self.term_height - sudoku_height) // 2
                    )
                    # Dibujar título
                    self.draw_title()
                    # Dibujar controles
                    self.draw_controls()
                    self.draw_sudoku()
                    col, row = self.cursor_pos
                    x, y = self.calc_cursor_pos(col, row)
                    sys.stdout.write(term.move_xy(x, y))

                # Renderizar el mensaje de abajo
                self.render_status_bar()

                ##### CONTROLES #####
                # Esta sección se dedica a lidiar con las teclas del usuario, para manipular e interactuar con el juego
                key = term.inkey(1) # Si nada se presiona, la pantalla se refrescará cada segundo
                # Si la tecla presionada es un número, sea del teclado principal o el keypad
                if (n := key).isnumeric() or (n := key).replace('KEY_KP_', '').isnumeric():
                    num = int(n)
                    if num > self.sudoku.size:
                        continue # El número está fuera de rango
                    col, row = self.cursor_pos
                    # Cambiar el número en el tablero si es modificable
                    self.sudoku.content[row][col] = num
                    self.sudoku.correct[row][col] = None
                    self.edited_cell = True
                    # Dibujamos el número
                    self.write_number(num)
                # Este caso trata con el movimiento del cursor
                elif is_key_directional(key):
                    self.update_numbers(col, row)
                    col, row = self.handle_move(key)
                    # Hacemos flush para que el cursor se mueva immediatamente, y no tengamos que renderizar todo
                    # el tablero cada vez que cambiemos celda
                    self.move_cursor_to(col, row, flush=True)
                # En caso de presionar Backspace o Delete, borrar la celda y actualizar el estado interno
                elif key.code in (term.KEY_BACKSPACE, term.KEY_DELETE):
                    col, row = self.cursor_pos
                    # Cambiar el número en el tablero si es modificable
                    if self.sudoku.given[row][col] == 0:
                        self.sudoku.content[row][col] = 0
                    self.write_number(0)
                    self.edited_cell = True
                    self.update_numbers(col, row)
                # Shift+Delete borra todo el tablero, regresándolo a su estado inicial
                elif key.code == term.KEY_SDC:
                    # Borrar todo el tablero
                    for i in range(self.sudoku.size):
                        for j in range(self.sudoku.size):
                            self.sudoku.content[i][j] = self.sudoku.given[i][j]
                            self.sudoku.correct[i][j] = None
                    # Redibujar
                    self.draw_sudoku(grid=False)
                # La tecla Enter guarda el valor de la celda y comunica si estaba correcto o incorrecto
                elif key.code == term.KEY_ENTER:
                    self.update_numbers(col, row)
                    col, row = self.cursor_pos
                    # col, row = self.sud.get_next_modifiable_cell(col, row, 1)
                    # self.move_cursor_to(col, row, flush=True)
                # La tecla q o Escape sale del juego
                elif key == 'q' or key.code == term.KEY_ESCAPE:
                    break
                else:
                    # Si nada se presiona, no es necesario checar algo
                    continue

                if not self.show_feedback and self.check_full() and self.sudoku.is_solved():
                    self.on_completion()

        self.stop()

    def render_status_bar(self):
        """Dibuja el texto de la barra de abajo, con información sobre el sudoku, su dificultad y el tiempo transcurrido."""
        difficulty = 'Fácil'
        if self.sudoku.difficulty >= .75:
            difficulty = 'Difícil'
        elif self.sudoku.difficulty >= .5:
            difficulty = 'Intermedio'
        subtitle = f"{self.sudoku.size}x{self.sudoku.size} | Dificultad: {difficulty} | {self.get_formatted_time()}"
        self.draw_subtitle(term.dimgray(subtitle))

    def render_controls(self):
        """Dibuja un área que muestra los controles del juego."""


    def check_full(self):
        """Verifica si el tablero está lleno. Esta función está semi optimizada para su uso constante."""
        # Tenemos dos punteros, uno al principio y uno al final
        # Cada ciclo se acercan al centro, y apuntan a dos celdas de ambos lados
        # Esto divide a la mitad el tiempo requerido para verificar en el peor caso
        for i in range((self.sudoku.size**2)//2):
            s = self.sudoku.size
            j = self.sudoku.size - 1 - i
            c1 = self.sudoku.content[i//s][i%s]
            c2 = self.sudoku.content[j//s][j%s]
            if c1 == 0 or c2 == 0:
                return False
        return True

    def update_numbers(self, col, row):
        """Actualizar los números y si están correctos o no."""
        # Revisar números, colorear números correctos/incorrectos si es necesario
        # Sólo sucede si se editó un número
        if self.edited_cell and self.show_feedback:
            self.sudoku.update_conflicts(col, row)
            self.draw_sudoku(grid=False)
            self.edited_cell = False # Resetear bandera

    def write_number(self, n):
        """Escribe el número proporcionado en la celda seleccionada."""
        # Dibujamos el número
        with term.location(), term.hidden_cursor():
            col, row = self.cursor_pos
            if self.sudoku.given[row][col] == 0:
                sys.stdout.write(str(n) if n else ' ')

    def handle_move(self, key):
        """Mueve el cursor de acuerdo a la tecla del teclado presionada."""
        (x, y) = self.cursor_pos
        # flecha: mover celda
        if key.code == term.KEY_UP or key == 'w':
            y = (y - 1) % self.sudoku.size
        elif key.code == term.KEY_DOWN or key == 's':
            y = (y + 1) % self.sudoku.size
        elif key.code == term.KEY_LEFT or key == 'a':
            x = (x - 1) % self.sudoku.size
        elif key.code == term.KEY_RIGHT or key == 'd':
            x = (x + 1) % self.sudoku.size
        # Shift + flecha: Buscar la siguiente celda editable
        elif key.code == term.KEY_SUP or key == 'W':
            x, y = self.sudoku.get_next_modifiable_cell(x, y, 0)
        elif key.code == term.KEY_SRIGHT or key == 'D':
            x, y = self.sudoku.get_next_modifiable_cell(x, y, 1)
        elif key.code == term.KEY_SDOWN or key == 'S':
            x, y = self.sudoku.get_next_modifiable_cell(x, y, 2)
        elif key.code == term.KEY_SLEFT or key == 'A':
            x, y = self.sudoku.get_next_modifiable_cell(x, y, 3)

        return x, y

    def move_cursor_to(self, x, y, flush=False):
        """Mueve el cursor a la celda (x, y), calculando su posición real y haciendo flush a la consola si es especificado."""
        self.cursor_pos = [x, y]
        col, row = self.calc_cursor_pos(x, y)
        sys.stdout.write(term.move_xy(col, row))
        if flush:
            sys.stdout.flush()

    def draw_sudoku(self, grid=True, numbers=True):
        """Renderiza el tablero de Sudoku a la pantalla."""
        with term.location(), term.hidden_cursor():
            (sudoku_width, sudoku_height) = self.sudoku.rendered_size()
            with term.hidden_cursor():
                # Imprimir un error si el tablero de sudoku no cabe en la consola
                if sudoku_height > self.term_height or sudoku_width > self.term_width:
                    sys.stdout.write(term.home + term.clear + term.move_down(term.height//2 - 1))
                    sys.stdout.write(term.center(term.red('ERROR ') + 'La consola es demasiado pequeña para dibujar el tablero.'))
                    sys.stdout.write(term.center(f'Favor de extender la consola al menos {sudoku_height-self.term_height} filas'))
                    sys.stdout.flush()
                    time.sleep(1)
                    return
            if self.changed_size():
                # Las dimensiones de la consola cambiaron, volver a dibujar
                sys.stdout.write(term.clear)
            if grid:
                sys.stdout.write(term.home)
                sys.stdout.write(term.move_down(self.sudoku_home[1]))
                # Imprimir tablero vacío
                for line in self.sudoku.render(show_nums=False):
                    sys.stdout.write('\r' + term.move_right(self.sudoku_home[0]) + line + '\n')

            if numbers:
                # Mover el cursor a la primera celda
                sys.stdout.write(term.home)
                # Esta variable guardará si todos las celdas están llenas
                full = True
                for i in range(self.sudoku.size):
                    for j in range(self.sudoku.size):
                        (cell_x, cell_y) = self.calc_cursor_pos(j, i)
                        sys.stdout.write(term.move_xy(cell_x, cell_y))
                        # Mantener un inventario de las celdas, para checar si todo el tablero está correcto
                        cell_correct = self.sudoku.correct[i][j]
                        # Verificar si la celda no está vacía
                        full = full and self.sudoku.content[i][j] != 0
                        # Es el número en esta celda uno predeterminado o escrito por el usuario?
                        if (n := self.sudoku.given[i][j]) == 0:
                            n = self.sudoku.content[i][j]
                            color = term.normal
                            if cell_correct is True and self.show_feedback:
                                color = term.palegreen
                            elif cell_correct is False and self.show_feedback:
                                color = term.lightcoral
                            sys.stdout.write(color + CHAR_FONTS['alpha'][n] + term.normal)
                        else:
                            color = term.slategray4
                            if cell_correct is False and self.show_feedback:
                                color = term.firebrick4
                            sys.stdout.write(color + CHAR_FONTS['alpha'][n] + term.normal)

                if full:
                    if self.sudoku.is_solved():
                        with term.hidden_cursor():
                            self.on_completion()

            sys.stdout.flush()

    def on_completion(self):
        """Dibuja el sudoku todo verde y lo marca como completado."""
        # Imprimir tablero verde
        sys.stdout.write(term.home)
        sys.stdout.write(term.move_down(self.sudoku_home[1]))
        for line in self.sudoku.render():
            # Regresar al principio de la línea, llegar hasta la coordenada x del sudoku, e imprimir
            sys.stdout.write('\r' + term.move_right(self.sudoku_home[0]) + term.green(line) + '\n')
        # finish_time = self.get_time()
        pause()
        self.completed = True

    def draw_number(self, n):
        """Dibuja un número en la celda seleccionada."""
        sys.stdout.write(n)

    def draw_title(self):
        """Dibuja el título de Sudoku en la pantalla"""
        title_height = len(SUDOKU_TITLE_INGAME.splitlines())
        with term.location(), term.hidden_cursor():
            if title_height <= (self.sudoku_home[1]) - 1:
                sys.stdout.write(term.home)
                sys.stdout.write(term.move_down((self.sudoku_home[1]//2 - title_height//2) - 1))
                for line in SUDOKU_TITLE_INGAME.splitlines():
                    sys.stdout.write(term.center(line))
                sys.stdout.flush()

    def draw_subtitle(self, text):
        """Dibuja un texto de subtítulo en la parte inferior de la pantalla."""
        with term.location(), term.hidden_cursor():
            # El texto debe de estar a la mitad del espacio entre el sudoku y el borde inferior de la consola
            x_pos = term.height - (term.height - self.sudoku.rendered_size()[1])//4 - 1
            sys.stdout.write(term.home + term.move_down(x_pos))
            sys.stdout.write(term.center(text))
            sys.stdout.flush()

    def draw_controls(self):
        """Renderiza los controles del juego a la pantalla en caso de que quepa."""
        controls_height = len(controls_text.splitlines())
        # Conseguir la línea del texto con la mayor cantidad de caracteres
        controls_width = len(max(controls_text.splitlines(), key=len))
        sudoku_width, _ = self.sudoku.rendered_size()
        free_space_start = self.sudoku_home[0]+sudoku_width
        free_space = self.term_width-(free_space_start)
        if controls_width <= (free_space) and controls_height <= self.term_height:
            with term.location():
                sys.stdout.write(term.home+term.move_down((self.term_height-controls_height)//2))
                controls_start = free_space_start + (free_space-controls_width)//2
                for line in controls_text.splitlines():
                    sys.stdout.write(term.move_right(controls_start) + line + '\n')
                sys.stdout.flush()


    def clear_subtitle(self):
        """Borra el subtítulo de la pantalla."""
        with term.location(), term.hidden_cursor():
            x_pos = term.height - (term.height - self.sudoku.rendered_size()[1])//4
            sys.stdout.write(term.home + term.move_down(x_pos))
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
        return (x*4 + self.sudoku_home[0]+2, y*2 + self.sudoku_home[1]+1)

    # pylint: disable=missing-function-docstring
    def stop(self):
        pass
        # print("done!")

controls_text = f"""
┏━━━━━━━━━━━━━━━━━┓
┃    Controles    ┃
┗━━━━━━━━━━━━━━━━━┛
{term.dimgray}
←↑↓→ | wasd      cambiar celda
del | backspace  borrar celda
Shift + wasd     siguiente celda
Shift + del      borrar
q                salir
{term.normal}"""[1:]

credit_text = f"""
por Victor Quintana - A10643020@tec.mx

Este programa fue creado por Victor Quintana para la clase de Pensamiento Computacional para Ingeniería.
Todos los archivos y ejecutables dentro de la carpeta raíz de este proyecto están bajo la licencia MIT,
como especificada en el archivo LICENSE.

Se usó la librería blessed para la manipulación de la consola:
{term.link('https://github.com/jquast/blessed', 'Blessed en GitHub')}
"""

class CreditsScreen:
    """Créditos del programa."""
    def render(self):
        """Dibujar los créditos."""
        with term.location(), term.hidden_cursor(), term.cbreak(), term.fullscreen():
            print(term.home + term.clear)
            for line in SUDOKU_TITLE_SMALL.splitlines():
                print(term.center(line))
            for line in credit_text.splitlines():
                print(term.center(line))
            term.inkey()

rules_text = r"""
#############################
¿CÓMO JUGAR SUDOKU?
#############################

El Sudoku es un juego de lógica. Consiste en un tablero de 9 por 9 celdas,
donde pueden existir números del 1 al 9. El objetivo es llenar el tablero,
de manera que ninguna celda quede vacía. Sin embargo, no es tan simple como
parece, ya que cada celda tiene que cumplir con tres reglas fundamentales:

1. No se pueden repetir números en el mismo renglón.
2. No se pueden repetir números en la misma columna
3. No se pueden repetir números dentro del mismo cuadrado 3 por 3.
"""

class RulesScreen:
    """Reglas del Sudoku."""
    def render(self):
        """Dibujar las reglas del Sudoku."""
        with term.location(), term.hidden_cursor(), term.cbreak(), term.fullscreen():
            print(term.home + term.clear)
            for line in rules_text.splitlines():
                print(term.center(line))
            term.inkey()
