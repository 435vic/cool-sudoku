"""Clases de utilidad para la manipulación de la consola."""

from blessed import Terminal
term = Terminal()

# pylint: disable=missing-function-docstring
def get_terminal():
    return term

class Select:
    """Menú de selección.

    Argumentos:
    options (dict(str, str)): Diccionario de opciones. La llave representa una identificación, y el valor lo que se
    mostrará en esa opción.
    """

    def __init__(self, options):
        self.options = options
        self.index = 0
        self._text = None

    def render(self, selection=0):
        """Renderiza el menú de selección a la consola."""
        # Imprimir las opciones, añadiendo el cursor (>) en caso de que sea la seleccionada.
        for (idx, option) in enumerate(self.options.values()):
            cursor = '   ' if not idx == selection else term.aqua + ' > '
            print(cursor + option + term.normal)

    def render_help_message(self):
        """Imprime un mensaje de guía con los controles para el menú."""
        msg = "[↑↓ para seleccionar | esc para cancelar | enter para confirmar]"
        print('\n' + term.dimgray(msg))

    def set_prompt(self, text):
        """Configura el prompt del menú de selección, sin imprimirlo a la pantalla."""
        self._text = text
        return self

    def prompt(self, text='', default=0, erase_after_use=False):
        """Renderiza la lista de opciones con un prompt especificado.

        Argumentos:
        text (str): El prompt.
        default (int): El item que estará seleccionado al inicio (default: 0)
        erase_after_use (boolean): Si después de elegir la opción, dejar la línea con la selección (False) o eliminarla (True)

        Retorna: La opción seleccionada."""
        # Preparar la consola para recibir teclas individuales, y esconder el cursor
        with term.cbreak(), term.hidden_cursor():
            if self._text:
                text = self._text
            print(text)
            index = default
            self.render(index)
            self.render_help_message()

            while True:
                with term.location():
                    # Regresar al principio de la lista (tomando en cuenta el mensaje de ayuda)
                    print(term.move_up(len(self.options)+2), end='')
                    self.render(index)

                key = term.inkey(timeout=4)
                # mover el cursor, regresando al principio o al final si se excede la lista.
                if key.name == 'KEY_UP':
                    index = (index - 1) % len(self.options)
                elif key.name == 'KEY_DOWN':
                    index = (index + 1) % len(self.options)
                elif key.name == 'KEY_ENTER':
                    # Regresar al principio y reemplazar todo para sólo dejar la selección
                    print(term.move_up(len(self.options)+2+erase_after_use)+term.clear_eos, end='')
                    if not erase_after_use:
                        print(term.move_up() + term.move_right(len(text)) + term.aqua + list(self.options.values())[index] + term.normal)
                    return list(self.options.keys())[index]
                elif key.name == 'KEY_ESCAPE' or key == 'q':
                    # Regresar al principio y reemplazar todo para sólo dejar la selección
                    print(term.move_up(len(self.options)+2+erase_after_use)+term.clear_eos, end='', flush=True)
                    if not erase_after_use:
                        print(term.move_up() + term.move_right(len(text)) + term.red + 'Cancelado' + term.normal)
                    return None

if __name__ == '__main__':
    seleccion = Select({
        'a': 'Opción 1',
        'b': 'Opción 2',
        'c': 'Opción 3'
    }).prompt('Elige una opción: ', default=1)
    print(seleccion)

# term = Terminal()

# with term.cbreak(), term.hidden_cursor():
#     print("Testing!")
#     print("Testing!")
#     print("(press q to quit)", end='')
#     sys.stdout.flush()
#     while (val := term.inkey()).lower() != 'q':
#         pass
#     print((term.clear_bol+term.move_up)*3+"\n")
