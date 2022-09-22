from terminal import get_terminal
import sys

term = get_terminal()

class Screen():
    """Un espacio separado a la pantalla principal, el cual tiene las dimensiones de la consola y puede ser manipulado.
    Clase abstracta."""

    def __init__(self):
        pass

    def render(self):
        self.start()
        self.stop()

    def start(self):
        raise NotImplementedError('Es obligatorio implementar esta función')

    def stop(self):
        raise NotImplementedError('Es obligatorio implementar esta función')

test = """
╔═══╤═══╤═══╦═══╤═══╤═══╦═══╤═══╤═══╗
║ 3 │ 4 │   ║   │   │   ║   │   │   ║
╚═══╧═══╧═══╩═══╧═══╧═══╩═══╧═══╧═══╝
""".splitlines()[1:]

class SudokuScreen(Screen):
    def __init__(self):
        super().__init__()
    
    def start(self):
        with term.fullscreen(), term.hidden_cursor(), term.cbreak():
            
            sys.stdout.write(term.move_yx(term.height//2, 0) + term.center(test[0]))
            sys.stdout.write(term.center(test[1]))
            sys.stdout.write(term.center(test[2]))

            sys.stdout.flush()
            term.inkey()

    def stop(self):
        print("done!")
