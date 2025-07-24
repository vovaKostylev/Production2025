import sympy as sp
from functools import lru_cache
import time

# Вспомогательная функция для решения уравнений с кэшированием
@lru_cache(maxsize=128)
def cached_solve(eq, var):
    solutions = sp.solve(eq, var, simplify=False)
    return solutions[0] if solutions else None

# Вспомогательная функция для упрощения выражений с кэшированием
@lru_cache(maxsize=128)
def cached_simplify(expr_str):
    expr = sp.sympify(expr_str)
    return str(expr.expand())  # Используем expand вместо simplify для скорости

def solve_ADAR():
    start_total = time.time()
    # Определяем символьные переменные
    P1, P2, Z, u = sp.symbols('P1 P2 Z u')
    r1, r2, K1, K2, alpha1, alpha2, w1, w2, d1, d2, b1, gamma1, gamma2, m, m1 = sp.symbols(
        'r1 r2 K1 K2 alpha1 alpha2 w1 w2 d1 d2 b1 gamma1 gamma2 m m1'
    )
    P2_star, T1, T2 = sp.symbols('P2_star T1 T2')

    steps = []

    # 1. Исходная система
    dP1_dt = r1 * P1 * (1 - (P1 + alpha1 * P2) / K1) - (w1 * P1 * Z) / (d1 + P1) + u
    dP2_dt = r2 * P2 * (1 - (P2 + alpha2 * P1) / K2) - (w2 * P2 * Z) / (d2 + b1 * P2 ** 2)
    dZ_dt = (gamma1 * P1 * Z) / (d1 + P1) - (gamma2 * P2 * Z) / (d2 + b1 * P2  ** 2) - m * Z - m1 * Z ** 2

    steps.append(("Исходная система уравнений:", [
        r"\frac{dP_1}{dt} = " + sp.latex(dP1_dt),
        r"\frac{dP_2}{dt} = " + sp.latex(dP2_dt),
        r"\frac{dZ}{dt} = " + sp.latex(dZ_dt)
    ]))

    # 2. Макропеременные
    phi = sp.Symbol('phi')
    psi = P1 - phi
    psi2 = P2 - P2_star

    steps.append(("Макропеременные:", [
        r"\psi_1 = " + sp.latex(psi),
        r"\psi_2 = " + sp.latex(psi2)
    ]))

    # 3. Производные макропеременных
    start = time.time()
    dphi_dP2 = sp.diff(phi, P2)
    dphi_dZ = sp.diff(phi, Z)
    dphi_dt = dphi_dP2 * dP2_dt + dphi_dZ * dZ_dt
    dpsi_dt = dP1_dt - dphi_dt
    dpsi2_dt = dP2_dt
    print(f"Время вычисления производных: {time.time() - start} сек")

    steps.append(("Производные макропеременных:", [
        r"\frac{d\psi_1}{dt} = " + sp.latex(dpsi_dt),
        r"\frac{d\psi_2}{dt} = " + sp.latex(dpsi2_dt)
    ]))

    # 4. Уравнения Эйлера-Лагранжа
    eq = T1 * dpsi_dt + psi
    eq2 = T2 * dpsi2_dt + psi2

    steps.append(("Уравнения Эйлера-Лагранжа:", [
        r"T_1 \frac{d\psi_1}{dt} + \psi_1 = 0 : " + sp.latex(eq),
        r"T_2 \frac{d\psi_2}{dt} + \psi_2 = 0 : " + sp.latex(eq2)
    ]))

    # 5. Решение для u с кэшированием
    start = time.time()
    u_solution = cached_solve(str(eq), 'u')
    if u_solution:
        u_solution = sp.sympify(u_solution)
    else:
        u_solution = None
    print(f"Время решения для u: {time.time() - start} сек")

    steps.append(("Решение для управления u:", [
        r"u = " + sp.latex(u_solution) if u_solution else "Не удалось решить для u"
    ]))

    # 6. Выражение P1 через phi с кэшированием
    start = time.time()
    P1_solution = cached_solve(str(psi), 'P1')
    if P1_solution:
        P1_solution = sp.sympify(P1_solution)
    else:
        P1_solution = None
    print(f"Время выражения P1: {time.time() - start} сек")

    steps.append(("Выражение P₁ через φ:", [
        r"P_1 = " + sp.latex(P1_solution) if P1_solution else "Не удалось выразить P1"
    ]))

    # 7. Решение для phi с кэшированием
    start = time.time()
    if P1_solution:
        eq2_subst = eq2.subs(P1, P1_solution)
        eq2_subs = sp.cancel(eq2_subst)
        phi_solution = cached_solve(str(eq2_subs), str(phi))
        if phi_solution:
            phi_solution = sp.sympify(phi_solution)
        else:
            phi_solution = None
    else:
        phi_solution = None
    print(f"Время решения для phi: {time.time() - start} сек")

    steps.append(("Решение для φ:", [
        r"\phi = " + sp.latex(phi_solution) if phi_solution else "Не удалось решить для φ"
    ]))