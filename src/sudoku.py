from characters import SUDOKU_FONTS

class Sudoku():
    """Tablero de Sudoku."""
    def __init__(self, grade=3):
        # 'nivel' del sudoku. Entre más alto, más grande y difícil el Sudoku.
        self.grade = grade
        # Tamaño total del sudoku, en celdas.
        self.size = self.grade**2

    def rendered_size(self):
        """Regresa el tamaño del tablero de Sudoku, en caracteres.
        
        Retorna:
        Una tupla, con la longitud y altura."""
        return (self.size*4+1, self.size*2+1)

    def render(self):
        """Retorna un string con el tablero de sudoku."""
        boxchars = SUDOKU_FONTS['double']
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
                        row[1] += boxchars['vline'][1] + ' '*3 
                    ###### línea vertical menor ######
                    else: 
                        # Si estamos en la primera fila, la intersección es ┯, si no, ┿
                        row[0] += boxchars['hdline'][0] if i == 0 else boxchars['cross'][2]
                        row[1] += boxchars['vline'][0] + ' '*3

                    row[0] += boxchars['hline'][1]*3

                ###### línea horizontal menor ######
                else:
                    # Si esta columna está en una línea vertical mayor, ┠ si es la primera o ╂ si no
                    row[0] += boxchars['vrline'][0] if j == 0 else boxchars['cross'][j%self.grade == 0]
                    row[1] += boxchars['vline'][j % self.grade == 0]
                    row[0] += boxchars['hline'][0]*3
                    row[1] += ' '*3
            
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
