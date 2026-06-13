# Verification Scripts for "Generating Functions for Temperley's No-Overhang Stacked Partitions"

This repository contains Python scripts that verify the main results of the paper:

> Paul M. King, *Generating Functions for Temperley's No-Overhang Stacked Partitions* (submitted), School of Natural Sciences, Birkbeck, University of London.

The verification scripts use symbolic computation (via [SymPy](https://www.sympy.org)) and exact rational arithmetic to confirm the recurrences, generating function formulae, and combinatorial identities stated in the paper. The repository also contains two utility scripts for generating tooth diagrams and coefficient tables.

## Requirements

- Python 3.8 or later
- [SymPy](https://www.sympy.org) (`pip install sympy`) — required by the four `verify_*.py` scripts
- No external libraries are required by `generate_tooth.py` or `generate_tooth_sequences.py`

## Repository structure

```
.
├── python_scripts/
│   ├── generate_tooth_sequences.py
│   ├── generate_tooth.py
│   ├── verify_conjecture_and_tables.py
│   ├── verify_recurrence.py
│   ├── verify_theorem1.py
│   └── verify_theorem3.py
├── summaries/
│   ├── generate_tooth_sequences_summary.md  (.pdf)
│   ├── generate_tooth_summary.md            (.pdf)
│   ├── verify_conjecture_and_tables_summary.md  (.pdf)
│   ├── verify_recurrence_summary.md         (.pdf)
│   ├── verify_theorem1_summary.md           (.pdf)
│   └── verify_theorem3_summary.md           (.pdf)
└── README.md
```

## Scripts

### `verify_recurrence.py`

Verifies the recurrence relations for the tooth generating functions $h_r(q)$.

- **Check 1.** Computes closed forms $h_r(q) = N_r(q)/(q;q)_r$ for $r = 1, \ldots, 7$ via the two-term recurrence and displays the numerator polynomials $N_r(q)$, matching Table 1 of the paper.
- **Check 2.** Verifies $h_1$, $h_2$, $h_3$ against Temperley's explicit values from his equation (9).
- **Check 3.** Verifies the two-term recurrence (equation (4) of the paper) symbolically for $r = 2, \ldots, 7$.
- **Check 4.** Verifies the multi-term equation (equivalent to Temperley's equation (8)) for $r = 1, \ldots, 7$.
- **Check 5.** Verifies the intermediate identity $F_r - 2qF_{r-1} + q^2F_{r-2} = q^r(2h_{r-1} - h_{r-2})$, where $F_r = (1-q^r)h_r$, confirming that the cross-terms cancel exactly in the derivation of the two-term recurrence.

### `verify_theorem1.py`

Verifies Theorem 1 (the explicit formula for the bivariate generating function $H(y,q)$).

- **Check A.** Verifies the functional equation $H(y,q)(1-qy)^2 = H(qy,q) - qy$ symbolically up to order $y^6$.
- **Check B.** Extracts the coefficients $[y^1]H$ and $[y^2]H$ from the formula symbolically and confirms they equal $h_1(q)$ and $h_2(q)$ respectively (reproducing Remark 4 of the paper).
- **Check C.** Evaluates $H(0.3, 0.5)$ numerically by two independent methods — from the recurrence sum and from the explicit formula — using 40-term truncations, and confirms agreement to at least 10 decimal places.

### `verify_theorem3.py`

Verifies Theorem 3 (the Gaussian binomial expansion of $h_r(q)$).

- **Check A.** Verifies the $q$-series identity $[t^a]\prod_{i=1}^n 1/(1-tq^i) = q^a\binom{a+n-1}{a}_q$ symbolically for $n = 1, 2, 3$ and $a = 0, 1, 2, 3, 4$.
- **Check B.** Verifies the full Gaussian binomial expansion formula for $r = 1, \ldots, 6$, comparing coefficient-by-coefficient against $h_r$ from the recurrence up to $q^{24}$. Also gives a detailed breakdown by height $h$ for $r = 3$, matching the worked example in Section 9 of the paper.

### `verify_conjecture_and_tables.py`

Two independent computations.

- **Part 1.** Verifies Conjecture 1 (the Durfee-type formula $U(t) = \sum_{m \geq 0} q^{m^2} t^{2m} / ((t;q)_m(t;q)_{m+1})$) symbolically by checking that the coefficients of $t^0$ through $t^{15}$ agree on both sides, and displays the first several $u_r(q)$.
- **Part 2.** Computes the coefficient triangle $T(r,N) = [q^N]h_r(q)$ for $r = 1, \ldots, 7$ and $N = 1, \ldots, 15$, matching Table 2 of the paper. Also computes column sums for $N = 1, \ldots, 9$ and spot-checks the closed form $T(2,N) = N-1$.

### `generate_tooth_sequences.py`

Generates and verifies the coefficient triangle $T(r,N) = [q^N]h_r(q)$ using exact rational arithmetic (Python's `fractions.Fraction`), without SymPy.

- Computes $T(r,N)$ for $r = 1, \ldots, 7$ and $N = 1, \ldots, 30$ via the coefficient-level recurrence $T(r,N) = 2T(r-1,N-1) - T(r-2,N-2) + T(r,N-r)$, extending Table 2 of the paper from $N = 15$ to $N = 30$.
- Verifies all computed values for $N = 1, \ldots, 15$ against the hard-coded entries of Table 2.
- Prints the triangle and the individual fixed-base sequences beginning at their first non-zero entry.

### `generate_tooth.py`

Generates an SVG diagram of a specified Temperley tooth (no-overhang stacked partition). This is a standalone utility with no dependency on SymPy or the paper's verification checks.

- Accepts a tooth as a sequence of `(length, offset)` row pairs via the `--rows` argument, validates the no-overhang condition, and renders the tooth as a grid of coloured unit cells.
- Optionally annotates the canonical decomposition parameters $a_i$, $b_i$ (the left shift and right inset between consecutive rows) and $c$ (the top row length) using the `--annotate` flag.
- Supports customisation of cell size, colours, stroke, rounding, padding, and a diagonal linear gradient fill.
- Outputs SVG to stdout or to a file via `-o`.

## Usage

Run the verification scripts from the `python_scripts/` directory:

```bash
cd python_scripts

python verify_recurrence.py
python verify_theorem1.py
python verify_theorem3.py
python verify_conjecture_and_tables.py
python generate_tooth_sequences.py
```

Each verification script prints a structured report of its checks with pass/fail indicators. `generate_tooth_sequences.py` prints the coefficient triangle and a verification message.

To generate a tooth diagram:

```bash
# Tooth of base 7, height 3: rows of lengths 7, 4, 2 with left offsets 0, 2, 3
python generate_tooth.py --rows "7,0 4,2 2,3"

# Same tooth, saved to a file
python generate_tooth.py --rows "7,0 4,2 2,3" -o tooth.svg

# Show canonical decomposition annotations (a_i, b_i, c)
python generate_tooth.py --rows "7,0 4,2 2,3" --annotate

# Custom colours and cell size
python generate_tooth.py --rows "7,0 4,2 2,3" --fill "#0ea5e9" --stroke "#0369a1" --box-size 36
```

Run `python generate_tooth.py --help` for the full list of options.

## Relationship to the paper

| Script | Paper result |
|---|---|
| `verify_recurrence.py` | Equation (3), Equation (4), Table 1, Section 3 derivation |
| `verify_theorem1.py` | Theorem 1, Remark 4 |
| `verify_theorem3.py` | Theorem 3, Section 9 worked example |
| `verify_conjecture_and_tables.py` | Conjecture 1, Table 2 |
| `generate_tooth_sequences.py` | Table 2 (extended to $N = 30$) |
| `generate_tooth.py` | Utility: figures, canonical decomposition |

## Summaries

The `summaries/` directory contains a Markdown and PDF description of each script, explaining the theory, implementation, and output in detail.

## Licence

MIT Licence.

Copyright (c) 2026 Paul M. King

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
