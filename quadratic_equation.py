def discriminant(a, b, c):
    """
    Вычисляет дискриминант квадратного уравнения.
    """
    return b**2 - 4 * a * c


def solution(a, b, c):
    """
    Решает квадратное уравнение ax² + bx + c = 0.
    """
    if a == 0:
        raise ValueError("Коэффициент 'a' не может быть нулём в квадратном уравнении.")

    d = discriminant(a, b, c)

    if d > 0:
        x1 = (-b + d**0.5) / (2 * a)
        x2 = (-b - d**0.5) / (2 * a)
        return sorted([x1, x2], reverse=True)
    elif d == 0:
        x = -b / (2 * a)
        return [x]
    else:
        return "корней нет"
