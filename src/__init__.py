############################################
#                  Sudoku                  #
#           por Victor Quintana            #
#             a10643020@tec.mx             #
############################################

def main():
    from utils import pad
    from terminal import Select, get_terminal
    from screen import SudokuScreen
    from characters import get_title

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

            diff = Select({
                0: 'Fácil',
                .5: 'Intermedio',
                1: 'Difícil'
            }).prompt('Selecciona la dificultad: ', default=1)

            SudokuScreen(grade, diff).render()
            print(term.move_up(2) + term.clear_eos)
        elif option == 'creds':
            print(f"{term.home}{term.black_on_skyblue}{term.clear}")
            print("press 'q' to quit.")
            with term.cbreak():
                val = ''
                while val.lower() != 'q':
                    val = term.inkey(timeout=3)
                    if not val:
                        print("It sure is quiet in here ...")
                    elif val.is_sequence:
                        print("got sequence: {0}.".format((str(val), val.name, val.code)))
                    elif val:
                        print("got {0}.".format(val))
                print(f'bye!{term.normal}')
    
    


if __name__ == '__main__':
    main()
