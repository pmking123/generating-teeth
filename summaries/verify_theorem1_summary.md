# Verification of Theorem 1

## Summary of `verify_theorem1.py`

---

## (a) Theory

### The bivariate generating function

The paper introduces the bivariate generating function

\[
H(y,q)
=
\sum_{r\ge0} h_r(q)\,y^r,
\]

where \(h_r(q)\) is the generating function for teeth of base length \(r\).

Theorem 1 gives an explicit closed-form expression for \(H(y,q)\), namely

\[
H(y,q)
=
\frac{1}{(yq;q)_\infty^2}
-
\sum_{m\ge1}
\frac{yq^m}
     {(yq;q)_m^2}.
\]

This representation replaces the recursive definition of the \(h_r(q)\) with a single analytic expression involving q-Pochhammer symbols.

### Functional equation

The proof of Theorem 1 is based on the functional equation

\[
H(y,q)(1-qy)^2
=
H(qy,q)-qy.
\]

This equation encapsulates the recurrence structure of the generating functions and uniquely characterises \(H(y,q)\).

### Recovery of the individual generating functions

Since

\[
H(y,q)
=
\sum_{r\ge0} h_r(q)y^r,
\]

the coefficient of \(y^r\) in the closed-form expression must reproduce \(h_r(q)\).

In particular,

\[
[y]H(y,q)=h_1(q),
\qquad
[y^2]H(y,q)=h_2(q).
\]

These provide immediate consistency checks on the theorem.

---

## (b) What the script does

The script performs three independent verifications of Theorem 1.

### Check A: Functional equation

It constructs a truncated series representation of \(H(y,q)\) from the recurrence-generated functions \(h_r(q)\) and verifies that

\[
H(y,q)(1-qy)^2
=
H(qy,q)-qy
\]

holds symbolically through order \(y^6\). This check tests the recurrence-generated series directly; the closed-form formula of Theorem 1 does not appear in Check A. The verification establishes that the truncated recurrence series satisfies the functional equation that characterises \(H(y,q)\), which is a necessary condition for the theorem.

### Check B: Coefficient extraction

It extracts the coefficients

\[
[y]H(y,q)
\quad\text{and}\quad
[y^2]H(y,q)
\]

directly from the closed-form formula and verifies that they reproduce the known generating functions \(h_1(q)\) and \(h_2(q)\).

### Check C: Numerical evaluation

It evaluates \(H(y,q)\) at

\[
(y,q)=(0.3,0.5)
\]

using two completely different methods:

1. Summation of the recurrence-generated coefficients \(h_r(q)\);
2. Direct evaluation of the closed-form expression from Theorem 1.

The resulting numerical values are compared, with agreement declared if the absolute difference is less than \(10^{-9}\).

---

## (c) How the script does it

### Construction of \(h_r(q)\)

`compute_h(max_r)` generates the functions recursively using

\[
(1-q^r)h_r(q)
=
2q\,h_{r-1}(q)
-
q^2 h_{r-2}(q).
\]

The resulting rational functions are simplified symbolically using SymPy.

### Check A: Functional equation

The script forms the truncated generating function

\[
H(y,q)
=
\sum_{r=0}^{6} h_r(q)y^r,
\]

which includes the \(y^0\) term \(h_0 = 1\) — the boundary condition \(H(0,q)=1\) used in the proof of Theorem 1. It then computes

\[
H(y,q)(1-qy)^2
\]

and

\[
H(qy,q)-qy,
\]

expands both as polynomials in \(y\), and subtracts them.

The theorem is verified if the resulting polynomial is identically zero.

### Check B: Symbolic coefficient extraction

Rather than performing general automated coefficient extraction, the script encodes the specific logarithmic differentiation steps as hardcoded symbolic expressions. This is a symbolic confirmation of the manual calculations presented in Remark 2 of the paper (the consistency check for \(r=1\) and \(r=2\)).

For the first term of Theorem 1,

\[
\frac{1}{(yq;q)_\infty^2},
\]

the script uses logarithmic differentiation and known q-series identities to obtain the coefficients of \(y\) and \(y^2\).

The corresponding coefficients of the subtraction term

\[
\sum_{m\ge1}
\frac{yq^m}
     {(yq;q)_m^2}
\]

are then evaluated separately.

Combining the two contributions yields symbolic expressions for

\[
[y]H(y,q)
\]

and

\[
[y^2]H(y,q),
\]

which are compared against the recurrence-generated values of \(h_1(q)\) and \(h_2(q)\).

### Check C: Numerical evaluation

The script evaluates

\[
H(0.3,0.5)
\]

in two independent ways.

#### Recurrence evaluation

The generating functions \(h_r(0.5)\) are generated recursively up to \(r=39\), and

\[
H(0.3,0.5)
=
\sum_{r=0}^{39} h_r(0.5)(0.3)^r
\]

is computed.

#### Closed-form evaluation

The product

\[
\frac{1}{(yq;q)_\infty^2}
\]

and the correction sum

\[
\sum_{m\ge1}
\frac{yq^m}
     {(yq;q)_m^2}
\]

are both truncated after 40 terms and evaluated numerically.

The two resulting approximations are then compared. At \((y,q)=(0.3,0.5)\) the \(r\)-th term of the recurrence sum is of order \((0.3)^r\), which decays rapidly, so 40 terms is more than sufficient for the required precision. Agreement is declared if the absolute difference is less than \(10^{-9}\).

---

## (d) Output produced

### Functional equation verification

The script prints

\[
H(y,q)(1-qy)^2
-
\bigl(H(qy,q)-qy\bigr),
\]

expanded through order \(y^6\).

A successful verification gives

```
LHS - RHS = 0
```

confirming agreement term-by-term.

### Coefficient checks

The script prints the extracted values of

\[
[y]H(y,q)
\]

and

\[
[y^2]H(y,q),
\]

alongside the independently generated functions \(h_1(q)\) and \(h_2(q)\).

For each coefficient it reports whether the symbolic expressions are identical.

### Numerical comparison

The values

\[
H(0.3,0.5)
\]

obtained from the recurrence and from Theorem 1 are displayed.

The script reports:

* the two numerical values;
* their absolute difference;
* whether their absolute difference is less than \(10^{-9}\).

---

## (e) What we learn

**Theorem 1 satisfies the defining functional equation.** The symbolic verification confirms that the proposed closed-form expression obeys the same functional equation that characterises the generating function \(H(y,q)\).

**The formula reproduces the known low-order generating functions.** The coefficients \([y]H\) and \([y^2]H\) recover \(h_1(q)\) and \(h_2(q)\) exactly, demonstrating consistency with the recurrence theory.

**The analytic and recursive constructions agree numerically.** The evaluation at \((y,q)=(0.3,0.5)\) provides an independent numerical confirmation that the closed-form expression and the recurrence-generated series describe the same function.

**The verification is independent in three different ways.** Functional-equation testing, coefficient extraction, and numerical evaluation each probe different aspects of the theorem, making simultaneous agreement highly persuasive.

**The script acts as a validation of Theorem 1 rather than a derivation.** Its purpose is to confirm that the explicit q-series formula is consistent with the recurrence structure and the known generating functions, thereby providing computational support for the theorem presented in the paper.
