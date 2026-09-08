"""The deliberately small HTML/SVG vocabulary accepted by diso."""
import os
import re
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDENTIFIER = r"[A-Za-z][A-Za-z0-9_.:-]*"
IDENTIFIER_RE = re.compile(IDENTIFIER)
RASTER_RE = re.compile(r"data:image/(png|jpeg|gif|webp);base64,([A-Za-z0-9+/]*={0,2})")
VOID = {"meta", "br", "hr", "img", "col"}
HTML_TAGS = set("html head meta title style body nav main article header footer section div span p h1 h2 h3 ul ol li table thead tbody tfoot tr th td caption colgroup col b strong code pre blockquote details summary a br hr figure figcaption sup sub dl dt dd time abbr kbd samp img".split())
SVG_TAGS = {"svg", "title", "desc", "defs", "pattern", "g", "rect", "circle", "text", "tspan", "path", "line", "polyline"}
GLOBAL_ATTRS = {"id", "class", "lang", "dir", "title", "role"}
HTML_ATTRS = {
    "html": {"data-mode"}, "meta": {"charset", "name", "content"},
    "a": {"href", "target", "rel"}, "details": {"open"},
    "th": {"scope", "colspan", "rowspan"}, "td": {"colspan", "rowspan"},
    "col": {"span"}, "colgroup": {"span"}, "ol": {"start", "reversed"},
    "li": {"value"}, "time": {"datetime"},
    "img": {"src", "alt", "width", "height"},
}
PRESENTATION = {"fill", "stroke", "stroke-width", "stroke-linecap", "stroke-linejoin",
                "stroke-dasharray", "opacity", "fill-opacity", "stroke-opacity",
                "font-family", "font-size", "font-weight", "text-anchor"}
SVG_ATTRS = {
    "svg": {"xmlns", "viewbox"},
    "pattern": {"width", "height", "x", "y", "patternunits"},
    "rect": {"x", "y", "width", "height", "rx", "ry", "data-node"},
    "circle": {"cx", "cy", "r"},
    "text": {"x", "y"}, "tspan": {"x", "y", "dx", "dy"},
    "path": {"d"}, "line": {"x1", "y1", "x2", "y2"}, "polyline": {"points"},
}


class Node:
    # Plain classes keep the hot import path free of the dataclasses machinery.
    __slots__ = ("tag", "attrs", "line", "parent", "children", "svg", "_classes")

    def __init__(self, tag, attrs, line, parent=None):
        self.tag = tag
        self.attrs = attrs
        self.line = line
        self.parent = parent
        self.children = []
        self._classes = None
        # Cached once at parse time: ancestor("svg") is called for nearly
        # every node in check_markup, and walking parents repeatedly costs
        # more than every parse-time assignment.
        self.svg = self if tag == "svg" else (parent.svg if parent is not None and isinstance(parent, Node) else None)

    def walk(self):
        # Iterative traversal: the recursive generator re-entered walk()
        # once per node (76k+ generator frames per validate on the example).
        stack = [self]
        while stack:
            node = stack.pop()
            yield node
            for child in reversed(node.children):
                if isinstance(child, Node):
                    stack.append(child)

    def text(self):
        return "".join(c.text() if isinstance(c, Node) else c for c in self.children)

    def has_class(self, name):
        # Hot helper (hundreds of calls per validate). A node's class list is
        # fixed once parsed, so split lazily once and cache on the instance.
        cached = self._classes
        if cached is None:
            cached = self._classes = self.attrs.get("class", "").split()
        return name in cached

    def ancestor(self, tag):
        node = self
        while node:
            if node.tag == tag:
                return node
            node = node.parent
        return None

    def in_svg(self):
        return self.svg is not None

    def inherited(self, name, default=""):
        node = self
        while node and node.tag != "#document":
            if name in node.attrs:
                return node.attrs[name]
            node = node.parent
        return default


class Result:
    __slots__ = ("errors", "warnings")

    def __init__(self):
        self.errors = []
        self.warnings = []

    def error(self, line, message):
        self.errors.append((line, message))

    def warn(self, line, message):
        self.warnings.append((line, message))

    @property
    def ok(self):
        return not (self.errors or self.warnings)


class Document(HTMLParser):
    """Require explicitly closed elements; do not emulate browser error repair."""
    def __init__(self, result):
        super().__init__(convert_charrefs=True)
        self.result = result
        self.root = Node("#document", {}, 1)
        self.stack = [self.root]
        self.doctypes = 0

    def handle_starttag(self, tag, attrs):
        line = self.getpos()[0]
        # attrs is a list of (name, value-or-None); collapse to a dict for the
        # Node while flagging duplicate names (None values become empty strings).
        node_attrs = {}
        for name, value in attrs:
            if name in node_attrs:
                self.result.error(line, "duplicate attributes are ambiguous")
            node_attrs[name] = value or ""
        node = Node(tag, node_attrs, line, self.stack[-1])
        self.stack[-1].children.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            if not self.stack[-1].ancestor("svg"):
                self.result.error(self.getpos()[0], f"HTML <{tag}> needs an explicit closing tag")
            self.stack.pop()

    def handle_endtag(self, tag):
        if len(self.stack) == 1 or self.stack[-1].tag != tag:
            self.result.error(self.getpos()[0], f"unmatched closing </{tag}>")
            return
        self.stack.pop()

    def handle_data(self, data):
        self.stack[-1].children.append(data)

    def handle_decl(self, decl):
        if decl.lower() != "doctype html":
            self.result.error(self.getpos()[0], "only <!DOCTYPE html> is supported")
        self.doctypes += 1

    def unknown_decl(self, data):
        self.result.error(self.getpos()[0], "unsupported declaration")

    def handle_pi(self, data):
        self.result.error(self.getpos()[0], "processing instructions are unsupported")

    def handle_comment(self, data):
        # Browsers also close comments abruptly at <!--> and <!--->, while
        # HTMLParser keeps scanning to the next -->. Reject both early-close
        # shapes so markup after them cannot hide inside a "comment".
        if "--" in data or data.startswith((">", "-")) or data.endswith("<!-"):
            self.result.error(self.getpos()[0], "malformed HTML comment")


def parse_html(raw, result=None):
    result = result if result is not None else Result()
    document = Document(result)
    document.feed(raw)
    document.close()
    for node in document.stack[1:]:
        result.error(node.line, f"unclosed <{node.tag}>")
    return document


def trusted_stylesheet():
    with open(os.path.join(ROOT, "assets", "base.html"), encoding="utf-8") as stream:
        asset = stream.read()
    return asset.split("<style>", 1)[1].split("</style>", 1)[0].strip()


def valid_link(value):
    """Only passive HTTP(S) citations and document fragments are supported."""
    if not value or "\\" in value:
        return False
    # Any control character (including whitespace) anywhere, or DEL, kills the
    # link: schemes like "java\x01script:" hide payloads between the checks.
    if any(ord(c) <= 32 or ord(c) == 127 for c in value):
        return False
    if value.startswith("#"):
        return bool(IDENTIFIER_RE.fullmatch(value[1:]))
    from urllib.parse import urlsplit
    try:
        url = urlsplit(value)
        return url.scheme.lower() in {"http", "https"} and bool(url.hostname)
    except ValueError:
        return False


def raster_data(value):
    from base64 import b64decode
    match = RASTER_RE.fullmatch(value)
    if not match:
        return False
    try:
        data = b64decode(match[2], validate=True)
    except ValueError:
        return False
    return {"png": data.startswith(b"\x89PNG\r\n\x1a\n"),
            "jpeg": data.startswith(b"\xff\xd8\xff"),
            "gif": data.startswith((b"GIF87a", b"GIF89a")),
            "webp": data.startswith(b"RIFF") and data[8:12] == b"WEBP"}[match[1]]


def check_markup(document, result):
    nodes = list(document.root.walk())[1:]
    ids = {}
    for node in nodes:
        svg = node.svg
        if node.tag not in (SVG_TAGS if svg else HTML_TAGS):
            result.error(node.line, f"<{node.tag}> is unsupported; use static HTML and inline SVG")
        if node.tag == "svg" and node.parent.svg:
            result.error(node.line, "nested SVG canvases are unsupported")
        attrs = GLOBAL_ATTRS | (PRESENTATION | SVG_ATTRS.get(node.tag, set()) if svg else HTML_ATTRS.get(node.tag, set()))
        for name, value in node.attrs.items():
            if name not in attrs and not name.startswith("aria-"):
                result.error(node.line, f"unsupported attribute {name!r} on <{node.tag}>")
            if name == "style":
                result.error(node.line, "inline CSS is unsupported; use the bundled classes")
            if name.startswith("on"):
                result.error(node.line, "event handlers violate zero-JS")
            if name == "id":
                if not IDENTIFIER_RE.fullmatch(value):
                    result.error(node.line, f"invalid id {value!r}")
                if value in ids:
                    result.error(node.line, f"duplicate id {value!r}")
                ids[value] = node
            if name in {"href", "xlink:href"} and (node.tag != "a" or svg or not valid_link(value)):
                result.error(node.line, "only HTML citation links and local anchors may use href")
        if node.tag == "img" and (not raster_data(node.attrs.get("src", "")) or not node.attrs.get("alt")):
            result.error(node.line, "img needs alt text and a base64 PNG/JPEG/GIF/WebP; no external or relative assets")
        if node.tag == "meta":
            if node.attrs.get("charset", "utf-8").lower() != "utf-8":
                result.error(node.line, "the document encoding must be UTF-8")
            if "charset" not in node.attrs and node.attrs.get("name", "").lower() not in {"viewport", "description"}:
                result.error(node.line, "only charset, viewport and description metadata are supported")
        if node.tag == "style" and (svg or node.parent.tag != "head" or node.attrs):
            result.error(node.line, "the stylesheet must be an unqualified <style> in <head>")
    for node in nodes:
        href = node.attrs.get("href", "")
        if href.startswith("#") and href[1:] not in ids:
            result.error(node.line, f"anchor {href} resolves to nothing")
    styles = [n for n in nodes if n.tag == "style"]
    if len(styles) != 1 or styles[0].text().strip() != trusted_stylesheet():
        result.error(0, "stylesheet differs from assets/base.html; rebuild with scripts/build.py (no custom CSS)")
    return nodes, ids
