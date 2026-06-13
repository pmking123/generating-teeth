# Verification of Theorem 3

## Summary of `verify_theorem3.py`

---

## (a) Theory

### Theorem 3: Gaussian-binomial expansion

Theorem 3 provides an explicit expansion for the tooth generating functions

\[
h_r(q),
\]

expressing them as a weighted sum over tooth height and two auxiliary combinatorial parameters. The theorem states that

\[
h_r(q)
=
\sum_{h\ge1}
\sum_{\substack{a,b\ge0\\a+b\le r-1}}
q^{a+b+h(r-a-b)}
\begin{bmatrix}
a+h-2\\
a
\end{bmatrix}_q
\begin{bmatrix}
b+h-2\\
b
\end{bmatrix}_q .
\]

The coefficients are Gaussian (or q-binomial) coefficients, providing a direct combinatorial interpretation of the generating functions.

### Gaussian binomial coefficients

The q-binomial coefficient

\[
\begin{bmatrix}
n\\k
\end{bmatrix}_q
\]

is the q-analogue of the ordinary binomial coefficient and plays a central role in partition theory and q-series.

A key identity used in the proof of Theorem 3 is

\[
[t^a]
\prod_{i=1}^{n}
\frac{1}{1-tq^i}
=
q^a
\begin{bmatrix}
a+n-1\\a
\end{bmatrix}_q.
\]

This identity converts generating-function coefficients into Gaussian binomial coefficients and is the bridge between the recurrence formulation and the explicit expansion.

### Convergence of the height sum

Although the theorem involves an infinite sum over heights \(h\), each term contributes only powers of \(q\) greater than or equal to \(h\). Consequently, for any finite truncation in \(q\), only finitely many values of \(h\) contribute.

This makes coefficient-by-coefficient verification computationally feasible.

---

## (b) What the script does

The script performs two principal verification tasks.

### Check A: Verification of the q-series identity

It verifies

\[
[t^a]
\prod_{i=1}^{n}
\frac{1}{1-tq^i}
=
q^a
\begin{bmatrix}
a+n-1\\a
\end{bmatrix}_q
\]

symbolically for

* \(n=1,2,3\);
* \(a=0,1,2,3,4\).

### Check B: Verification of Theorem 3

It evaluates the full Gaussian-binomial expansion for base lengths

\[
r=1,2,3,4,5,6
\]

and compares the result against the independently generated functions \(h_r(q)\) obtained from the two-term recurrence.

The comparison is carried out coefficient-by-coefficient through

\[
q^{24}.
\]

### Detailed worked example

For the illustrative case

\[
r=3,
\]

the script prints the contribution from each height \(h\) separately and demonstrates explicitly how the individual contributions sum to the generating function \(h_3(q)\).

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

These recurrence-generated functions serve as the reference values for the verification.

### Gaussian binomial coefficients

`gauss_binom(n,k)` evaluates

\[
\begin{bmatrix}
n\\k
\end{bmatrix}_q
\]

symbolically.

The implementation adopts the following conventions:

\[
\begin{bmatrix}n\\0\end{bmatrix}_q = 1 \quad \text{for all } n,
\qquad
\begin{bmatrix}n\\k\end{bmatrix}_q = 0 \quad \text{if } k < 0,
\qquad
\begin{bmatrix}n\\k\end{bmatrix}_q = 0 \quad \text{if } n < 0 \text{ and } k > 0.
\]

The last rule is non-standard but essential: when \(h=1\), the factor \(\binom{a+h-2}{a}_q = \binom{a-1}{a}_q\) has \(n = a-1 < 0\) for every \(a \ge 1\), so the function returns zero, causing all \(h=1\) terms with \(a \ge 1\) (or \(b \ge 1\)) to vanish correctly. The only surviving \(h=1\) term is \(a=b=0\), which contributes \(q^r\) to \(h_r(q)\) — the single base-only tooth.

The coefficients are constructed from the product formula

\[
\begin{bmatrix}
n\\k
\end{bmatrix}_q
=
\prod_{i=0}^{k-1}
\frac{1-q^{\,n-i}}
     {1-q^{\,i+1}}.
\]

The result is passed through `sp.factor`, so intermediate values are stored in factored form. This does not affect correctness but makes the symbolic expressions more compact during accumulation.

### Check A: q-series identity

For each \(n\), the script expands

\[
\prod_{i=1}^{n}
\frac{1}{1-tq^i}
\]

as a power series in \(t\).

The coefficient of \(t^a\) is extracted symbolically and compared against

\[
q^a
\begin{bmatrix}
a+n-1\\a
\end{bmatrix}_q.
\]

Any discrepancy would be reported explicitly.

### Check B: Full theorem verification

For each base length \(r\), the script evaluates

\[
\sum_{h\ge1}
\sum_{a,b\ge0 \atop a+b\le r-1}
q^{a+b+h(r-a-b)}
\begin{bmatrix}
a+h-2\\a
\end{bmatrix}_q
\begin{bmatrix}
b+h-2\\b
\end{bmatrix}_q.
\]

The height loop runs over all \(h = 1, \ldots, 25\) without early termination; individual \((a,b,h)\) triples whose q-exponent \(a+b+h(r-a-b)\) already meets or exceeds the target order are skipped via a `continue` guard, but the outer loop is always exhausted. The resulting expression is expanded as a power series through

\[
q^{24},
\]

and compared against the corresponding expansion of \(h_r(q)\).

### Detailed analysis for \(r=3\)

To illustrate the structure of the theorem, the script computes the contribution from each individual height

\[
h=1,2,\ldots
\]

up to order \(q^{11}\).

The separate contributions are printed, accumulated, and then compared against the recurrence-generated series for \(h_3(q)\).

---

## (d) Output produced

### q-series identity verification

For each value of \(n\), the script reports whether

\[
[t^a]
\prod_{i=1}^{n}
\frac{1}{1-tq^i}
=
q^a
\begin{bmatrix}
a+n-1\\a
\end{bmatrix}_q
\]

holds for

\[
a=0,1,2,3,4.
\]

A successful run prints

```
a = 0,1,2,3,4: all match
```

for every tested value of \(n\).

### Verification of Theorem 3

For each base length

\[
r=1,\ldots,6,
\]

the script reports whether the Gaussian-binomial expansion agrees with the recurrence-generated generating function through order

\[
q^{24}.
\]

Typical output is

```
r=3: match up to q^24: True
```

and similarly for the remaining values of \(r\).

### Detailed decomposition of \(h_3(q)\)

The script prints:

* the contribution from each height \(h\);
* the accumulated total;
* the independently generated series \(h_3(q)\);
* confirmation that the two agree through \(q^{11}\).

This provides a concrete illustration of how Theorem 3 builds \(h_3(q)\) from contributions at different heights, and directly reproduces the worked example in Section 5 of the paper, which quotes the \(h=4\) contribution explicitly as \(3q^6+4q^7+7q^8+6q^9+5q^{10}+2q^{11}+q^{12}\).

---

## (e) What we learn

**The Gaussian-binomial identity used in the proof is correct.** The symbolic coefficient extractions confirm the key q-series identity on which the theorem depends.

**Theorem 3 reproduces the recurrence-generated generating functions.** For every tested width \(r\), the explicit Gaussian-binomial expansion agrees coefficient-by-coefficient with the generating functions obtained from the recurrence relation.

**The infinite height sum behaves exactly as expected.** Only finitely many heights contribute to any fixed q-degree, making the theorem computationally well-defined and confirming the convergence argument described in the paper.

**The height decomposition has a clear combinatorial interpretation.** The detailed analysis of the \(r=3\) case demonstrates how contributions from successive heights accumulate to produce the full generating function.

**The theorem provides an explicit combinatorial formula for \(h_r(q)\).** Unlike the recurrence relation, which defines the generating functions indirectly, Theorem 3 expresses them directly in terms of Gaussian binomial coefficients, thereby revealing the underlying q-combinatorial structure of the tooth enumeration problem.
