import copy
from html import escape
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build import LABELS, render
from check import validate
from markup import Result, parse_html
from svg import check_svgs, path_points


class PipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / "examples/btree-index.json").read_text(encoding="utf-8"))
        cls.page = render(cls.data)

    def assertClean(self, page):
        result = validate(page)
        self.assertTrue(result.ok, result.errors + result.warnings)

    def assertRejected(self, page, message=None):
        result = validate(page)
        self.assertFalse(result.ok)
        if message:
            self.assertTrue(any(message in text for _, text in result.errors + result.warnings), result)

    def inject(self, html):
        return self.page.replace("</main>", html + "</main>")

    def inject_svg(self, html):
        return self.page.replace("</svg>", html + "</svg>", 1)

    def test_example_is_reproducible_and_clean(self):
        self.assertEqual(self.page, (ROOT / "examples/diso-btree-index.html").read_text(encoding="utf-8"))
        self.assertClean(self.page)

    def test_positive_and_negative_markup_fixtures(self):
        fixtures = json.loads((ROOT / "tests/fixtures/markup.json").read_text(encoding="utf-8"))
        for case in fixtures:
            with self.subTest(case["name"]):
                page = self.inject(case["html"])
                self.assertClean(page) if case["valid"] else self.assertRejected(page)

    def test_embedded_raster_is_allowed_but_svg_and_external_assets_are_not(self):
        # A real inline 1x1 PNG, not a relative or remote dependency.
        png = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+aD1sAAAAASUVORK5CYII="
        self.assertClean(self.inject(f'<img alt="pixel" src="data:image/png;base64,{png}">'))
        self.assertRejected(self.inject('<img alt="pixel" src="data:image/png;base64,invalid">'))

    def test_css_is_bounded_to_the_asset(self):
        for css in ("p{color:red}", "p{color:rgb(20,20,19)}", "p{color:#fff}",
                    "p{color:#141413ff}", "p{color:color-mix(in srgb,red,blue)}",
                    "@import 'a.css';", "p{background:url(a.png)}", "p{border-radius:99px}",
                    "p{font-weight:700}", "p{font-style:italic}"):
            with self.subTest(css):
                self.assertRejected(self.page.replace("</style>", css + "</style>"), "stylesheet differs")

    def test_svg_color_formats_and_inheritance(self):
        for color in ("red", "rgb(20,20,19)", "#fff", "#ffff", "#141413ff", "#000000", "currentColor", "var(--brand)", "color-mix(in srgb,red,blue)"):
            with self.subTest(color):
                self.assertRejected(self.inject_svg(f'<rect x="4" y="4" width="32" height="32" fill="{color}"/>'), "palette")
        self.assertClean(self.inject_svg('<g fill="#141413"><rect x="4" y="4" width="32" height="32"/></g>'))
        self.assertRejected(self.inject_svg('<g fill="red"><rect x="4" y="4" width="32" height="32"/></g>'), "palette")
        self.assertRejected(self.page.replace('role="img"', 'role="img" fill="red"', 1), "palette")
        self.assertRejected(self.inject_svg('<g fill="#78c2c4"><text x="32" y="64" font-size="26">wash</text></g>'), "wash as text")

    def test_svg_resource_and_transform_bypasses(self):
        for markup in ('<image href="a.svg"/>', '<use href="a.svg#x"/>', '<use href="#dots1"/>',
                       '<foreignObject><p>foreign</p></foreignObject>', '<animate attributeName="href" values="javascript:alert(1)"/>',
                       '<set attributeName="fill" to="red"/>', '<marker id="arrow"/>',
                       '<g transform="rotate(45)"><path d="M0 0 H40" stroke="#141413" fill="none"/></g>',
                       '<rect x="4" y="4" width="32" height="32" fill="url(a.svg#x)"/>'):
            with self.subTest(markup):
                self.assertRejected(self.inject_svg(markup))

    def test_only_internal_existing_patterns_are_allowed(self):
        self.assertClean(self.page)
        self.assertRejected(self.page.replace('url(#dots1)', 'url(#missing)', 1), "pattern")
        self.assertRejected(self.page.replace('url(#dots1)', 'url(#dots2)', 1), "pattern")
        self.assertRejected(self.page.replace('url(#dots1)', 'url(#p1)', 1), "pattern")

    def test_curves_and_general_three_point_paths_fail(self):
        invalid = ["M0 0 C10 10 20 20 40 40", "M0 0 Q20 20 40 40", "M0 0 A10 10 0 0 1 40 40",
                   "M0 0 S20 20 40 40", "M0 0 T40 40", "M0 0 l40 40", "M0 0 L40 40 L80 0",
                   "M0 0 40 40 80 0", "M0 0 H40 V40 Z", "M0 0 L", "M0 0 C", "L0 0 L40 0", "M0 0 HNaN"]
        for d in invalid:
            with self.subTest(d):
                self.assertRejected(self.inject_svg(f'<path d="{d}" fill="none" stroke="#141413"/>'))

    def test_relative_implicit_and_horizontal_vertical_paths(self):
        valid = ["M0 0 H40 V40 H80", "m0 0 h40 v40 h40", "M0 0 40 0 40 40", "M0 0 h4e1 v+40",
                 "M0 0 H40 M80 80 V120", "M0,0 L40,0 L40,40 L0,40 Z", "m40 40 l-40 0 0-40"]
        for d in valid:
            with self.subTest(d):
                self.assertClean(self.inject_svg(f'<path d="{d}" fill="none" stroke="#141413"/>'))
        self.assertEqual(path_points("M40 40 h40 v40"), [[(40, 40), (80, 40), (80, 80)]])

    def test_lines_polylines_and_chevrons(self):
        self.assertClean(self.inject_svg('<line x1="0" y1="0" x2="40" y2="0" stroke="#141413"/>'))
        self.assertRejected(self.inject_svg('<line x1="0" y1="0" x2="40" y2="40" stroke="#141413"/>'), "diagonal")
        self.assertClean(self.inject_svg('<polyline points="0,0 40,0 40,40" fill="none" stroke="#141413"/>'))
        self.assertRejected(self.inject_svg('<polyline points="0,0 40,40 80,0" fill="none" stroke="#141413"/>'), "diagonal")
        for d in ("M475 205 L480 212 L485 205", "M475 219 L480 212 L485 219", "M473 207 L480 212 L473 217", "M487 207 L480 212 L487 217"):
            with self.subTest(d):
                self.assertClean(self.inject_svg(f'<path d="{d}" fill="none" stroke="#141413" stroke-linecap="round" stroke-linejoin="round"/>'))

    def test_edge_paint_case_and_degenerate_segments(self):
        self.assertRejected(self.inject_svg('<path d="M0 0 H40" stroke="#C47A78" stroke-width="2.5" fill="none"/>'), "wash strokes")
        self.assertClean(self.inject_svg('<path d="M0 0 H40" stroke="#141413" fill="NONE"/>'))
        self.assertRejected(self.inject_svg('<path d="M0 0 Z" stroke="#141413" fill="none"/>'), "no visible segment")
        self.assertRejected(self.inject_svg('<line x1="0" y1="0" x2="0" y2="0" stroke="#141413"/>'), "no visible segment")

    def test_chevron_allows_float_noise_at_off_grid_origins(self):
        self.assertClean(self.inject_svg('<path d="M0.2 0 L5.2 7 L10.2 0" fill="none" stroke="#141413" stroke-linecap="round" stroke-linejoin="round"/>'))

    def test_grid_and_node_sizes(self):
        self.assertClean(self.inject_svg('<rect x="4" y="4" width="160" height="64" rx="4" fill="#faf9f5" stroke="#141413"/>'))
        for attrs in ('x="4.5" y="4" width="160" height="64"', 'x="4" y="4" width="200" height="64"',
                      'x="4" y="4" width="160" height="128"', 'x="4" y="4" width="NaN" height="64"'):
            with self.subTest(attrs):
                self.assertRejected(self.inject_svg(f'<rect {attrs} rx="4" fill="#faf9f5" stroke="#141413"/>'))
        self.assertRejected(self.inject_svg('<rect data-node="true" x="4" y="4" width="200" height="64" fill="#faf9f5"/>'), "node dimensions")
        self.assertRejected(self.inject_svg('<path d="M1.5 0 H40" stroke="#141413" fill="none"/>'), "grid")

    def test_attribute_order_quotes_and_case_do_not_change_rules(self):
        self.assertClean(self.inject_svg("<rect HEIGHT='64' fill='#FAF9F5' width='160' y='4' x='4' rx='4' stroke='#141413'/>"))
        self.assertRejected(self.inject_svg("<path stroke-width='1.5' stroke='#78c2c4' fill='none' d='M0 0 H40'/>"), "wash strokes")
        self.assertRejected(self.inject_svg("<rect width='160' height='64' y='4' x='4' rx='12' fill='#faf9f5'/>"), "radius")

    def test_accessibility_and_budgets(self):
        self.assertRejected(re.sub(r"<desc>.*?</desc>", "", self.page, flags=re.S), "<desc>")
        self.assertRejected(re.sub(r"<title>.*?</title>", "", self.page, count=2, flags=re.S), "<title>")
        self.assertRejected(self.inject_svg('<rect x="4" y="4" width="160" height="64" fill="#c47a78"/>'), "accent hue")
        self.assertRejected(self.inject_svg('<rect x="4" y="4" width="160" height="64" fill="#78c2c4"/>' * 2), "focus nodes")
        self.assertRejected(self.inject_svg('<circle r="12" fill="#267072" cx="24" cy="24"/>' * 7), "sequence dots")

    def test_modes_keep_mapping_boundaries_sources_and_matching_toc(self):
        for mode in ("kid", "standard", "deep"):
            with self.subTest(mode):
                page = render(self.data, mode)
                self.assertClean(page)
                nodes = list(parse_html(page).root.walk())
                ids = {n.attrs.get("id") for n in nodes}
                self.assertTrue({"p1", "p2", "p4", "sources", "takeaway"} <= ids)
                self.assertEqual("p3" in ids, mode != "kid")
                self.assertEqual(any(n.tag == "details" for n in nodes), mode == "deep")
                self.assertEqual("N ≈ L" in page, mode == "deep")

    def test_plain_fields_are_escaped_once_and_placeholders_stay_literal(self):
        data = copy.deepcopy(self.data)
        value = '<img src="x" onerror="alert(1)"> & {{title}}'
        data["title"] = value
        data["essence"] = value
        data["steps"][0]["text"] = value
        data["sources"][0]["title"] = value
        page = render(data)
        self.assertClean(page)
        self.assertIn(escape(value), page)
        self.assertFalse(any(n.tag == "img" for n in parse_html(page).root.walk()))

    def test_language_and_custom_labels(self):
        data = copy.deepcopy(self.data)
        data["lang"] = "en"
        self.assertClean(render(data))
        self.assertIn('aria-label="Contents"', render(data))
        self.assertIn("Why this seems plausible: ", render(data))
        data["lang"] = "ja"
        with self.assertRaises(ValueError):
            render(data)
        data["labels"] = {key: "翻訳" for key in LABELS["en"]}
        self.assertClean(render(data))

    def test_documented_svg_snippets_obey_the_contract(self):
        reference = (ROOT / "references/output-template.md").read_text(encoding="utf-8")
        snippets = re.findall(r"```html\n(.*?)\n```", reference, re.S)
        self.assertGreater(len(snippets), 8)
        for i, snippet in enumerate(snippets):
            with self.subTest(i):
                svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 400"><title>Snippet</title><desc>Reference geometry</desc>' + snippet + '</svg>'
                result = Result()
                nodes = list(parse_html(svg, result).root.walk())
                check_svgs(nodes, {}, result)
                self.assertTrue(result.ok, result.errors + result.warnings)

    def test_repeat_validation_has_no_global_findings(self):
        self.assertRejected(self.inject('<script>alert(1)</script>'))
        self.assertClean(self.page)
        self.assertClean(self.page)

    def test_installed_skill_works_from_unrelated_directory_with_spaces(self):
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder)
            skill = base / "installed skill"
            workspace = base / "project with spaces"
            workspace.mkdir()
            shutil.copytree(ROOT / "scripts", skill / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
            shutil.copytree(ROOT / "assets", skill / "assets")
            source = workspace / "topic.json"
            source.write_text(json.dumps(self.data), encoding="utf-8")
            output = workspace / "topic.html"
            built = subprocess.run([sys.executable, str(skill / "scripts/build.py"), "topic.json", "-o", "topic.html"], cwd=workspace, capture_output=True, text=True)
            self.assertEqual(built.returncode, 0, built.stdout + built.stderr)
            checked = subprocess.run([sys.executable, str(skill / "scripts/check.py"), str(output)], cwd=base, capture_output=True, text=True)
            self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)

    def test_failed_build_preserves_output_and_reports_usage_errors(self):
        with tempfile.TemporaryDirectory() as folder:
            source, output = Path(folder) / "input.json", Path(folder) / "output.html"
            data = copy.deepcopy(self.data)
            data["mechanism_html"] += '<script>alert(1)</script>'
            source.write_text(json.dumps(data), encoding="utf-8")
            output.write_text("previous page", encoding="utf-8")
            command = [sys.executable, str(ROOT / "scripts/build.py"), str(source), "-o", str(output)]
            run = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(run.returncode, 1, run.stdout + run.stderr)
            self.assertEqual(output.read_text(), "previous page")
            for invalid in ('{"title":', '{"title":"a","title":"b"}', '[]'):
                source.write_text(invalid, encoding="utf-8")
                run = subprocess.run(command, capture_output=True, text=True)
                self.assertEqual(run.returncode, 2, run.stdout + run.stderr)
                self.assertNotIn("Traceback", run.stderr)
            self.assertEqual(output.read_text(), "previous page")

    def test_warnings_fail_cli_and_unreadable_files_are_usage_errors(self):
        page = self.page.replace('class="step-num">01', 'class="step-num">1', 1)
        result = validate(page)
        self.assertFalse(result.errors)
        self.assertTrue(result.warnings)
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "warning.html"
            path.write_text(page, encoding="utf-8")
            run = subprocess.run([sys.executable, str(ROOT / "scripts/check.py"), str(path)], capture_output=True, text=True)
            self.assertEqual(run.returncode, 1)
            path.unlink()
            run = subprocess.run([sys.executable, str(ROOT / "scripts/check.py"), str(path)], capture_output=True, text=True)
            self.assertEqual(run.returncode, 2)
            self.assertNotIn("Traceback", run.stderr)


if __name__ == "__main__":
    unittest.main()
