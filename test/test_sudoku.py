# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=import-error

import unittest
import random
from sudoku.sudoku import Sudoku
from sudoku.characters import CHAR_FONTS

class TestSudoku(unittest.TestCase):
    def test_gen_from_str(self):
        """Verifica que se puede generar un tablero a partir de un String."""
        print('\n\n', '='*10, 'TEST GENERACION DE SUDOKU', '='*10)
        # Hace la misma prueba tres veces por cada tamaño soportado de Sudoku
        for grade in [2, 2, 2, 3, 3, 3, 4, 4, 4]:
            size = grade**2
            nums = [random.randint(0, size) for _ in range(size**2)]
            grid = [[0 for _ in range(size)] for _ in range(size)]
            for (i, n) in enumerate(nums):
                col, row = i%size, i//size
                grid[row][col] = n
            source = ''.join([CHAR_FONTS['alpha'][n] for n in nums]).replace(' ', '.')
            sudoku = Sudoku.from_str(grade, source)
            print(f'String: {source}')
            print('Sudoku generado')
            print('\n'.join(sudoku.render()))
            self.assertEqual(grid, sudoku.content)
            self.assertEqual(grid, sudoku.given)

    def test_check_safe(self):
        """Revisa que el sudoku pueda correctamente detectar números incorrectos."""
        print('\n\n', '='*10, 'TEST CHECAR NUMERO SEGURO', '='*10)
        # Los casos de prueba.
        # Elemento 0: tablero
        # Elemento 1: grado del tablero
        # Elemento 2: Lista de pruebas.
        #     - Tupla con coordenadas
        #     - Número a insertar
        #     - Resultado esperado
        cases = (
            ['26..7.48331......957.34...21.....9...8..9..3...7.....57...52.948......57956.3..21', 3,
            [
                [(2, 0), 6, False],
                [(7, 3), 9, False],
                [(4, 5), 2, True]
            ]],
            ['53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79', 3,
            [
                [(4,4), 4, False],
                [(4,4), 1, False],
                [(4,4), 5, True],
            ]],
            ['43.2.2...14.....', 2,
            [
                [(2,0), 2, False],
                [(0,2), 2, True],
                [(2,3), 1, True]
            ]]
        )
        for case in cases:
            source = case.pop(0)
            grade = case.pop(0)
            sudoku = Sudoku.from_str(grade, source)
            render = '\n'.join(sudoku.render())
            print('Sudoku:', render, sep='\n')
            for test in case.pop(0):
                col, row = test.pop(0) # coordenadas
                num = test.pop(0) # número a probar
                expected = test.pop(0) # Resultado esperado de la función
                print(f'Colocar {num} en {col}, {row}, se espera {expected}: {sudoku.check_safe(col, row, num)}')
                self.assertEqual(sudoku.check_safe(col, row, num), expected,
                msg=f'Safe check failed on col {col}, row {row} with num {num} (expected {expected}, got {sudoku.check_safe(col, row, num)})\n{render}')

    def test_is_solved(self):
        """Verifica que la funcion `is_solved` del sudoku funciona y correctamente identifica tableros resueltos y no resueltos."""
        print('\n\n', '='*10, 'TEST SUDOKU RESUELTO', '='*10)
        cases = (
            ['534678912672195348198342567859761423426853791713924856961537284287419635345286179', 3, True],
            ['53467891267219534819834256785976142342685379171392485696.537284287419635345286179', 3, False],
            ['534678912672195348198342567859761423426853791713924856965537284287419635345286179', 3, False],
            ['4312123421433421', 2, True],
            ['1342143223412413', 2, False]
        )
        for case in cases:
            source = case.pop(0)
            grade = case.pop(0)
            sudoku = Sudoku.from_str(grade, source)
            render = '\n'.join(sudoku.render())
            expected = case.pop(0)
            solved = sudoku.is_solved()
            print(f'Sudoku resuelto (valor esperado): {expected}', render, sep='\n')
            print(f'Valor actual: {solved}')
            self.assertEqual(solved, expected, msg=render)
