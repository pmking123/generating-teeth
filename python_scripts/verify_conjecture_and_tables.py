"""
verify_conjecture_and_tables.py
================================
Two independent computations:

PART 1 — Conjecture (Durfee-type formula for U(t)):
  Verifies Conjecture 1 of the paper:
      U(t) = sum_{m >= 0} q^{m^2} t^{2m} / ((t;q)_m * (t;q)_{m+1})
  where U(t) = sum_{r >= 0} u_r(q) t^r and u_r is the normalized
  generating function defined by h_r(q) = (q^r / (q;q)_r) * u_r(q).

  The conjecture is verified symbolically by checking that the
  coefficients of t^0 through t^{N_max} agree on both sides.

PART 2 — Coefficient table:
  Computes the triangle T(r, N) = [q^N] h_r(q) for r = 1, ..., 7
  and N = 1, ..., 15, matching Table 2 in the paper.
  Also computes the column sums sum_{r=1}^N T(r, N) for N = 1, ..., 9
  and verifies the row r=2 formula T(2,N) = N-1.

Requires: sympy
"""

import sympy as sp

q = sp.Symbol('q')
t = sp.Symbol('t')


def compute_h(max_r):
    """Compute h_r(q) for r = 0, ..., max_r via the two-term recurrence."""
    h = {0: sp.Integer(1), 1: q / (1 - q)}
    for r in range(2, max_r + 1):
        h[r] = sp.cancel((2 * q * h[r-1] - q**2 * h[r-2]) / (1 - q**r))
    return h


def compute_u(max_r):
    """
    Compute u_r(q) for r = 0, ..., max_r via the recurrence
        u_r = 2 u_{r-1} - (1 - q^{r-1}) u_{r-2},  r >= 2,
    with u_0 = u_1 = 1.
    """
    u = {0: sp.Integer(1), 1: sp.Integer(1)}
    for r in range(2, max_r + 1):
        u[r] = sp.expand(2 * u[r-1] - (1 - q**(r-1)) * u[r-2])
    return u


def poch(a, n):
    """Compute (a; q)_n = prod_{k=0}^{n-1} (1 - a q^k)."""
    if n == 0:
        return sp.Integer(1)
    return sp.Mul(*[1 - a * q**k for k in range(n)])


def main():

    # ==================================================================
    print("=" * 60)
    print("PART 1: Verification of the Durfee-type conjecture")
    print("  U(t) = sum_{m>=0} q^{m^2} t^{2m} / ((t;q)_m (t;q)_{m+1})")
    print("=" * 60)

    N_max = 15
    u = compute_u(N_max + 2)

    # U(t) from recurrence
    U_recurrence = sum(u[r] * t**r for r in range(N_max + 1))

    # U(t) from conjecture (sum over m up to N_max//2 + 2)
    U_conjecture = sp.Integer(0)
    for m in range(N_max // 2 + 3):
        numer  = q**(m * m) * t**(2 * m)
        denom  = poch(t, m) * poch(t, m + 1)
        term   = sp.cancel(numer / denom)
        term_s = sp.series(term, t, 0, N_max + 1).removeO()
        U_conjecture = sp.expand(U_conjecture + term_s)

    U_conj_s = sp.series(U_conjecture, t, 0, N_max + 1).removeO()
    U_rec_s  = sp.series(U_recurrence, t, 0, N_max + 1).removeO()

    print(f"\n  Checking coefficients of t^0 through t^{N_max}:")
    all_match = True
    for r in range(N_max + 1):
        c_rec  = sp.Poly(U_rec_s,  t).nth(r)
        c_conj = sp.Poly(U_conj_s, t).nth(r)
        match  = sp.expand(c_rec - c_conj) == 0
        if not match:
            all_match = False
            print(f"    MISMATCH at r={r}:")
            print(f"      recurrence: {sp.expand(c_rec)}")
            print(f"      conjecture: {sp.expand(c_conj)}")
    print(f"  All coefficients match (r = 0 to {N_max}): {all_match}")

    print(f"\n  First several u_r(q):")
    for r in range(8):
        print(f"    u_{r}(q) = {sp.expand(u[r])}")

    # ==================================================================
    print()
    print("=" * 60)
    print("PART 2: Coefficient triangle T(r, N) = [q^N] h_r(q)")
    print("=" * 60)
    h = compute_h(8)

    max_r = 7
    max_N = 15
    table = {}
    for r in range(1, max_r + 1):
        series = sp.series(h[r], q, 0, max_N + 1)
        for N in range(1, max_N + 1):
            table[(r, N)] = int(series.coeff(q, N))

    print(f"\n  {'r\\N':<5}", end="")
    for N in range(1, max_N + 1):
        print(f"{N:4d}", end="")
    print()
    print("  " + "-" * (5 + 4 * max_N))
    for r in range(1, max_r + 1):
        print(f"  {r:<5}", end="")
        for N in range(1, max_N + 1):
            print(f"{table[(r, N)]:4d}", end="")
        print()

    print(f"\n  Column sums sum_{{r=1}}^N T(r, N) (teeth with exactly N cubes):")
    for N in range(1, 10):
        col_sum = sum(table.get((r, N), 0) for r in range(1, N + 1))
        print(f"    N={N}: {col_sum}")

    print(f"\n  Spot check: row r=2 satisfies T(2,N) = N-1 for N=2,...,{max_N}:")
    ok = all(table[(2, N)] == N - 1 for N in range(2, max_N + 1))
    print(f"  {ok}")


if __name__ == "__main__":
    main()
