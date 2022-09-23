import unittest
from src.utils import pad, interpolate

class TestPadding(unittest.TestCase):

    def test_features(self):
        """Prueba la función bajo contextos normales. Verifica su funcionalidad."""
        self.assertEqual(
            pad('TEST', 10, 'left'),
            'TEST      '
        )
        self.assertEqual(
            pad('TEST', 10, 'right'),
            '      TEST'
        )
        self.assertEqual(
            pad('TEST', 10, 'center'),
            '   TEST   '
        )
    
    def test_center_impar(self):
        self.assertEqual(pad('AAA', 9), '   AAA   ')

    def test_center_asimetrico(self):
        self.assertEqual(pad('TEST', 9, 'center'), '  TEST   ')

    def test_longitud_fuera_rango(self):
        for al in ['left', 'right', 'center']:
            self.assertEqual(pad('TEST', 1, alignment=al), 'TEST')

    def test_alignment_invalido(self):
        self.assertEqual(pad('TEST', 8, alignment='bogus'), pad('TEST', 8, alignment='center'))

    def test_interpolate(self):
        self.assertEqual(
            interpolate(5, 0, 100, 0, 10), 50
        )

        self.assertEqual(
            interpolate(25, 50, 100, 20, 40), 62.5
        )


if __name__ == '__main__':
    unittest.main()
