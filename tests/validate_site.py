from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class SiteParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = []
        self.images = []
        self.text = []
        self._capture = []

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if "id" in data:
            self.ids.add(data["id"])
        if tag == "a" and "href" in data:
            self.links.append(data["href"])
        if tag == "img" and "src" in data:
            self.images.append(data["src"])

    def handle_data(self, data):
        if data.strip():
            self.text.append(data.strip())

def main():
    index = ROOT / "index.html"
    assert index.exists(), "index.html must exist at standalone site root"
    html = index.read_text(encoding="utf-8")
    parser = SiteParser()
    parser.feed(html)

    required_ids = {"about", "news", "research", "experience", "publications", "contact"}
    missing = required_ids - parser.ids
    assert not missing, f"missing academic sections: {sorted(missing)}"

    body_text = "\n".join(parser.text)
    for required in [
        "Jiahao Xie",
        "Dalian Medical University",
        "Computational Chemistry",
        "Bioinformatics",
        "Molecular Dynamics",
        "ORCID",
    ]:
        assert required in body_text, f"missing academic content: {required}"

    forbidden = ["Gallery", "Music", "Quiz", "Mother", "Father", "heart failure", "心衰", "心力衰竭"]
    for word in forbidden:
        assert word not in body_text, f"non-academic/personal content leaked: {word}"

    required_markup = [
        '<main class="page"',
        '<aside class="profile"',
        '<article class="content"',
        '<ul class="compact-list news-list">',
        '<ol class="publication-list">',
    ]
    for snippet in required_markup:
        assert snippet in html, f"missing plain academic homepage markup: {snippet}"

    marketing_classes = ["hero", "card-grid", "card", "project-item", "quick-links", "section-intro"]
    for class_name in marketing_classes:
        assert f'class="{class_name}' not in html, f"marketing-style class remains: {class_name}"

    css = (ROOT / "style.css").read_text(encoding="utf-8")
    required_css = [
        "background: #fff",
        "max-width: 1000px",
        "font-family: Arial, Helvetica, sans-serif",
        "color: #1772d0",
    ]
    for snippet in required_css:
        assert snippet in css, f"missing reference-like academic CSS: {snippet}"
    for forbidden_css in ["box-shadow", "border-radius: 24px", "linear-gradient", "backdrop-filter"]:
        assert forbidden_css not in css, f"landing-page styling remains: {forbidden_css}"

    for href in parser.links:
        if href.startswith(("http://", "https://", "mailto:", "#")):
            continue
        assert (ROOT / href).exists(), f"broken local link: {href}"

    for src in parser.images:
        assert (ROOT / src).exists(), f"missing image asset: {src}"

    assert (ROOT / ".nojekyll").exists(), ".nojekyll should exist for GitHub Pages static deployment"
    assert (ROOT / "README.md").exists(), "README.md should document deployment"
    print("validated standalone academic site")

if __name__ == "__main__":
    main()
