############################################
#                  Sudoku                  #
#           por Victor Quintana            #
#             a10643020@tec.mx             #
############################################

from utils import pad
from terminal import Select, get_terminal
from screen import SudokuScreen

def main():
    main_menu = Select([
        'Jugar Sudoku',
        'Reglas',
        'Opciones',
        'Créditos',
        'Salir'
    ]).set_prompt('Elige una opción: ')
    while True:
        option = main_menu.prompt(erase_after_use=True)
        if option in ['Salir', None]:
            print("Adiós!")
            return
        if option == 'Jugar Sudoku':
            SudokuScreen().render()
    
    


if __name__ == '__main__':
    main()
