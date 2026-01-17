import unittest
from check_triangle import check_triangle


class TestCheckTriangle(unittest.TestCase):

    def test_equilateral_triangle(self):
        """Тест: все стороны равны - равносторонний треугольник"""
        self.assertEqual(check_triangle(10, 10, 10), "Равносторонний треугольник")
        self.assertEqual(check_triangle(5, 5, 5), "Равносторонний треугольник")

    def test_isosceles_triangle(self):
        """Тест: две стороны равны - равнобедренный треугольник"""
        self.assertEqual(check_triangle(10, 10, 15), "Равнобедренный треугольник")
        self.assertEqual(check_triangle(10, 15, 10), "Равнобедренный треугольник")
        self.assertEqual(check_triangle(15, 10, 10), "Равнобедренный треугольник")

    def test_scalene_triangle(self):
        """Тест: все стороны разные, но треугольник существует - разносторонний"""
        self.assertEqual(check_triangle(3, 4, 5), "Разносторонний треугольник")
        self.assertEqual(check_triangle(7, 10, 12), "Разносторонний треугольник")

    def test_triangle_not_exists_by_inequality(self):
        """Тест: сумма двух сторон меньше или равна третьей - треугольник не сущ-ет"""
        self.assertEqual(check_triangle(10, 20, 30), "Треугольник не существует")
        self.assertEqual(check_triangle(1, 1, 3), "Треугольник не существует")
        self.assertEqual(check_triangle(5, 7, 13), "Треугольник не существует")

    def test_triangle_not_exists_with_zero_side(self):
        """Тест: одна из сторон равна нулю"""
        self.assertEqual(check_triangle(0, 10, 10), "Треугольник не существует")
        self.assertEqual(check_triangle(10, 0, 10), "Треугольник не существует")
        self.assertEqual(check_triangle(10, 10, 0), "Треугольник не существует")

    def test_triangle_not_exists_with_negative_side(self):
        """Тест: одна из сторон отрицательная"""
        self.assertEqual(check_triangle(-10, 10, 10), "Треугольник не существует")
        self.assertEqual(check_triangle(10, -5, 10), "Треугольник не существует")
        self.assertEqual(check_triangle(10, 10, -1), "Треугольник не существует")

    def test_all_sides_negative(self):
        """Тест: все стороны отрицательные"""
        self.assertEqual(check_triangle(-10, -10, -10), "Треугольник не существует")


if __name__ == "__main__":
    unittest.main()
