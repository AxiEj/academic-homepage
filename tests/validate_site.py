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

    required_ids = {"about", "news", "research", "experience", "publications"}
    missing = required_ids - parser.ids
    assert not missing, f"missing academic sections: {sorted(missing)}"

    body_text = "\n".join(parser.text)
    visible_text = " ".join(parser.text)
    for required in [
        "Jiahao Xie",
        "Dalian Medical University",
        "Computational Chemistry",
        "Bioinformatics",
        "Molecular Dynamics",
        "A note to readers: I am an undergraduate student",
        "if this page has led you to overestimate me, I apologize for the misunderstanding",
        "Email: xjhdl@dmu.edu.cn",
        "GitHub: https://github.com/AxiEj",
        "ORCID",
    ]:
        assert required in visible_text, f"missing academic content: {required}"

    profile_start = html.index('<aside class="profile"')
    profile_end = html.index("</aside>", profile_start)
    profile_html = html[profile_start:profile_end]
    for required in ["Contact", "Email:", "xjhdl@dmu.edu.cn", "GitHub:", "https://github.com/AxiEj", "ORCID:", "0009-0004-2387-7021"]:
        assert required in profile_html, f"left profile contact missing: {required}"

    forbidden = ["Gallery", "Music", "Quiz", "Mother", "Father", "heart failure", "心衰", "心力衰竭"]
    for word in forbidden:
        assert word not in body_text, f"non-academic/personal content leaked: {word}"

    expected_news = "2025.12 Research Intern, University of Pittsburgh, Department of Pharmaceutical Sciences, participating in the MAPLE project."
    assert expected_news in visible_text, f"missing MAPLE project note in news: {expected_news}"

    required_markup = [
        '<button class="language-toggle"',
        'data-language-toggle',
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

    bilingual_requirements = [
        "data-i18n=",
        "const translations =",
        "function applyLanguage",
        "localStorage.setItem(storageKey, current)",
        "<strong>A note to readers:</strong>",
        "<strong>写给读者：</strong>",
        "同行评议原创研究论文",
        "通信 / 评论 / 综述",
        "负责机制图绘制和稿件返修",
    ]
    for snippet in bilingual_requirements:
        assert snippet in html, f"missing bilingual language-toggle support: {snippet}"
    assert "position: fixed" in css and ".language-toggle" in css, "language toggle should be fixed in the top-right corner"

    publications = [
        ("Regulation of gut epithelial barrier and tuft/goblet cell responses by microbiome repair: Opportunities and future directions", "10.1073/pnas.2535289123"),
        ("Host–gut microbiota interactions in health and disease: mechanisms and intervention strategies", "10.3389/fmicb.2026.1785607"),
        ("Letter regarding HOXA9 drives lymphatic metastasis by activating the c-MYC-glycolysis-lactate axis in gastric cancer", "10.1186/s12967-026-07822-x"),
        ("Letter to the editor: clinical translation of senolytic immunotherapy: critical considerations for SenoVax™ and beyond", "10.1186/s12967-026-07820-z"),
        ("Mechanism by which porcine transmissible gastroenteritis virus disrupts host innate immunity", "10.3389/fimmu.2025.1675572"),
        ("Combining network pharmacology, machine learning, molecular docking and molecular dynamic to explore the mechanism of Chufeng Qingpi decoction in treating schistosomiasis", "10.3389/fcimb.2024.1453529"),
    ]
    for title, doi in publications:
        assert title in visible_text, f"missing publication title: {title}"
        assert doi in visible_text, f"missing publication DOI: {doi}"
    assert "No public publication list yet" not in visible_text, "placeholder publication text should be removed"

    publication_block_start = html.index('<section id="publications"')
    publication_block_end = html.index("</section>", publication_block_start)
    publication_html = html[publication_block_start:publication_block_end]
    peer_heading = publication_html.index("Peer-reviewed research articles")
    correspondence_heading = publication_html.index("Correspondence / Commentaries / Reviews")
    original_title = "Combining network pharmacology, machine learning, molecular docking and molecular dynamic to explore the mechanism of Chufeng Qingpi decoction in treating schistosomiasis"
    original_position = publication_html.index(original_title)
    assert peer_heading < original_position < correspondence_heading, "original research article must be under Peer-reviewed research articles"
    contribution_note = "Contribution: responsible for the molecular dynamics simulations in this study."
    assert original_position < publication_html.index(contribution_note) < correspondence_heading, "MD simulation contribution note must stay with the original research article"
    for title in [
        "Regulation of gut epithelial barrier and tuft/goblet cell responses by microbiome repair",
        "Host–gut microbiota interactions in health and disease",
        "Letter regarding HOXA9 drives lymphatic metastasis",
        "Letter to the editor: clinical translation of senolytic immunotherapy",
        "Mechanism by which porcine transmissible gastroenteritis virus disrupts host innate immunity",
    ]:
        assert correspondence_heading < publication_html.index(title), f"non-original publication must be in correspondence/review section: {title}"
    review_note = "Contribution: responsible for mechanistic figure preparation and manuscript revision."
    for title in [
        "Host–gut microbiota interactions in health and disease",
        "Mechanism by which porcine transmissible gastroenteritis virus disrupts host innate immunity",
    ]:
        title_position = publication_html.index(title)
        note_position = publication_html.index(review_note, title_position)
        assert title_position < note_position, f"mechanistic figure/revision contribution note must stay with: {title}"
    assert publication_html.count(review_note) == 2, "two review articles should carry the mechanistic figure/revision contribution note"
    assert publication_html.count('<ol class="publication-list">') == 2, "publication categories should use two separate lists"

    for required in [
        "Laboratory Animal Center, Dalian Medical University",
        "大连医科大学实验动物中心",
        "由王栩剑博士指导",
        "由王梓安与张晓陶指导",
        "王亮课题组",
    ]:
        assert required in html, f"missing corrected bilingual experience wording: {required}"

    initial_html = html[:html.index("<script>")]
    assert "大连医科大学实验动物中心)" not in initial_html, "English/default interface should not include Chinese parenthetical for Laboratory Animal Center"
    assert "（Laboratory Animal Center, Dalian Medical University）" not in html, "Chinese interface should not include English parenthetical for Laboratory Animal Center"

    experience_block_start = html.index('<section id="experience"')
    experience_block_end = html.index("</section>", experience_block_start)
    experience_text = " ".join(parser.text)
    expected_experience = [
        "2025-12 - Present Research Intern University of Pittsburgh · Dept. of Pharmaceutical Sciences Supervised by PhD Xujian Wang (Prof. Junmei Wang's Group)",
        "2025-06 - Present Research Assistant Second Affiliated Hospital of Dalian Medical University Feng Zhang Group · Supervised by Zian Wang & Xiaotao Zhang",
        "2023-10 - Present Research Assistant Laboratory Animal Center, Dalian Medical University Liang Wang Group",
    ]
    for snippet in expected_experience:
        assert snippet in experience_text, f"missing exact experience wording: {snippet}"
    forbidden_experience = ["2025.12.24", "Remote", "School of Pharmacy", "under Prof.", "2025.06", "2023.10"]
    experience_html = html[experience_block_start:experience_block_end]
    for word in forbidden_experience:
        assert word not in experience_html, f"stale experience wording remains: {word}"

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
