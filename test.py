import sympy as sp

# Переменные
P1, P2, Z, u = sp.symbols('P1 P2 Z u')
phi = sp.Symbol('phi')
T1 = sp.Symbol('T1')
r1, K1, alpha1, w1, d1 = sp.symbols('r1 K1 alpha1 w1 d1')
r2, K2, alpha2, w2, d2, b1, T2, P2_star = sp.symbols('r2 K2 alpha2 w2 d2 b1 T2 P2_star')
# dP1/dt
dP1_dt = r1 * P1 * (1 - (P1 + alpha1 * P2) / K1) - (w1 * P1 * Z) / (d1 + P1) + u
dP2_dt = r2 * P2 * (1 - (P2 + alpha2 * P1) / K2) - (w2 * P2 * Z) / (d2 + b1 * P2 ** 2)

# Уравнение Эйлера-Лагранжа по psi1
eq_u = T1 * dP1_dt + (P1 - phi)
eq_phi = T2 * dP2_dt + (P2 - P2_star)
# Решаем относительно u
u_expr = sp.solve(eq_u, u)[0]

# Выражение для phi из предыдущего шага


phi_expr = sp.solve(eq_phi.subs(P1, phi) , phi)[0]

# Подставляем φ в u
u_final = u_expr.subs(phi, phi_expr)
u_simplified = sp.simplify(u_final)
eq_check = eq_u.subs(u,u_final).subs(phi, phi_expr)
eq_check_simp = sp.sympify(eq_check)

print(eq_check_simp)
print(u_simplified)