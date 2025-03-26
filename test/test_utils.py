# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=import-error

import unittest
from sudoku import utils

class TestPadding(unittest.TestCase):

    def test_features(self):
        """Prueba la función bajo contextos normales. Verifica su funcionalidad."""
        self.assertEqual(
            utils.pad('TEST', 10, 'left'),
            'TEST      '
        )
        self.assertEqual(
            utils.pad('TEST', 10, 'right'),
            '      TEST'
        )
        self.assertEqual(
            utils.pad('TEST', 10, 'center'),
            '   TEST   '
        )

    def test_center_impar(self):
        self.assertEqual(utils.pad('AAA', 9), '   AAA   ')

    def test_center_asimetrico(self):
        self.assertEqual(utils.pad('TEST', 9, 'center'), '  TEST   ')

    def test_longitud_fuera_rango(self):
        for al in ['left', 'right', 'center']:
            self.assertEqual(utils.pad('TEST', 1, alignment=al), 'TEST')

    def test_alignment_invalido(self):
        self.assertEqual(utils.pad('TEST', 8, alignment='bogus'), utils.pad('TEST', 8, alignment='center'))

class TestInterpolate(unittest.TestCase):
    def test_interpolate(self):
        self.assertEqual(
            utils.interpolate(5, 0, 100, 0, 10), 50
        )

        self.assertEqual(
            utils.interpolate(25, 50, 100, 20, 40), 62.5
        )

class TestFormatTime(unittest.TestCase):
    def test_format(self):
        cases = {
            100: '1:40',
            61: '1:01',
            600: '10:00',
            3700: '1:01:40',
            0: '0:00',
            2: '0:02'
        }
        for (case, expected) in cases.items():
            self.assertEqual(utils.format_time(case), expected)

if __name__ == '__main__':
    unittest.main()
