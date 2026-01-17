import unittest
from quadratic_equation import solution


class TestQuadraticEquation(unittest.TestCase):

    def test_two_real_roots(self):
        """Тест: два различных корня"""
        result = solution(1, 8, 15)
        self.assertAlmostEqual(result[0], -3.0, places=5)
        self.assertAlmostEqual(result[1], -5.0, places=5)

    def test_two_real_roots_reversed(self):
        """Тест: два корня в другом примере"""
        result = solution(1, -13, 12)
        self.assertAlmostEqual(result[0], 12.0, places=5)
        self.assertAlmostEqual(result[1], 1.0, places=5)

    def test_one_root(self):
        """Тест: один корень (d = 0)"""
        result = solution(-4, 28, -49)
        self.assertAlmostEqual(result[0], 3.5, places=5)

    def test_no_real_roots(self):
        """Тест: нет вещественных корней"""
        result = solution(1, 1, 1)
        self.assertEqual(result, "корней нет")

    def test_discriminant_zero_in_solution(self):
        """Тест: убедимся, что d=0 возвращает один элемент"""
        result = solution(1, -6, 9)  # (x-3)²
        self.assertEqual(len(result), 1)
        self.assertAlmostEqual(result[0], 3.0, places=5)

    def test_invalid_a_zero(self):
        """Тест: a = 0 - должно вызвать исключение"""
        with self.assertRaises(ValueError) as context:
            solution(0, 1, 1)
        self.assertEqual(
            str(context.exception),
            "Коэффициент 'a' не может быть нулём в квадратном уравнении.",
        )


if __name__ == "__main__":
    unittest.main()
