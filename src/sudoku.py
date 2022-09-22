from characters import SUDOKU_FONTS


# ┏━━━┯━━━┯━━━┳━━━┯━━━┯━━━┳━━━┯━━━┯━━━┓
# ┃   │   │   ┃   │   │   ┃   │   │   ┃

# ┠───┼───┼───╂───┼───┼───╂───┼───┼───┫
# ┃   │   │   ┃   │   │   ┃   │   │   ┃
#  
# ┠───┼───┼───╂───┼───┼───╂───┼───┼───┫
# ┃   │   │   ┃   │   │   ┃   │   │   ┃

# ┣━━━┿━━━┿━━━╋━━━┿━━━┿━━━╋━━━┿━━━┿━━━┫
# ┃   │   │   ┃   │   │   ┃   │   │   ┃
 
# ┠───┼───┼───╂───┼───┼───╂───┼───┼───┫
# ┃   │   │   ┃   │   │   ┃   │   │   ┃

# ┠───┼───┼───╂───┼───┼───╂───┼───┼───┫
# ┃   │   │   ┃   │   │   ┃   │   │   ┃

# ┣━━━┿━━━┿━━━╋━━━┿━━━┿━━━╋━━━┿━━━┿━━━┫
# ┃   │   │   ┃   │   │   ┃   │   │   ┃

# ┠───┼───┼───╂───┼───┼───╂───┼───┼───┫
# ┃   │   │   ┃   │   │   ┃   │   │   ┃

# ┠───┼───┼───╂───┼───┼───╂───┼───┼───┫
# ┃   │   │   ┃   │   │   ┃   │   │   ┃

# ┗━━━┷━━━┷━━━┻━━━┷━━━┷━━━┻━━━┷━━━┷━━━┛

class Sudoku():
    """Tablero de Sudoku."""
    def __init__(self):
        pass

    def render(self):
        """Retorna un string con el tablero de sudoku."""
        boxchars = SUDOKU_FONTS['basic']
        # El tablero está compuesto de líneas mayores y menores. Las mayores suceden cada 3 celdas
        # y en los bordes externos, y las menores en el resto de las líneas.
        grid = []
        for i in range(9): # cada hilera de celdas
            # cada celda mide dos hileras de caracteres, y existe una extra en el final.
            row = ['', '']
            for j in range(9): # cada columna de celdas
                ###### línea horizontal mayor ######
                if i % 3 == 0:
                    ###### línea vertical mayor ######
                    if j % 3 == 0:
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
                    if j % 3 == 0:
                        # Si esta columna está en una línea vertical mayor, ┠ si es la primera o ╂ si no
                        row[0] += boxchars['vrline'][0] if j == 0 else boxchars['cross'][1]
                        row[1] += boxchars['vline'][1]
                    else:
                        row[0] += boxchars['cross'][0]
                        row[1] += boxchars['vline'][0]
                    
                    row[0] += boxchars['hline'][0]*3
                    row[1] += ' '*3
            
            row[0] += boxchars['urcorner'] if i == 0 else boxchars['vlline'][i%3 == 0]            
            row[1] += boxchars['vline'][1]

            grid.extend(row) 

        print('\n'.join(grid))


def main():
    sud = Sudoku()
    sud.render()

if __name__ == '__main__':
    main()
