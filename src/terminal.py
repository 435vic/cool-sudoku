import platform, os
import sys

def clear():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')
    
def get_terminal_size():
    try:
        size = os.get_terminal_size()
        return size
    except OSError:
        return None

def terminal_setup():
    """Preparar consola para el programa."""
    pass

class Position:
    """Clase de utilidad que representa la posición de un cursor, en columnas y filas.
    
    ## Atributos
    - row (int): La fila del cursor.
    - col (int): La columna del cursor.
    """
    def __init__(self, col=0, row=0):
        self.row = row
        self.col = col

# Inspirado por Inquire, una librería de Rust (copyright Mikael Mello) https://github.com/mikaelmello/inquire
class Viewport:
    """Representa un búfer de texto en la consola, el cual puede ser manipulado.
    
    Consiste de un búfer de texto y un cursor, el cual puede ser manipulado y renderizado a demanda.
    El cursor comienza en la posición (0,0), y el búfer tiene un tamaño inicial de cero.

    ## Atributos
    - buffer (str): El búfer de texto del viewport.
    - cursor (Position): La posición del cursor.
    - stream_in (TextIOBase): El stream de datos de donde conseguir datos (default: stdin)
    - stream_out (TextIOBase): El stream de datos para usar para la salida de datos (default: stdout)
    """

    def __init__(self, stream_in=sys.stdin, stream_out=sys.stdout):
        self._buffer = ""
        self.cursor = Position()
        self.end_position = Position()
        self.terminal_size = get_terminal_size()
        self.sin = stream_in
        self.sout = stream_out
    
    def write(self, text):
        """Escribe el texto proporcionado al stream de salida especificado."""
        self._buffer.push(text)
        self.sin.write(text)

    def update_position(self):
        """Actualiza el cursor y la posición final interna para que sea el final del texto.

        Esto toma en cuenta las líneas y las dimensiones físicas de la consola.
        """
        # Inicilizamos una posición en 0,0
        pos = Position()

        # Hacemos un bucle sobre los caracteres del búfer, actualizando la cursor cuando sea necesario.
        for (idx, c) in enumerate(self._buffer):
            # Nueva línea, cambiamos de fila y reseteamos la columna a 0
            if c == '\n':
                pos.row += 1
                pos.col = 0
            else:
                chars_left = self.terminal_size.columns - pos.col
                # Si excedemos la longitud de la consola, pasar a la siguiente fila
                if chars_left < 1:
                    pos.row += 1
                    pos.col = 0
                else:
                    pos.col += 1
        
        self.cursor = pos
        self.end_position = pos

    
    

