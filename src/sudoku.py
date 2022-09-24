from characters import SUDOKU_FONTS, CHAR_FONTS
from random import shuffle, random
from utils import interpolate
from time import sleep

class Sudoku():
    """Tablero de Sudoku."""
    def __init__(self, grade=3, difficulty=0):
        # 'nivel' del sudoku. Entre más alto, más grande y difícil el Sudoku.
        self.grade = grade
        # Tamaño total del sudoku, en celdas.
        self.size = self.grade**2
        # Contenido del sudoku, una matrix del tamaño self.size, con números del 0 al 9. 0 representa una celda vacía.
        self.content = [[0 for _ in range(self.size)] for _ in range(self.size)]
        # Los números predeterminados del sudoku, no se pueden cambiar
        self.given = [[0 for _ in range(self.size)] for _ in range(self.size)]
        # Una matriz expresando si el número en dicha posición es correcto
        self.correct = [[None for _ in range(self.size)] for _ in range(self.size)]
        # La dificultad del sudoku, valor de 0 a 1, representando el porcentaje de celdas que estarán vacías al empezar.
        self.difficulty = interpolate(difficulty, .6, .74)

    def set_cell(self, col, row, n, delay=0):
        """Le asigna el valor n a la celda especificada por su columna y fila."""
        if delay:
            sleep(delay)
        self.content[row][col] = n

    def is_solved(self):
        """Revisar si el sudoku está resuelto."""
        solved = True
        for row in range(self.size):
            for col in range(self.size):
                cell = self.content[row][col]
                solved = solved and self.check_safe(col, row, cell) and cell != 0
        return solved

    def generate_sudoku(self):
        """Genera un sudoku nuevo, y su solución."""
        # Adaptado de https://www.geeksforgeeks.org/program-sudoku-generator/
        # Intentaré sólo usar los pasos proporcionados, sin mirar al código para ver si lo puedo lograr solo.

        # Following is the improved logic for the problem.
        # 1. Fill all the diagonal 3x3 matrices.
        # 2. Fill recursively rest of the non-diagonal matrices.
        #    For every cell to be filled, we try all numbers until
        #    we find a safe number to be placed.  
        # 3. Once matrix is fully filled, remove K elements
        #    randomly to complete game.

        # Pseudoalgoritmo función recursiva
        # for n in possibilities // números posibles, 1 al 9 normalmente
        #     if is_safe:
        #         safe_route = repeat_next_cell() // llamada a sí mismo
        #         if safe_route return true // si la ruta es segura y no causa errores, podemos salir
        #         if on_last_cell return true // si es la última celda y no hay errores ¡acabamos!
        #     // llegamos a este punto si sucedió algun error
        #     cell = 0 // borramos la celda, estábamos mal en algún otro lado
        #     return false // la ruta no fue segura

        # Paso 1: Llenar los cuadros diagonales
        for i in range(self.grade if self.grade > 2 else 1):
            self.fill_subsquare((i*self.grade)+i)

        # Paso 2: Resolver!!!
        self.recursive_solve(self.grade, 0)

        # Paso 3: Ahora que tenemos un tablero válido, podemos quitar números.
        for i in range(self.size):
            for j in range(self.size):
                if random() < self.difficulty:
                    self.content[i][j] = 0
                
                # Configuramos los números iniciales
                self.given[i][j] = self.content[i][j]

    def recursive_solve(self, col, row):
        """Resuelve el tablero de sudoku recursivamente, retornando verdadero al terminar."""
        for n in range(1, self.size+1):
            if self.check_safe(col, row, n):
                # Este numero está bien, ponerlo en el tablero
                self.set_cell(col, row, n)
                (next_col, next_row) = self.get_next_empty_cell(col, row)
                if next_col < 0 or next_row < 0:
                    # Esta celda es la última vacía, y la resolvimos ya! Hemos acabado :)
                    return True
                # Averiguamos un numero para esta celda, a la siguiente
                is_path_safe = self.recursive_solve(next_col, next_row)
                # El camino adelante fue el correcto! Terminamos
                if is_path_safe:
                    return True

        # La ruta tomada no fue correcta, tenemos que irnos para atrás
        self.set_cell(col, row, 0) # borrar la celda, estaba mal
        return False # Indicamos que hubo un error

    def check_safe(self, col, row, n):
        """Verifica si un número n cumple con las reglas del Sudoku al ser colocado en la celda (col, row).
        Esta función asume que el tablero está en un estado válido."""
        if col >= self.size or row >= self.size:
            raise Exception('Fuera de rango')
        # Revisar filas, columnas y cuadrados
        for cell_col, cell_row in self.get_neighbors(col, row):
            cell = self.content[cell_row][cell_col]
            # Verificar que la celda tiene un número, y si se repite
            if cell != 0 and cell == n:
                return False
        # Todas las pruebas se cumplieron, el número es seguro
        return True

    def get_neighbors(self, col, row):
        """Retorna todas las celdas que interactúan con la celda (col, row), es decir,
        todas las celdas en la misma fila, columna y subcuadrado."""
        out = []
        out.extend([(i, row) for i in range(self.size) if (i, row) != (col, row)])
        out.extend([(col, i) for i in range(self.size) if (col, i) != (col, row)])
        subsq = self.get_subsquare_cells(col, row)
        subsq.remove((col, row))
        out.extend(subsq)
        return out

    def update_conflicts(self, x, y):
        """Revisa el tablero en la posición (x, y) para determinar los números correctos e incorrectos.
        
        Regresa True si el número en (col, row) es incorrecto y se hicieron cambios, False en otro caso."""
        # Checar el número
        for col, row in self.get_neighbors(x, y) + [(x, y)]:
            cell = self.content[row][col]
            self.correct[row][col] = self.check_safe(col, row, cell)

        return True

    def get_next_empty_cell(self, col, row):
        """Regresa la posición de la siguiente celda vacía a la derecha, o al principio de la siguiente
        fila si se llegó al borde."""
        # Número de 0 a self.size^2, representando cada celda
        linear = row*self.size + col
        while linear < (self.size**2) - 1:
            linear += 1 # Siguiente celda
            (j, i) = (linear%self.size, linear//self.size)
            if self.content[i][j] == 0:
                return (j, i) # Celda vacía, retornar su columna y fila
        
        # No hay celdas vacías
        return (-1, -1)

    def get_next_modifiable_cell(self, col, row, direction, lazy=False):
        """Regresa la posición de la siguiente celda modificable por el usuario a la derecha, o al principio de la siguiente
        fila si se llegó al borde.
        
        Argumentos:
        col: columna.
        row: fila.
        direction: La dirección en la que buscar:
            - 0: arriba
            - 1: derecha
            - 2: abajo
            - 3: izquierda
        lazy: si es verdadero, permanecer en la celda proporcionada si ésta es válida. Falso por default."""
        
        if direction % 2 == 0: # Arriba y abajo
            forward = 1 if direction == 2 else -1
            if not lazy: row = (row + forward) % self.size
            i = 0
            while self.given[row][col] != 0:
                row = (row + forward) % self.size # Hacia arriba o abajo, dependiendo de la dirección
                if i > len(self.given): # Dimos una vuelta completa, no hay espacios disponibles en esta columna
                    col = (col + 1) % self.size
                    i = 0 # reseteamos el contador
                i += 1
            return col, row
        else: # Izquierda y derecha
            forward = 1 if direction == 1 else -1
            if not lazy: col = (col + forward) % self.size
            i = 0
            while self.given[row][col] != 0:
                col = (col + forward) % self.size
                if i > len(self.given): # Dimos una vuelta completa, no hay espacios disponibles en esta fila
                    row = (row + 1) % self.size
                    i = 0 # reseteamos el contador
                i += 1
            return col, row

    def get_subsquare_cells(self, col, row):
        """Proporciona las coordenadas de las celdas del cuadrado 3x3 en el que está la celda especificada."""
        out = []
        # Cambia las coordenadas a la esquina superior izquierda del subcuadrado donde está
        (sq_col, sq_row) = (col//self.grade*self.grade, row//self.grade*self.grade)
        for i in range(sq_row, sq_row+self.grade):
            for j in range(sq_col, sq_col+self.grade):
                out.append((j, i))

        return out

    def fill_subsquare(self, id):
        """Llena un cuadrado 3x3 con números aleatorios.
        
        Argumentos:
        id (int): El número de cuadro. Se cuenta de izquierda a derecha y luego de arriba a abajo. Empieza en cero."""
        # Calcular las coordenadas del cuadrado.
        (sq_col, sq_row) = ((id % self.grade)*self.grade, (id // self.grade) * self.grade)
        nums = list(range(1,self.size+1))
        shuffle(nums)
        for i in range(sq_row, sq_row+self.grade):
            for j in range(sq_col, sq_col+self.grade):
                (k, l) = (i-sq_row, j-sq_col)
                self.set_cell(j, i, nums[k*self.grade + l])

    def rendered_size(self):
        """Regresa el tamaño del tablero de Sudoku, en caracteres.
        
        Retorna:
        Una tupla, con la longitud y altura."""
        return (self.size*4+1, self.size*2+1)

    def render(self, show_nums=True):
        """Retorna un string con el tablero de sudoku.
        
        Argumentos:
        show_nums: si mostrar los números de la cuadrícula o no. Default es sí."""
        boxchars = SUDOKU_FONTS['double']
        numchars = CHAR_FONTS['alpha']
        # La lógica para renderizar esta cuadrícula inspirada en este repositorio: https://github.com/thisisparker/cursewords

        # El tablero está compuesto de líneas mayores y menores. Las mayores suceden cada 3 celdas
        # y en los bordes externos, y las menores en el resto de las líneas.
        grid = []
        for i in range(self.size): # cada hilera de celdas
            # cada celda mide dos hileras de caracteres (y cuatro columnas), y sobra una extra en el final en ambas dimensiones.
            row = ['', '']
            for j in range(self.size): # cada columna de celdas
                ###### línea horizontal mayor ######
                if i % self.grade == 0:
                    ###### línea vertical mayor ######
                    if j % self.grade == 0:
                        if j == 0: # primera columna
                            # Si es la primera fila, la primera columna es la esquina (┏). Si no, una intersección (┣)
                            row[0] += boxchars['ulcorner'] if i == 0 else boxchars['vrline'][1]
                        else: # el resto de las columnas
                            # Si estamos en la primera fila (borde superior), la columna es ┳, si no, ╋
                            row [0] += boxchars['hdline'][1] if i == 0 else boxchars['cross'][3]
                        # La fila de abajo está vacía por ahora
                    ###### línea vertical menor ######
                    else: 
                        # Si estamos en la primera fila, la intersección es ┯, si no, ┿
                        row[0] += boxchars['hdline'][0] if i == 0 else boxchars['cross'][2]

                    row[0] += boxchars['hline'][1]*3

                ###### línea horizontal menor ######
                else:
                    # Si esta columna está en una línea vertical mayor, ┠ si es la primera o ╂ si no
                    row[0] += boxchars['vrline'][0] if j == 0 else boxchars['cross'][j%self.grade == 0]
                    row[0] += boxchars['hline'][0]*3
                # La segunda fila tiene líneas verticales y espacios únicamente
                n = self.given[i][j]
                # Mostrar el número en la celda, o nada si es 0
                cell_content = f' {numchars[n] or " "} ' if show_nums else ' '*3
                row[1] += boxchars['vline'][j % self.grade == 0] + cell_content

            # Añadir la última columna (la extra)
            row[0] += boxchars['urcorner'] if i == 0 else boxchars['vlline'][i%self.grade == 0]            
            row[1] += boxchars['vline'][1]
            # Añadir las dos filas completadas a la cuadrícula
            grid.extend(row) 

        # Añadir la fila extra
        final_row = boxchars['llcorner']+boxchars['hline'][1]*3 \
            + ''.join([boxchars['huline'][(j+1)%self.grade==0]+boxchars['hline'][1]*3 for j in range(self.size-1)]) \
            + boxchars['lrcorner']

        grid.append(final_row)
        return grid


def main():
    sud = Sudoku()
    print('\n'.join(sud.render()))

if __name__ == '__main__':
    main()
