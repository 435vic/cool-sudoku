"""Módulo de utilidad que proporciona caracteres para la renderización del tablero del Sudoku.
Existen dos opciones: la básica y la doble, la cual cambia el estilo de las líneas."""

# Caracteres que representan gráficamente el tablero de sudoku.
# ┏━━━┯━━━┯━━━┳━━━┯━━━┯━━━┳━━━┯━━━┯━━━┓
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
# ┣━━━┿━━━┿━━━╋━━━┿━━━┿━━━╋━━━┿━━━┿━━━┫
# ┃   │   │   ┃   │   │   ┃   │   │   ┃
# ┠───┼───┼───╂───┼───┼───╂───┼───┼───┫
# ┃   │   │   ┃   │   │   ┃   │   │   ┃
# ┠───┼───┼───╂───┼───┼───╂───┼───┼───┫
# ┃   │   │   ┃   │   │   ┃   │   │   ┃
# ┗━━━┷━━━┷━━━┻━━━┷━━━┷━━━┻━━━┷━━━┷━━━┛

# Cada caracter necesario para renderizar el tablero.
# Contiene versiones marcadas y no marcadas, para indicar la división entre cuadrículas de 3 por 3.
SUDOKU_FONTS = {
    'basic': {
        'ulcorner': '┏', # Upper left corner
        'urcorner': '┓', # Upper right corner
        'llcorner': '┗', # Lower left corner
        'lrcorner': '┛', # Lower right corner
        'vline': ['│', '┃'], # Vertical line
        'hline': ['─', '━'], # Horizontal line
        'huline': ['┷', '┻'], # Horizontal (and) up line
        'hdline': ['┯', '┳'], # Horizontal (and) down line
        'vlline': ['┨', '┫'], # Vertical (and) left line
        'vrline': ['┠', '┣'], # Vertical (and) right line
        'cross': ['┼', '╂', '┿', '╋'] # Cross
    },
    'double': {
        'ulcorner': '╔',
        'urcorner': '╗',
        'llcorner': '╚',
        'lrcorner': '╝',
        'vline': ['│', '║'],
        'hline': ['─', '═'],
        'huline': ['╧', '╩'],
        'hdline': ['╤', '╦'],
        'vlline': ['╢', '╣'],
        'vrline': ['╟', '╠'],
        'cross': ['┼', '╫', '╪', '╬']
    }
}