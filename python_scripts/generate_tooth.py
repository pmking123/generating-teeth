#!/usr/bin/env python3
"""
Generate Tooth Diagram SVG

A Python script that generates an SVG diagram of a Temperley tooth —
a no-overhang stacked partition as defined in the paper.

A tooth of base r is a sequence of rows of unit cubes with:
  - Row lengths lambda_1 = r >= lambda_2 >= ... >= lambda_h >= 1 (weakly decreasing).
  - Left offsets x_1, x_2, ..., x_h satisfying the no-overhang condition:
      0 <= x_{i+1} - x_i <= lambda_i - lambda_{i+1}  for each i.

Input is given as a sequence of (length, offset) pairs, one per row,
starting from the base row (bottom). Row 1 is always drawn at the bottom.

Optionally, the canonical decomposition parameters a_i, b_i (for i = 1, ..., h-1)
and c = lambda_h can be annotated on the diagram.

Usage examples:
  # A tooth of base 7, height 3: rows (7,0), (4,2), (2,3)
  python generate_tooth.py --rows "7,0 4,2 2,3"

  # Same tooth, output to file
  python generate_tooth.py --rows "7,0 4,2 2,3" -o tooth.svg

  # Show decomposition annotations (a_i, b_i, c)
  python generate_tooth.py --rows "7,0 4,2 2,3" --annotate

  # Customise colours and box size
  python generate_tooth.py --rows "7,0 4,2 2,3" --fill "#0ea5e9" --stroke "#0369a1" --box-size 36
"""

import argparse
import sys
import xml.etree.ElementTree as ET
from xml.dom import minidom


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_tooth(rows):
    """
    Validate that the given rows form a valid tooth.

    rows: list of (lambda_i, x_i) pairs, row 1 (base) first.

    Raises ValueError with a descriptive message on any violation.
    Returns (lambdas, offsets).
    """
    if not rows:
        raise ValueError("A tooth must have at least one row.")

    lambdas = [r[0] for r in rows]
    offsets = [r[1] for r in rows]

    # Check lengths are positive and weakly decreasing
    for i, lam in enumerate(lambdas):
        if lam < 1:
            raise ValueError(f"Row {i+1} has non-positive length {lam}.")
    for i in range(len(lambdas) - 1):
        if lambdas[i+1] > lambdas[i]:
            raise ValueError(
                f"Row lengths must be weakly decreasing: "
                f"lambda_{i+2} = {lambdas[i+1]} > lambda_{i+1} = {lambdas[i]}."
            )

    # Check base row offset is 0
    if offsets[0] != 0:
        raise ValueError(
            f"The base row (row 1) must have offset 0, got {offsets[0]}."
        )

    # Check no-overhang condition for each consecutive pair
    for i in range(len(rows) - 1):
        lam_i  = lambdas[i]
        lam_i1 = lambdas[i+1]
        x_i    = offsets[i]
        x_i1   = offsets[i+1]
        delta  = x_i1 - x_i
        slack  = lam_i - lam_i1
        if delta < 0:
            raise ValueError(
                f"No-overhang violated between rows {i+1} and {i+2}: "
                f"x_{i+2} - x_{i+1} = {delta} < 0 (left overhang)."
            )
        if delta > slack:
            raise ValueError(
                f"No-overhang violated between rows {i+1} and {i+2}: "
                f"x_{i+2} - x_{i+1} = {delta} > lambda_{i+1} - lambda_{i+2} = {slack} (right overhang)."
            )

    return lambdas, offsets


# ---------------------------------------------------------------------------
# Decomposition parameters
# ---------------------------------------------------------------------------

def compute_decomposition(lambdas, offsets):
    """
    Compute the canonical decomposition parameters a_i, b_i, c.

      a_i = x_{i+1} - x_i       (left shift between rows i and i+1)
      b_i = (lambda_i - lambda_{i+1}) - a_i   (right inset)
      c   = lambda_h             (top row length)

    Returns (a_list, b_list, c) where a_list and b_list have length h-1.
    """
    h = len(lambdas)
    a_list = []
    b_list = []
    for i in range(h - 1):
        a_i = offsets[i+1] - offsets[i]
        b_i = (lambdas[i] - lambdas[i+1]) - a_i
        a_list.append(a_i)
        b_list.append(b_i)
    c = lambdas[-1]
    return a_list, b_list, c


# ---------------------------------------------------------------------------
# SVG helpers
# ---------------------------------------------------------------------------

def prettify(elem):
    """Returns a pretty-printed XML string for the Element."""
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    pretty_str = reparsed.toprettyxml(indent="  ")
    return "\n".join([line for line in pretty_str.splitlines() if line.strip()])


# ---------------------------------------------------------------------------
# Main SVG generation
# ---------------------------------------------------------------------------

def generate_tooth_svg(
    rows,
    box_size=40,
    spacing=2,
    fill_color="#4f46e5",
    stroke_color="#312e81",
    stroke_width=2,
    rounded=4,
    padding=20,
    gradient_colors=None,
    text_color="#ffffff",
    font_size=12,
    font_family="sans-serif",
    annotate=False,
    annot_color="#e11d48",
    annot_font_size=11,
):
    """
    Generate an SVG diagram of a tooth.

    rows     : list of (lambda_i, x_i) pairs, row 1 (base) at index 0.
    annotate : if True, label the a_i, b_i, c decomposition parameters.
    """
    lambdas, offsets = validate_tooth(rows)
    h = len(lambdas)
    r = lambdas[0]  # base length

    # The maximum rightward extent determines canvas width
    max_right = max(offsets[i] + lambdas[i] for i in range(h))

    # Canvas dimensions: rows are stacked bottom-to-top in the diagram.
    # In SVG coordinates, row 1 (base) is drawn at the bottom.
    cell = box_size + spacing
    svg_width  = padding * 2 + max_right * cell - spacing
    svg_height = padding * 2 + h * cell - spacing

    svg = ET.Element('svg', {
        'xmlns': 'http://www.w3.org/2000/svg',
        'width':   str(svg_width),
        'height':  str(svg_height),
        'viewBox': f"0 0 {svg_width} {svg_height}",
    })

    # Optional gradient
    actual_fill = fill_color
    if gradient_colors and len(gradient_colors) >= 2:
        defs = ET.SubElement(svg, 'defs')
        grad = ET.SubElement(defs, 'linearGradient', {
            'id': 'tooth-gradient',
            'x1': '0%', 'y1': '0%', 'x2': '100%', 'y2': '100%',
        })
        ET.SubElement(grad, 'stop', {
            'offset': '0%',
            'stop-color': gradient_colors[0],
            'stop-opacity': '1',
        })
        ET.SubElement(grad, 'stop', {
            'offset': '100%',
            'stop-color': gradient_colors[1],
            'stop-opacity': '1',
        })
        actual_fill = 'url(#tooth-gradient)'

    # Draw rows bottom-to-top.
    # Row index 0 (base) maps to the bottom of the SVG.
    for i in range(h):
        lam_i = lambdas[i]
        x_i   = offsets[i]
        # SVG y-coordinate: row 0 is at the bottom
        svg_row = h - 1 - i
        y = padding + svg_row * cell

        for col in range(lam_i):
            x = padding + (x_i + col) * cell

            rect_attribs = {
                'x':      str(x),
                'y':      str(y),
                'width':  str(box_size),
                'height': str(box_size),
                'fill':   actual_fill,
            }
            if stroke_color and stroke_width > 0:
                rect_attribs['stroke']       = stroke_color
                rect_attribs['stroke-width'] = str(stroke_width)
            if rounded > 0:
                rect_attribs['rx'] = str(rounded)
                rect_attribs['ry'] = str(rounded)
            ET.SubElement(svg, 'rect', rect_attribs)

    # ---------------------------------------------------------------------------
    # Decomposition annotations
    # ---------------------------------------------------------------------------
    if annotate and h > 1:
        a_list, b_list, c = compute_decomposition(lambdas, offsets)

        ann_style = {
            'font-size':   str(annot_font_size),
            'font-family': font_family,
            'font-weight': 'bold',
            'fill':        annot_color,
            'text-anchor': 'middle',
            'dominant-baseline': 'central',
        }

        # Place a_i and b_i labels between row i and row i+1.
        # We draw a small brace/line above each row boundary to indicate
        # the a_i (left shift) and b_i (right inset) spans.
        bracket_y_offset = box_size // 2   # vertical offset into the gap above a row

        for i in range(h - 1):
            a_i = a_list[i]
            b_i = b_list[i]
            x_i   = offsets[i]
            x_i1  = offsets[i+1]
            lam_i  = lambdas[i]
            lam_i1 = lambdas[i+1]

            # y-coordinate of the boundary between row i and row i+1 in SVG space
            svg_row_i = h - 1 - i
            boundary_y = padding + svg_row_i * cell - spacing // 2

            # --- a_i label: covers columns x_i to x_i + a_i - 1 (left shift) ---
            if a_i > 0:
                ax_left  = padding + x_i * cell
                ax_right = padding + x_i1 * cell
                ax_mid   = (ax_left + ax_right) / 2
                ay       = boundary_y - annot_font_size - 2

                # Horizontal bracket line
                ET.SubElement(svg, 'line', {
                    'x1': str(ax_left + box_size // 4),
                    'y1': str(ay),
                    'x2': str(ax_right - box_size // 4),
                    'y2': str(ay),
                    'stroke':       annot_color,
                    'stroke-width': '1.5',
                })
                t = ET.SubElement(svg, 'text', {**ann_style,
                    'x': str(ax_mid),
                    'y': str(ay - annot_font_size),
                })
                t.text = f"a={a_i}"

            # --- b_i label: covers the right inset ---
            if b_i > 0:
                # b_i spans the right-hand reduction that is not a left shift
                bx_left  = padding + (x_i1 + lam_i1) * cell
                bx_right = padding + (x_i + lam_i) * cell
                bx_mid   = (bx_left + bx_right) / 2
                by       = boundary_y - annot_font_size - 2

                ET.SubElement(svg, 'line', {
                    'x1': str(bx_left + box_size // 4),
                    'y1': str(by),
                    'x2': str(bx_right - box_size // 4),
                    'y2': str(by),
                    'stroke':       annot_color,
                    'stroke-width': '1.5',
                })
                t = ET.SubElement(svg, 'text', {**ann_style,
                    'x': str(bx_mid),
                    'y': str(by - annot_font_size),
                })
                t.text = f"b={b_i}"

        # --- c label: top row length ---
        top_row   = h - 1
        svg_row_top = 0
        cx_left  = padding + offsets[top_row] * cell
        cx_right = padding + (offsets[top_row] + lambdas[top_row]) * cell
        cx_mid   = (cx_left + cx_right) / 2
        cy       = padding - annot_font_size - 4

        t = ET.SubElement(svg, 'text', {**ann_style,
            'x': str(cx_mid),
            'y': str(cy),
        })
        t.text = f"c={c}"

        # Summary line at bottom
        summary_parts = [f"c={c}"]
        for i in range(h - 1):
            summary_parts.append(f"(a={a_list[i]},b={b_list[i]})")
        summary = "  ".join(summary_parts)
        summary_y = padding + h * cell + annot_font_size + 4
        t = ET.SubElement(svg, 'text', {
            'x': str(svg_width // 2),
            'y': str(summary_y),
            'font-size':   str(annot_font_size),
            'font-family': font_family,
            'fill':        '#475569',
            'text-anchor': 'middle',
            'dominant-baseline': 'central',
        })
        t.text = f"r = {r},  h = {h}:  {summary}"

        # Adjust SVG height to include summary line
        new_height = summary_y + annot_font_size + padding
        svg.set('height', str(new_height))
        svg.set('viewBox', f"0 0 {svg_width} {new_height}")

    return prettify(svg)


# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------

def parse_rows(rows_str):
    """
    Parse a rows string like "7,0 4,2 2,3" into a list of (length, offset) pairs.
    Each token is "length,offset".
    """
    pairs = []
    for token in rows_str.strip().split():
        parts = token.split(',')
        if len(parts) != 2:
            raise argparse.ArgumentTypeError(
                f"Each row must be specified as 'length,offset', got '{token}'."
            )
        try:
            lam = int(parts[0])
            x   = int(parts[1])
        except ValueError:
            raise argparse.ArgumentTypeError(
                f"Row values must be integers, got '{token}'."
            )
        pairs.append((lam, x))
    return pairs


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Generate an SVG diagram of a Temperley tooth (no-overhang stacked partition)."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog=(
            "Example: python generate_tooth.py --rows \"7,0 4,2 2,3\" --annotate -o tooth.svg\n"
            "Rows are given as 'length,offset' pairs starting from the base row."
        ),
    )

    parser.add_argument(
        '--rows', '-r',
        type=str,
        required=True,
        help=(
            "Row specifications as space-separated 'length,offset' pairs, "
            "base row first. "
            "Example: \"7,0 4,2 2,3\" gives a tooth with rows of lengths 7, 4, 2 "
            "and left offsets 0, 2, 3."
        ),
    )

    parser.add_argument(
        '-o', '--output',
        type=str,
        help="Output SVG file path. If not provided, outputs to stdout.",
    )

    parser.add_argument(
        '--box-size',
        type=int,
        default=40,
        help="Size of each unit cube cell in pixels.",
    )

    parser.add_argument(
        '--spacing',
        type=int,
        default=2,
        help="Spacing between adjacent cells in pixels.",
    )

    parser.add_argument(
        '--fill',
        type=str,
        default="#4f46e5",
        help="Fill colour of the cells.",
    )

    parser.add_argument(
        '--stroke',
        type=str,
        default="#312e81",
        help="Border colour of the cells.",
    )

    parser.add_argument(
        '--stroke-width',
        type=float,
        default=2.0,
        help="Border width of the cells in pixels.",
    )

    parser.add_argument(
        '--rounded',
        type=int,
        default=4,
        help="Corner radius (rx/ry) for rounded cells.",
    )

    parser.add_argument(
        '--padding',
        type=int,
        default=20,
        help="Padding around the diagram in pixels.",
    )

    parser.add_argument(
        '--gradient',
        type=str,
        default=None,
        help=(
            "Comma-separated pair of colours for a diagonal linear gradient fill "
            "(e.g. '#818cf8,#4f46e5'). Overrides --fill."
        ),
    )

    parser.add_argument(
        '--font-size',
        type=int,
        default=12,
        help="Font size for cell annotations in pixels.",
    )

    parser.add_argument(
        '--font-family',
        type=str,
        default="sans-serif",
        help="Font family for annotations.",
    )

    parser.add_argument(
        '--annotate',
        action='store_true',
        help=(
            "Annotate the canonical decomposition parameters: "
            "a_i (left shift), b_i (right inset) between consecutive rows, "
            "and c (top row length)."
        ),
    )

    parser.add_argument(
        '--annot-color',
        type=str,
        default="#e11d48",
        help="Colour for decomposition annotations.",
    )

    parser.add_argument(
        '--annot-font-size',
        type=int,
        default=11,
        help="Font size for decomposition annotations in pixels.",
    )

    args = parser.parse_args()

    try:
        rows = parse_rows(args.rows)
    except argparse.ArgumentTypeError as e:
        print(f"Error parsing --rows: {e}", file=sys.stderr)
        sys.exit(1)

    gradient_colors = None
    if args.gradient:
        gradient_colors = [c.strip() for c in args.gradient.split(',') if c.strip()]

    try:
        svg_content = generate_tooth_svg(
            rows=rows,
            box_size=args.box_size,
            spacing=args.spacing,
            fill_color=args.fill,
            stroke_color=args.stroke,
            stroke_width=args.stroke_width,
            rounded=args.rounded,
            padding=args.padding,
            gradient_colors=gradient_colors,
            font_size=args.font_size,
            font_family=args.font_family,
            annotate=args.annotate,
            annot_color=args.annot_color,
            annot_font_size=args.annot_font_size,
        )
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        print(f"Tooth diagram saved to {args.output}")
    else:
        print(svg_content)


if __name__ == '__main__':
    main()
