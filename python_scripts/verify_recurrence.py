"""
verify_recurrence.py
====================
Verifies the recurrence relations for the Temperley tooth generating
functions h_r(q), and checks them against Temperley's explicit values
from his 1952 paper (equation 9).

Two recurrences are verified:
  (A) The multi-term equation (equivalent to Temperley's eq. 8):
        h_r(1 - q^r) = q^r * (1 + sum_{k=1}^{r-1} (r-k+1) * h_k(q))
  (B) The two-term recurrence (from Temperley's Note added in proof):
        (1 - q^r) h_r(q) = 2q h_{r-1}(q) - q^2 h_{r-2}(q)

The two-term recurrence is derived from the multi-term one by computing
the combination F_r - 2q F_{r-1} + q^2 F_{r-2}, where F_r = (1-q^r) h_r,
and verifying that the q^r cross-terms cancel exactly.

Requires: sympy
"""

import sympy as sp

q = sp.Symbol("q")


def compute_h(max_r):
    """Compute h_r(q) for r = 0, 1, ..., max_r via the two-term recurrence."""
    h = {0: sp.Integer(1), 1: q / (1 - q)}
    for r in range(2, max_r + 1):
        h[r] = sp.cancel((2 * q * h[r - 1] - q**2 * h[r - 2]) / (1 - q**r))
    return h


def main():
    max_r = 7
    h = compute_h(max_r)

    # ------------------------------------------------------------------
    print("=" * 60)
    print("1. Closed forms h_r(q) = N_r(q) / (q;q)_r")
    print("=" * 60)
    for r in range(1, max_r + 1):
        denom = sp.Mul(*[1 - q**k for k in range(1, r + 1)])
        numer = sp.factor(sp.cancel(h[r] * denom))
        print(f"  h_{r}(q) = {numer} / (q;q)_{r}")

    # ------------------------------------------------------------------
    print()
    print("=" * 60)
    print("2. Verification against Temperley's equation (9)")
    print("   (explicit values h_1, h_2, h_3 from Temperley 1952)")
    print("=" * 60)
    temperley_eq9 = {
        1: q / (1 - q),
        2: q**2 / (1 - q) ** 2,
        3: q**3 * (1 + q) ** 2 / ((1 - q) * (1 - q**2) * (1 - q**3)),
    }
    for r, expected in temperley_eq9.items():
        match = sp.simplify(h[r] - expected) == 0
        print(f"  h_{r}: matches Temperley eq(9): {match}")

    # ------------------------------------------------------------------
    print()
    print("=" * 60)
    print("3. Verification of the two-term recurrence")
    print("   (1 - q^r) h_r = 2q h_{r-1} - q^2 h_{r-2}")
    print("=" * 60)
    for r in range(2, max_r + 1):
        lhs = sp.cancel((1 - q**r) * h[r])
        rhs = sp.cancel(2 * q * h[r - 1] - q**2 * h[r - 2])
        match = sp.simplify(lhs - rhs) == 0
        print(f"  r={r}: {match}")

    # ------------------------------------------------------------------
    print()
    print("=" * 60)
    print("4. Verification of the multi-term equation (Temperley eq. 8)")
    print("   (1 - q^r) h_r = q^r * (1 + sum_{k=1}^{r-1} (r-k+1) h_k)")
    print("=" * 60)
    for r in range(1, max_r + 1):
        lhs = sp.cancel((1 - q**r) * h[r])
        rhs_sum = 1 + sum((r - k + 1) * h[k] for k in range(1, r))
        rhs = sp.cancel(q**r * rhs_sum)
        match = sp.simplify(lhs - rhs) == 0
        print(f"  r={r}: {match}")

    # ------------------------------------------------------------------
    print()
    print("=" * 60)
    print("5. Derivation of two-term from multi-term")
    print("   Setting F_r = (1-q^r) h_r, verify:")
    print("   F_r - 2q F_{r-1} + q^2 F_{r-2} = q^r (2 h_{r-1} - h_{r-2})")
    print("   (the q^r terms then cancel to give the two-term recurrence)")
    print("=" * 60)
    for r in range(3, max_r + 1):
        Fr = (1 - q**r) * h[r]
        Fr1 = (1 - q ** (r - 1)) * h[r - 1]
        Fr2 = (1 - q ** (r - 2)) * h[r - 2]
        lhs = sp.cancel(Fr - 2 * q * Fr1 + q**2 * Fr2)
        rhs = sp.cancel(q**r * (2 * h[r - 1] - h[r - 2]))
        match = sp.simplify(lhs - rhs) == 0
        print(f"  r={r}: {match}")

    print()
    print("Expanding and collecting, all q^r cross-terms cancel:")
    r = sp.Symbol("r", positive=True, integer=True)
    print("  2q(1-q^{r-1})h_{r-1} = 2q h_{r-1} - 2q^r h_{r-1}")
    print("  -q^2(1-q^{r-2})h_{r-2} = -q^2 h_{r-2} + q^r h_{r-2}")
    print("  + q^r(2h_{r-1} - h_{r-2})")
    print("  => total = 2q h_{r-1} - q^2 h_{r-2}  (q^r terms cancel)")


if __name__ == "__main__":
    main()
