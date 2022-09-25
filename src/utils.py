"""Funciones misceláneas de utilidad."""

from blessed import Terminal

def pad(text, length, alignment='center', pad_char=' '):
    """Le pone padding a un texto. Toma como argumentos el texto, la longitud deseada y la alineación,
       La cual puede ser `left`, `right` o `center`. Regresa el texto, con padding de `center` si el valor
       no es especificado o válido. El último argumento es el caracter con el que se desea espaciar el texto."""
    # El valor mímino es la longitud del texto
    if length < len(text): length = len(text)
    pad_text = pad_char*(length-len(text))
    if alignment == 'left':
        return text + pad_text
    elif alignment == 'right':
        return pad_text + text
    else:
        left_pad = pad_char * ((length-len(text))//2)
        right_pad = pad_char * (length-len(text)-len(left_pad))
        return left_pad + text + right_pad

def interpolate(n, out_start, out_end, in_start=0, in_end=1):
    """Mapea un rango de números a otro rango.

    Argumentos:
    in_start: El inicio del rango del número n
    in_end: El fin del rango del número n
    out_start: El inicio del rango de valores deseado
    out_end: El final del rango de valores deseado"""
    in_span = in_end-in_start
    out_span = out_end-out_start
    return ((((n-in_start) / in_span)) * out_span) + out_start

def is_key_directional(key):
    """Si una tecla proporcionada es direccional. Incluye las flechas y WASD."""
    term = Terminal()
    if key.is_sequence:
        return key.code in [term.KEY_UP, term.KEY_DOWN, term.KEY_LEFT, term.KEY_RIGHT]
    return key.lower() in ['w', 'a', 's', 'd']

def pause(prompt, timeout=None):
    """Pausa el programa hasta que una tecla es presionada. Equivalente al comando `pause` en Windows.

    Recibe un argumento `prompt` que es el texto que se imprimirá antes de esperar a una tecla.

    Opcionalmente, se puede proporcinar un `timeout` en segundos, que se esperará antes de continuar con el programa
    en caso de que no se reciban teclas."""
    term = Terminal()
    with term.cbreak(), term.hidden_cursor():
        print(prompt, end='', flush=True)
        term.inkey(timeout)
        print('') # Imprime un newline
 