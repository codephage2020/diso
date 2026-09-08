"""Validate presentation attributes and parse diso's orthogonal SVG grammar."""
import math
import re

from markup import Node

PALETTE = {
    "#78c2c4", "#267072", "#9ad8da", "#c47a78", "#8c4644", "#d89d9b",
    "#f5f4ed", "#faf9f5", "#f0eee6", "#e8e6dc", "#30302e", "#1b2e2e",
    "#141413", "#3d3d3a", "#504e49", "#6b6a64", "#e5e3d8",
    "#ddefef", "#e9f4f4", "#cde9e9", "#f4e8e7",
    "#eae9e2", "#e9e8e1", "#edece3", "#d4e7e7",
}
WASH = {"#78c2c4", "#c47a78"}
CELADON = {"#78c2c4", "#267072", "#9ad8da", "#ddefef", "#e9f4f4", "#cde9e9"}
TERRACOTTA = {"#c47a78", "#8c4644", "#d89d9b", "#f4e8e7"}
SVG_NS = "http://www.w3.org/2000/svg"
NUMBER = r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?"
NUMBER_RE = re.compile(NUMBER)
PATH_TOKENS = re.compile(r"[A-Za-z]|" + NUMBER)
PAINT_REF = re.compile(r"url\(\s*(?:'(#[-\w.:]+)'|\"(#[-\w.:]+)\"|(#[-\w.:]+))\s*\)")


def number(value):
    # float() accepts a superset of the NUMBER grammar. Whitespace and digit
    # separators are rejected here; inf/nan pass float() and are caught by the
    # isfinite check right after. The old regex pre-check was redundant work.
    if not isinstance(value, str) or value.strip() != value or "_" in value:
        raise ValueError(f"expected a unitless SVG number, got {value!r}")
    try:
        value = float(value)
    except ValueError:
        raise ValueError(f"expected a unitless SVG number, got {value!r}")
    if not math.isfinite(value):
        raise ValueError("SVG coordinates must be finite")
    return value


def tokenize(value, pattern):
    tokens = []
    position = 0
    for match in pattern.finditer(value):
        gap = value[position:match.start()]
        if gap.strip(" \t\r\n,") or gap.count(",") > 1:
            raise ValueError("invalid SVG geometry syntax")
        if "," in gap and (not tokens or tokens[-1].isalpha() or match[0].isalpha()):
            raise ValueError("misplaced comma in SVG geometry")
        tokens.append(match[0])
        position = match.end()
    if value[position:].strip():
        raise ValueError("invalid SVG geometry syntax")
    return tokens


def numbers(value):
    return [number(t) for t in tokenize(value, NUMBER_RE)]


def path_points(value):
    """Parse M/L/H/V/Z, relative and repeated coordinates, and exponents.

    Curves fail closed. Separate moveto subpaths never create implicit edges.
    """
    tokens = tokenize(value, PATH_TOKENS)
    paths, current = [], []
    point = (0.0, 0.0)
    command = None
    i = 0
    while i < len(tokens):
        if tokens[i].isalpha():
            command = tokens[i]
            i += 1
            if command not in "MmLlHhVvZz":
                raise ValueError(f"unsupported SVG path command {command}; curves are banned")
            if command in "Zz":
                if not current:
                    raise ValueError("closepath without moveto")
                current.append(current[0])
                point = current[0]
                command = None
                continue
        if command is None or (not paths and command not in "Mm"):
            raise ValueError("SVG path must start with moveto")
        count = 1 if command in "HhVv" else 2
        if i + count > len(tokens) or any(t.isalpha() for t in tokens[i:i + count]):
            raise ValueError(f"missing coordinates for {command}")
        coords = [number(t) for t in tokens[i:i + count]]
        i += count
        relative = command.islower()
        if command in "Hh":
            point = (coords[0] + (point[0] if relative else 0), point[1])
        elif command in "Vv":
            point = (point[0], coords[0] + (point[1] if relative else 0))
        else:
            point = tuple(v + (point[j] if relative else 0) for j, v in enumerate(coords))
        if not all(math.isfinite(v) for v in point):
            raise ValueError("SVG coordinates must be finite")
        if command in "Mm":
            current = []
            paths.append(current)
            command = "l" if relative else "L"
        current.append(point)
    if not paths or any(len(p) < 2 for p in paths):
        raise ValueError("SVG path has no edge")
    return paths


def chevron(points):
    if len(points) != 3:
        return False
    (x1, y1), (x2, y2), (x3, y3) = points

    def close(a, b):
        return math.isclose(a, b, rel_tol=0, abs_tol=1e-9)

    vertical = close(y1, y3) and close(x2, (x1 + x3) / 2) and close(abs(x3 - x1), 10) and close(abs(y2 - y1), 7)
    horizontal = close(x1, x3) and close(y2, (y1 + y3) / 2) and close(abs(y3 - y1), 10) and close(abs(x2 - x1), 7)
    return vertical or horizontal


def on_grid(value):
    return math.isclose(value / 4, round(value / 4), abs_tol=1e-8, rel_tol=0)


def check_edges(node, result):
    if node.tag == "path":
        paths = path_points(node.attrs.get("d", ""))
    elif node.tag == "polyline":
        coords = numbers(node.attrs.get("points", ""))
        if len(coords) < 4 or len(coords) % 2:
            raise ValueError("polyline needs coordinate pairs")
        paths = [list(zip(coords[::2], coords[1::2]))]
    else:
        paths = [[(number(node.attrs.get("x1", "0")), number(node.attrs.get("y1", "0"))),
                  (number(node.attrs.get("x2", "0")), number(node.attrs.get("y2", "0")))]]
    if all(a == b for points in paths for a, b in zip(points, points[1:])):
        raise ValueError("SVG edge has no visible segment")
    if node.inherited("fill", "none" if node.tag == "line" else "").lower() != "none":
        result.error(node.line, "edges and chevrons need fill=\"none\"")
    if len(paths) == 1 and chevron(paths[0]):
        if node.inherited("stroke-linecap") != "round" or node.inherited("stroke-linejoin") != "round":
            result.error(node.line, "chevrons need round caps and joins")
        return
    for points in paths:
        if any(x1 != x2 and y1 != y2 for (x1, y1), (x2, y2) in zip(points, points[1:])):
            result.error(node.line, "diagonal SVG edge; only orthogonal segments or exact 5×7 chevrons are allowed")
        if any(not on_grid(v) for point in points for v in point):
            result.error(node.line, "SVG edge coordinates are off the 4px grid")


def check_text(node, result, y=0):
    """Track the vertical text cursor through nested and successive tspans.

    Position attributes use the supported scalar, unitless syntax. A tspan's
    explicit y resets the cursor; dy advances it for subsequent text as well.
    """
    size = 0
    try:
        for attr in ("x", "dx"):
            if attr in node.attrs:
                number(node.attrs[attr])
        if "y" in node.attrs:
            y = number(node.attrs["y"])
        y += number(node.attrs.get("dy", "0"))
        size = number(node.inherited("font-size", "0"))
        if not math.isfinite(y) or size <= 0 or y < size * 1.2:
            result.error(node.line, "text baseline must be ≥ font-size × 1.2; a positive font-size is required")
    except ValueError as exc:
        result.error(node.line, str(exc))
    for child in node.children:
        if isinstance(child, Node) and child.tag == "tspan":
            y = check_text(child, result, y)
        elif isinstance(child, str) and child.strip() and (not math.isfinite(y) or y < size * 1.2):
            # A child can move the cursor; following text resumes this node's size.
            result.error(node.line, "text baseline must be ≥ font-size × 1.2 after tspan positioning")
    return y


def check_svgs(nodes, ids, result):
    svgs = [n for n in nodes if n.tag == "svg"]
    if not svgs:
        result.warn(0, "no SVG figures in the intuition journey")
    total_area = accent_area = 0
    for svg in svgs:
        try:
            vb = numbers(svg.attrs.get("viewbox", ""))
            if len(vb) != 4 or vb[:3] != [0, 0, 960] or vb[3] <= 0:
                raise ValueError("SVG needs viewBox=\"0 0 960 H\" with positive height")
            total_area += 960 * vb[3]
        except ValueError as exc:
            result.error(svg.line, str(exc))
        for tag in ("title", "desc"):
            if not any(isinstance(c, Node) and c.tag == tag and c.text().strip() for c in svg.children):
                result.error(svg.line, f"SVG missing nonempty <{tag}> (accessibility)")
        if svg.attrs.get("xmlns") != SVG_NS:
            result.error(svg.line, "SVG needs its standard xmlns")
        focus = warning = dots = groups = 0
        hues = set()
        for node in svg.walk():
            try:
                for attr in ("fill", "stroke"):
                    if attr not in node.attrs:
                        continue
                    value = node.attrs[attr].lower()
                    ref = PAINT_REF.fullmatch(node.attrs[attr])
                    if ref:
                        fragment = next(g for g in ref.groups() if g)
                        target = ids.get(fragment[1:])
                        if not target or target.tag != "pattern" or target.ancestor("svg") is not svg:
                            result.error(node.line, "paint URL must resolve to a pattern in this SVG")
                    elif value not in PALETTE and value != "none":
                        result.error(node.line, f"{attr}={node.attrs[attr]!r} is outside the six-digit hex palette")
                fill = node.inherited("fill").lower()
                stroke = node.inherited("stroke", "none").lower()
                if node.tag in {"rect", "circle", "text", "tspan"} and not fill:
                    result.error(node.line, "explicit or inherited fill is required (browser black is outside the palette)")
                if node.tag in {"text", "tspan"} and fill in WASH:
                    result.error(node.line, "wash as text fill is illegible; use the ink color")
                if stroke in WASH and node.tag not in {"svg", "g"} and not (stroke == "#78c2c4" and node.tag in {"path", "line", "polyline"} and number(node.inherited("stroke-width", "1")) == 2.5):
                    result.error(node.line, "wash strokes are only allowed as the 2.5px celadon focus path")
                if node.tag in {"rect", "circle", "text", "tspan", "path", "line", "polyline"}:
                    if {fill, stroke} & CELADON:
                        hues.add("celadon")
                    if {fill, stroke} & TERRACOTTA:
                        hues.add("terracotta")
                if "font-weight" in node.attrs and node.attrs["font-weight"] not in {"400", "500"}:
                    result.error(node.line, "SVG font-weight is locked to 400/500")
                for attr in ("opacity", "fill-opacity", "stroke-opacity"):
                    if attr in node.attrs and not 0 <= number(node.attrs[attr]) <= 1:
                        result.error(node.line, f"{attr} must be between 0 and 1")
                for attr in ("rx", "ry"):
                    if attr in node.attrs and not 0 <= number(node.attrs[attr]) <= 10:
                        result.error(node.line, "SVG corner radius must be between 0 and 10")
                if "stroke-width" in node.attrs and number(node.attrs["stroke-width"]) <= 0:
                    result.error(node.line, "stroke-width must be positive")
                if node.tag == "rect":
                    dims = {}
                    canvas = fill == "#f5f4ed" or PAINT_REF.fullmatch(node.attrs.get("fill", ""))
                    for attr in ("x", "y", "width", "height"):
                        value = node.attrs.get(attr, "0")
                        if attr in {"width", "height"} and value == "100%" and canvas:
                            continue
                        dims[attr] = number(value)
                        if not on_grid(dims[attr]):
                            result.error(node.line, f"rect {attr} is off the 4px grid")
                        if attr in {"width", "height"} and dims[attr] <= 0:
                            result.error(node.line, f"rect {attr} must be positive")
                    if fill in WASH and "width" in dims and "height" in dims:
                        accent_area += dims["width"] * dims["height"]
                    if fill in WASH:
                        focus += fill == "#78c2c4"
                        warning += fill == "#c47a78"
                    groups += fill == "#edece3"
                    # Rounded/stroked boxes are nodes. Square book bars, canvas
                    # pads and unstroked illustrations have their own dimensions.
                    is_node = node.attrs.get("data-node") == "true" or (stroke != "none" and ("rx" in node.attrs or "ry" in node.attrs))
                    if "data-node" in node.attrs and node.attrs["data-node"] != "true":
                        result.error(node.line, "data-node only accepts true")
                    if is_node and (dims.get("width") not in {128, 144, 160} or dims.get("height") not in {32, 64}):
                        result.error(node.line, "node dimensions must be 128/144/160 × 32/64")
                if node.tag == "circle":
                    radius = number(node.attrs.get("r", "0"))
                    for attr in ("cx", "cy"):
                        number(node.attrs.get(attr, "0"))
                    if radius <= 0:
                        result.error(node.line, "circle radius must be positive")
                    # Wash circles are accent fills too: count them and weigh
                    # them by area, same as wash rects.
                    if fill in WASH:
                        focus += fill == "#78c2c4"
                        warning += fill == "#c47a78"
                        accent_area += math.pi * radius * radius
                    dots += radius == 12 and fill == "#267072"
                if node.tag in {"path", "line", "polyline"}:
                    if stroke == "none":
                        result.error(node.line, "SVG edges require a visible stroke")
                    check_edges(node, result)
                if node.tag == "text":
                    check_text(node, result)
                if node.tag == "tspan" and (node.parent.tag not in {"text", "tspan"} or not node.ancestor("text")):
                    result.error(node.line, "tspan needs a text parent (directly or through tspans)")
            except ValueError as exc:
                result.error(node.line, str(exc))
        if len(hues) > 1:
            result.error(svg.line, "one accent hue per SVG; celadon and terracotta are mixed")
        for count, maximum, name in ((focus, 2, "focus nodes"), (warning, 1, "warning nodes"), (dots, 6, "sequence dots"), (groups, 2, "group containers")):
            if count > maximum:
                result.error(svg.line, f"{count} {name}; at most {maximum}")
    if total_area and accent_area / total_area > 0.05:
        result.warn(0, f"solid accent fills ≈{100 * accent_area / total_area:.1f}% of SVG canvas area; budget is 5%")
