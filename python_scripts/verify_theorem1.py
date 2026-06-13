"""
verify_theorem1.py
==================
Verifies Theorem 1: the explicit formula for the bivariate generating
function H(y, q) = sum_{r >= 0} h_r(q) y^r, namely

    H(y, q) = 1 / (yq; q)_inf^2  -  sum_{m >= 1} y q^m / (yq; q)_m^2

Three independent checks are performed:

  (A) The functional equation H(y,q)(1-qy)^2 = H(qy,q) - qy is verified
      symbolically up to y^6.

  (B) The coefficients [y^1] and [y^2] are extracted from the formula
      symbolically and verified to equal h_1(q) and h_2(q).

  (C) A numerical check at (y, q) = (0.3, 0.5): H is evaluated both
      from the recurrence sum (40 terms) and from the formula (40-term
      truncation of both the infinite product and the sum), and the
      results are compared to 10 decimal places.

Requires: sympy
"""

import sympy as sp

q = sp.Symbol('q')
y = sp.Symbol('y')


def compute_h(max_r):
    """Compute h_r(q) for r = 0, ..., max_r via the two-term recurrence."""
    h = {0: sp.Integer(1), 1: q / (1 - q)}
    for r in range(2, max_r + 1):
        h[r] = sp.cancel((2 * q * h[r-1] - q**2 * h[r-2]) / (1 - q**r))
    return h


def main():
    h = compute_h(7)

    # ------------------------------------------------------------------
    print("=" * 60)
    print("CHECK A: Functional equation H(y,q)(1-qy)^2 = H(qy,q) - qy")
    print("         verified symbolically up to y^6")
    print("=" * 60)
    order = 6
    H_series = sum(h[r] * y**r for r in range(order + 1))
    H_s   = sp.series(H_series, y, 0, order + 1).removeO()
    Hqy_s = sp.series(H_series.subs(y, q * y), y, 0, order + 1).removeO()
    lhs = sp.Poly(sp.series(sp.expand(H_s * (1 - q*y)**2), y, 0, order + 1).removeO(), y)
    rhs = sp.Poly(sp.expand(Hqy_s - q*y), y)
    diff = sp.expand(lhs.as_expr() - rhs.as_expr())
    print(f"  LHS - RHS = {diff}  (should be 0)")

    # ------------------------------------------------------------------
    print()
    print("=" * 60)
    print("CHECK B: Extract [y^1] and [y^2] from formula (*) symbolically")
    print("=" * 60)

    # [y^1] of 1/(yq;q)_inf^2:
    # d/dy|_{y=0} prod_{k>=1} 1/(1-yq^k)^2 = 2 sum_{k>=1} q^k = 2q/(1-q)
    coeff_y1_term1 = 2 * q / (1 - q)
    # [y^1] of sum_{m>=1} y q^m / (yq;q)_m^2:
    # at y=0, (yq;q)_m = 1, so contribution = sum_{m>=1} q^m = q/(1-q)
    coeff_y1_term2 = q / (1 - q)
    coeff_y1_H = sp.cancel(coeff_y1_term1 - coeff_y1_term2)
    print(f"  [y^1] H = {sp.factor(coeff_y1_H)},  "
          f"h_1(q) = {sp.factor(h[1])}")
    print(f"  Match: {sp.simplify(coeff_y1_H - h[1]) == 0}")

    # [y^2] via log-derivative of f(y) = 1/(yq;q)_inf^2:
    # [y^1](log f) = 2q/(1-q),  [y^2](log f) = q^2/(1-q^2)
    logf_y2 = q**2 / (1 - q**2)
    logf_y1 = 2 * q / (1 - q)
    coeff_y2_term1 = sp.factor(logf_y2 + sp.Rational(1, 2) * logf_y1**2)
    # [y^2] of subtracted sum:
    # [y^1](1/(yq;q)_m^2) = 2 sum_{k=1}^m q^k = 2q(1-q^m)/(1-q)
    # [y^2] sum = sum_{m>=1} q^m * 2q(1-q^m)/(1-q)
    coeff_y2_term2 = sp.cancel(
        2*q/(1-q) * q/(1-q) - 2*q/(1-q) * q**2/(1-q**2)
    )
    coeff_y2_H = sp.factor(coeff_y2_term1 - coeff_y2_term2)
    print(f"  [y^2] H = {coeff_y2_H},  "
          f"h_2(q) = {sp.factor(h[2])}")
    print(f"  Match: {sp.simplify(coeff_y2_H - h[2]) == 0}")

    # ------------------------------------------------------------------
    print()
    print("=" * 60)
    print("CHECK C: Numerical evaluation at (y, q) = (0.3, 0.5)")
    print("         Both series truncated at 40 terms")
    print("=" * 60)
    q_num, y_num = 0.5, 0.3
    trunc = 40

    # From recurrence sum (40 terms)
    h_vals = [1.0, q_num / (1 - q_num)]
    for r in range(2, trunc):
        h_new = (2*q_num*h_vals[-1] - q_num**2*h_vals[-2]) / (1 - q_num**r)
        h_vals.append(h_new)
    H_recurrence = sum(h_vals[r] * y_num**r for r in range(trunc))

    # From formula (40-term truncation of product and sum)
    term1 = 1.0
    for k in range(1, trunc):
        term1 /= (1 - y_num * q_num**k)**2
    term2 = 0.0
    for m in range(1, trunc):
        denom = 1.0
        for k in range(1, m + 1):
            denom *= (1 - y_num * q_num**k)**2
        term2 += y_num * q_num**m / denom
    H_formula = term1 - term2

    print(f"  H(0.3, 0.5) from recurrence sum : {H_recurrence:.12f}")
    print(f"  H(0.3, 0.5) from formula (*)    : {H_formula:.12f}")
    print(f"  Absolute difference             : {abs(H_recurrence - H_formula):.2e}")
    print(f"  Agreement to 10 d.p.            : "
          f"{abs(H_recurrence - H_formula) < 1e-9}")


if __name__ == "__main__":
    main()
