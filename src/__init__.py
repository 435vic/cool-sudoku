############################################
#                  Sudoku                  #
#           por Victor Quintana            #
#             a10643020@tec.mx             #
############################################

from utils import pad, pause
from terminal import Select, get_terminal
from screen import SudokuScreen
from characters import get_title

def main():
    term = get_terminal()
    main_menu = Select({
        'sudoku': 'Jugar Sudoku',
        'reglas': 'Reglas',
        'opts': 'Opciones',
        'creds': 'Créditos',
        'quit': 'Salir'
    }).set_prompt('Elige una opción: ')
    print(get_title(term.width))

    while True:
        option = main_menu.prompt(erase_after_use=True)
        if option in ['quit', None]:
            print("Gracias por jugar!")
            return
        elif option == 'sudoku':
            grade = Select({
                3: '3 x 3 (Estándar)',
                2: '2 x 2 (Mini)',
                4: '4 x 4 (Loco)'
            }).prompt('Selecciona un tamaño: ')
            # Si la elección es cancelada regresar al principio
            if grade == None:
                pause('Presiona enter para continuar...')
                # Borra la línea que acabamos de imprimir y el prompt anterior
                print(term.move_up(2) + term.clear_eos, end='')
                continue
            diff = Select({
                0: 'Fácil',
                .5: 'Intermedio',
                1: 'Difícil'
            }).prompt('Selecciona la dificultad: ', default=1)
            # Si la elección es cancelada regresar al principio
            if diff == None:
                pause('Presiona enter para continuar...')
                # Borra la línea de pause y los dos prompts anteriores
                print(term.move_up(3) + term.clear_eos, end='')
                continue
            SudokuScreen(grade, diff).render()
            print(term.move_up(2) + term.clear_eos)

if __name__ == '__main__':
    main()
