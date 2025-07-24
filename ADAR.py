import sympy as sp


def solve_ADAR():
    # Определяем символьные переменные
    P1, P2, Z, u, t = sp.symbols('P1 P2 Z u t')
    r1, r2, K1, K2, alpha1, alpha2, w1, w2, d1, d2, b1, gamma1, gamma2, m, m1 = sp.symbols(
        'r1 r2 K1 K2 alpha1 alpha2 w1 w2 d1 d2 b1 gamma1 gamma2 m m1'
    )
    P2_star, T1, T2 = sp.symbols('P2_star T1 T2', constant = True)

    # Собираем все шаги решения
    steps = []

    # 1. Исходная система
    dP1_dt = r1 * P1 * (1 - (P1 + alpha1 * P2) / K1) - (w1 * P1 * Z) / (d1 + P1) + u
    dP2_dt = r2 * P2 * (1 - (P2 + alpha2 * P1) / K2) - (w2 * P2 * Z) / (d2 + b1 * P2 ** 2)
    dZ_dt = (gamma1 * P1 * Z) / (d1 + P1) - (gamma2 * P2 * Z) / (d2 + b1 * P2 ** 2) - m * Z - m1 * Z ** 2

    steps.append(("Исходная система уравнений:", [
        r"\frac{dP_1}{dt} = " + sp.latex(dP1_dt),
        r"\frac{dP_2}{dt} = " + sp.latex(dP2_dt),
        r"\frac{dZ}{dt} = " + sp.latex(dZ_dt)
    ]))


    # 2. Определение макропеременных
    phi = sp.Function('phi')(P2, Z)
    psi = P1 - phi
    psi2 = P2 - P2_star

    steps.append(("Макропеременные:", [
        r"\psi_1 = " + sp.latex(psi),
        r"\psi_2 = " + sp.latex(psi2)
    ]))
    phi_dot = sp.Symbol(r'\dot{\phi}')
    dP2_dt_sym = sp.Symbol(r'\dot{P}_2')  # Символ для dP2/dt
    dZ_dt_sym = sp.Symbol(r'\dot{Z}')    # Символ для dZ/dt
    # 3. Производные макропеременных
    dphi_dt = sp.Derivative(phi, t , evaluate = False)#sp.diff(phi, P2) * dP2_dt + sp.diff(phi, Z) * dZ_dt
    dpsi_dt = dP1_dt - phi_dot
    dpsi2_dt = dP2_dt

    steps.append(("Производные макропеременных:", [
        r"\frac{d\psi_1}{dt} = " + sp.latex(dpsi_dt),
        r"\frac{d\psi_2}{dt} = " + sp.latex(dpsi2_dt)
    ]))

    # 4. Уравнения Эйлера-Лагранжа
    eq = T1 * dpsi_dt + psi
    eq2 = T2 * dpsi2_dt + psi2


    steps.append(("Уравнения Эйлера-Лагранжа:", [
        r"T_1 \frac{d\psi_1}{dt} + \psi_1 = " + sp.latex(eq),
        r"T_2 \frac{d\psi_2}{dt} + \psi_2 = " + sp.latex(eq2)
    ]))

    # 5. Решение для управления u
    u_solution = sp.solve(eq, u)[0]
    steps.append(("Решение для управления u:", [
        r"u = " + sp.latex(sp.apart(u_solution, P1))
    ]))



    # 6. Выражение P1 через phi
    P1_solution = sp.solve(psi, P1)[0]
    steps.append(("Выражение P₁ через φ:", [
        r"P_1 = " + sp.latex(P1_solution)
    ]))

    # 7. Решение для phi
    phi_substituted = eq2.subs(P1, P1_solution)
    phi_solved = sp.solve(phi_substituted, phi)[0]

    dphi_dP2 = sp.diff(phi_solved, P2) * dP2_dt_sym
    dphi_dZ = sp.diff(phi_solved, Z) * dZ_dt_sym
    steps.append(("Производные φ:", [
        r"\frac{\partial \phi}{\partial P_2} = " + sp.latex(sp.apart(sp.simplify(dphi_dP2), P2)),
        r"\frac{\partial \phi}{\partial Z} = " + sp.latex(dphi_dZ)
    ]))



    #phi_solution =  (K2 / alpha2) * (
    #1 - (1 / (r2 * P2)) * ((P2 - P2_star) / T2 + (w2 * P2 * Z) / (d2 + b1 * P2**2))) - (P2 / alpha2)
    steps.append(("Решение для φ:", [
        r"\phi = " + sp.latex( sp.apart(phi_solved, P2))
    ]))

    # 8. Итоговое управление

    u_substituted = u_solution.subs({P1: phi})

    # Вместо apart используем комбинацию методов:
    # 1. Сначала собираем по основным переменным
    #u_collected = sp.collect(u_substituted, [phi, phi_dot, r1, K1])

    # 2. Затем упрощаем (без разложения на дроби)
    u_simplified = sp.simplify(u_substituted)


    steps.append(("Итоговое управление u:", [
        r"u = " + sp.latex(sp.apart(u_simplified, phi))
    ]))
    return steps