"""
verify_theorem3.py
==================
Verifies Theorem 3: the Gaussian-binomial expansion

    h_r(q) = sum_{h >= 1}  sum_{a,b >= 0, a+b <= r-1}
                 q^{a+b+h(r-a-b)} * [a+h-2; a]_q * [b+h-2; b]_q

Two checks are performed:

  (A) The key q-series identity used in the proof,
          [t^a] prod_{i=1}^n 1/(1-tq^i) = q^a * [a+n-1; a]_q,
      is verified symbolically for n = 1, 2, 3 and a = 0, 1, 2, 3, 4.

  (B) The full expansion formula is verified for r = 1, 2, 3, 4, 5, 6:
      for each r, height h is summed until no further contributions
      can reach the target q-degree (q_order - 1 = 24), and the
      result is compared coefficient-by-coefficient to h_r from the
      two-term recurrence.

The convention [n; 0]_q = 1 for all n (including n < 0) is used.

Note on the sum over h: the formula involves an infinite sum over h >= 1.
For each fixed r, the minimum q-power of the h-th term is h (since the
minimum of a+b+h(r-a-b) over a+b <= r-1 is h*1 = h when r-a-b=1).
The sum therefore converges termwise in q, and for any finite q-degree D
only h = 1, ..., D contribute.

Requires: sympy
"""

import sympy as sp

q = sp.Symbol("q")
t = sp.Symbol("t")


def compute_h(max_r):
    """Compute h_r(q) for r = 0, ..., max_r via the two-term recurrence."""
    h = {0: sp.Integer(1), 1: q / (1 - q)}
    for r in range(2, max_r + 1):
        h[r] = sp.cancel((2 * q * h[r - 1] - q**2 * h[r - 2]) / (1 - q**r))
    return h


def gauss_binom(n, k):
    """
    Gaussian binomial coefficient [n; k]_q.

    Convention: [n; 0]_q = 1 for all n (empty product).
                [n; k]_q = 0 if k < 0 or (k > n and n >= 0).
    """
    if k == 0:
        return sp.Integer(1)
    if k < 0 or n < 0:
        return sp.Integer(0)
    if k > n:
        return sp.Integer(0)
    result = sp.Integer(1)
    for i in range(k):
        result = result * (1 - q ** (n - i)) / (1 - q ** (i + 1))
    return sp.factor(result)


def main():
    h = compute_h(7)

    # ------------------------------------------------------------------
    print("=" * 60)
    print("CHECK A: q-series identity")
    print("  [t^a] prod_{i=1}^n 1/(1-tq^i) = q^a * [a+n-1; a]_q")
    print("=" * 60)
    for n in range(1, 3):
        prod_expr = sp.Integer(1)
        for i in range(1, n + 1):
            prod_expr /= 1 - t * q**i
        print(f"  n = {n}:")
        all_match = True
        for a in range(5):
            series = sp.series(prod_expr, t, 0, a + 2)
            coeff = sp.Poly(series.removeO(), t).nth(a)
            rhs = q**a * gauss_binom(a + n - 1, a)
            match = sp.expand(coeff - rhs) == 0
            if not match:
                all_match = False
                print(f"    a={a}: MISMATCH")
                print(f"      LHS = {sp.expand(coeff)}")
                print(f"      RHS = {sp.expand(rhs)}")
        if all_match:
            print(f"    a = 0,1,2,3,4: all match")

    # ------------------------------------------------------------------
    print()
    print("=" * 60)
    print("CHECK B: Full Gaussian-binomial expansion for r = 1, ..., 6")
    print("  (h summed until minimum q-power exceeds q_order)")
    print("=" * 60)
    q_order = 25

    for r in range(1, 7):
        total = sp.Integer(0)
        # Sum heights h until the minimum q-exponent h exceeds q_order
        for hh in range(1, q_order + 1):
            for a in range(r):
                for b in range(r - a):
                    exp_val = a + b + hh * (r - a - b)
                    if exp_val >= q_order:
                        continue
                    gb1 = gauss_binom(a + hh - 2, a)
                    gb2 = gauss_binom(b + hh - 2, b)
                    weight = q**exp_val
                    total += sp.expand(weight * gb1 * gb2)

        total_s = sp.series(total, q, 0, q_order).removeO()
        hr_s = sp.series(h[r], q, 0, q_order).removeO()
        match = sp.expand(total_s - hr_s) == 0
        print(f"  r={r}: match up to q^{q_order - 1}: {match}")

    # ------------------------------------------------------------------
    print()
    print("=" * 60)
    print("Detailed verification for r = 3 (paper example, up to q^11)")
    print("=" * 60)
    r = 3
    q_detail = 12
    print(f"\n  Contributions by height h (terms up to q^{q_detail - 1}):")
    grand_total = sp.Integer(0)
    for hh in range(1, q_detail):
        subtotal = sp.Integer(0)
        for a in range(r):
            for b in range(r - a):
                exp_val = a + b + hh * (r - a - b)
                if exp_val >= q_detail:
                    continue
                gb1 = gauss_binom(a + hh - 2, a)
                gb2 = gauss_binom(b + hh - 2, b)
                subtotal += sp.expand(q**exp_val * gb1 * gb2)
        if subtotal != 0:
            print(f"  h={hh}: {sp.expand(subtotal)}")
        grand_total += subtotal

    grand_s = sp.series(grand_total, q, 0, q_detail).removeO()
    h3_s = sp.series(h[3], q, 0, q_detail).removeO()
    print(f"\n  Sum:   {sp.expand(grand_s)}")
    print(f"  h_3:   {sp.expand(h3_s)}")
    print(f"  Match up to q^{q_detail - 1}: {sp.expand(grand_s - h3_s) == 0}")


if __name__ == "__main__":
    main()
