

import argparse
import math
import sys

EPS = 1e-12

def is_finite_number(s: str) -> bool:
    try:
        x = float(s)
        return math.isfinite(x)
    except Exception:
        return False

def prompt_float(name: str) -> float:
    """Цикл ввода до корректного значения."""
    while True:
        raw = input(f"Введите коэффициент {name}: ").strip()
        if is_finite_number(raw):
            return float(raw)
        print(f"Некорректный ввод для {name}. Повторите.")

def get_coeffs_from_args_or_prompt() -> tuple[float, float, float]:
    """Парсим -a/-b/-c или позиционные; если что-то некорректно — спрашиваем у пользователя."""
    p = argparse.ArgumentParser(
        description="Решение биквадратного уравнения a*x^4 + b*x^2 + c = 0."
    )
    p.add_argument("-a", type=str, help="коэффициент a")
    p.add_argument("-b", type=str, help="коэффициент b")
    p.add_argument("-c", type=str, help="коэффициент c")
    p.add_argument("pos", nargs="*", help="позиционно: a b c")
    args = p.parse_args()


    raws = {"A": None, "B": None, "C": None}

    if len(args.pos) >= 1:
        raws["A"] = args.pos[0]
    if len(args.pos) >= 2:
        raws["B"] = args.pos[1]
    if len(args.pos) >= 3:
        raws["C"] = args.pos[2]

    if raws["A"] is None and args.a is not None:
        raws["A"] = args.a
    if raws["B"] is None and args.b is not None:
        raws["B"] = args.b
    if raws["C"] is None and args.c is not None:
        raws["C"] = args.c

    coeffs = {}
    for name in ("A", "B", "C"):
        if raws[name] is not None and is_finite_number(raws[name]):
            coeffs[name] = float(raws[name])
        else:
            
            coeffs[name] = prompt_float(name)

    return coeffs["A"], coeffs["B"], coeffs["C"]

def solve_biquadratic(a: float, b: float, c: float):
    """
    Возвращает (discriminant, roots, note).
    discriminant: None, если уравнение не квадратно по y=x^2 (т.е. a≈0)
    roots: отсортированный список действительных корней x
    note: текстовое пояснение для вырожденных случаев
    """
    roots: list[float] = []

    # Случай a ≈ 0: сводится к b*x^2 + c = 0
    if abs(a) < EPS:
        if abs(b) < EPS:
            if abs(c) < EPS:
                return None, [], "Бесконечно много решений: любое x удовлетворяет 0 = 0."
            else:
                return None, [], "Решений нет: получаем противоречие c = 0 при c ≠ 0."
        # b*x^2 + c = 0 → x^2 = -c/b
        y = -c / b
        if y < -EPS:
            return None, [], "Действительных корней нет: x^2 = отрицательное число."
        if abs(y) < EPS:
            roots = [0.0]
        else:
            s = math.sqrt(y)
            roots = sorted([-s, s])
        return None, roots, None

    # Обычный случай: a*y^2 + b*y + c = 0, где y = x^2
    D = b * b - 4 * a * c

    if D < -EPS:
        return D, [], "Действительных корней нет: дискриминант < 0."
    if abs(D) < EPS:
        y = -b / (2 * a)
        if y > EPS:
            s = math.sqrt(y)
            roots = sorted([-s, s])
        elif abs(y) <= EPS:
            roots = [0.0]
        else:
            roots = []
        return D, roots, None

    # D > 0
    sqrtD = math.sqrt(D)
    y1 = (-b + sqrtD) / (2 * a)
    y2 = (-b - sqrtD) / (2 * a)
    for y in (y1, y2):
        if y > EPS:
            s = math.sqrt(y)
            roots.extend([-s, s])
        elif abs(y) <= EPS:
            roots.append(0.0)
    roots = sorted(set([+0.0 if abs(x) < EPS else x for x in roots]))
    return D, roots, None

def main():
    a, b, c = get_coeffs_from_args_or_prompt()
    print(f"\nРешаем: {a} * x^4 + {b} * x^2 + {c} = 0")

    D, roots, note = solve_biquadratic(a, b, c)

    if D is not None:
        print(f"Дискриминант квадр. по y=x^2: D = {D}")
    if note:
        print(note)

    if roots:
        print("Действительные корни:")
        for i, r in enumerate(roots, 1):
            print(f"  x{i} = {r}")
    else:
        print("Действительных корней нет.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nПрервано пользователем.")
        sys.exit(130)
