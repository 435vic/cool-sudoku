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
