from blessed import Terminal

def pad(text: str, length: int, alignment='center', pad_char=' '):
    """Le pone padding a un texto. Toma como argumentos el texto, la longitud deseada y la alineación,
       La cual puede ser `left`, `right` o `center`. Regresa el texto, con padding de `center` si el valor
       no es especificado o válido. El último argumento es el caracter con el que se desea espaciar el texto."""
    # El valor mímino es la longitud del texto
    if length < len(text): length = len(text)
    pad = pad_char*(length-len(text))
    if alignment == 'left':
        return text + pad
    elif alignment == 'right':
        return pad + text
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
