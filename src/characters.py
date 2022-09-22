# Caracteres que representan gráficamente el tablero de sudoku.
# Esquina superior izquierda, esquina superior derecha, esquina inferior izquierda, esquina inferior derecha, linea horizontal, linea vertical
SUDOKU_FONTS = {
    'basic': {
        'vline': ['│', '┃'],
        'hline': ['─', '━'],
        'ulcorner': '┏',
        'urcorner': '┓',
        'llcorner': '┗',
        'lrcorner': '┛',
        'huline': ['┷', '┻'],
        'hdline': ['┯', '┳'],
        'vlline': ['┨', '┫'],
        'vrline': ['┠', '┣'],
        'cross': ['┼', '╂', '┿', '╋']
    },
    'double': {
        'vline': '║',
        'hline': '═',
        'ulcorner': '╔',
        'urcorner': '╗',
        'llcorner': '╚',
        'lrcorner': '╝',
        'huline': '╩',
        'hdline': '╦',
        'vlline': '╣',
        'vrline': '╠'
    }
}