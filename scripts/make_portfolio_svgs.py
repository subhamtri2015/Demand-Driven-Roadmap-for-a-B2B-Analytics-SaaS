import csv
from pathlib import Path


ASSETS = Path("assets")
ASSETS.mkdir(exist_ok=True)
INK = "#1d2b34"
TEAL = "#167d78"
MINT = "#d9efeb"
AMBER = "#f5e3bd"
GREY = "#e6eaed"
RED = "#c45c35"


def wrap_svg(title, desc, width, height, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{title}</title><desc id="desc">{desc}</desc>
<rect width="100%" height="100%" fill="#ffffff"/>
<style>text{{font-family:Inter,-apple-system,"Segoe UI",Arial,sans-serif;fill:{INK}}}.small{{font-size:13px}}.body{{font-size:15px}}.heading{{font-size:19px;font-weight:700}}.tag{{font-size:12px;font-weight:700}}</style>
{body}</svg>'''


def save(filename, svg):
    (ASSETS / filename).write_text(svg)


def read_csv(path):
    with open(path, newline="") as source:
        return list(csv.DictReader(source))


scores = read_csv("data/processed/rice_scores.csv")
name_map = {
    "A": "SDK theming with CSS variables",
    "B": "Warehouse connector gaps",
    "C": "Granular permissions",
    "D": "Dashboard filters",
    "E": "Remote sync branches",
}
colors = [TEAL, "#478f8b", "#79a9a4", "#c79845", "#a8b4ba"]

bar_rows = []
for index, row in enumerate(scores):
    y = 112 + index * 64
    value = float(row["score"])
    bar_width = value * 8
    sensitivity = ""
    if row["initiative"] == "A":
        alternate = float(row["reach"]) * float(row["impact"]) * float(row["confidence"]) / 3
        sensitivity = f'<line x1="{390+min(value, alternate)*8}" y1="{y+25}" x2="{390+max(value, alternate)*8}" y2="{y+25}" stroke="{RED}" stroke-width="5"/><text x="{390+alternate*8}" y="{y+47}" class="small">effort 3</text>'
    elif row["initiative"] == "C":
        alternate = float(row["reach"]) * float(row["impact"]) * 0.70 / float(row["effort"])
        sensitivity = f'<line x1="{390+min(value, alternate)*8}" y1="{y+25}" x2="{390+max(value, alternate)*8}" y2="{y+25}" stroke="{RED}" stroke-width="5"/><text x="{390+alternate*8}" y="{y+47}" class="small">confidence 70%</text>'
    bar_rows.append(
        f'<text x="26" y="{y+18}" class="body">{row["initiative"]}  {name_map[row["initiative"]]}</text>'
        f'<line x1="390" y1="{y+12}" x2="{390+bar_width}" y2="{y+12}" stroke="{colors[index]}" stroke-width="14" stroke-linecap="square"/>'
        + sensitivity
        + f'<text x="{400+bar_width}" y="{y+18}" class="body">{value:.2f}</text>'
    )
body = (
    '<text x="26" y="42" class="heading">RICE score and assumption sensitivity</text>'
    '<text x="26" y="67" class="small">Base scores from processed reach; impact, confidence, effort are assumptions.</text>'
    + "".join(bar_rows)
    + '<text x="26" y="445" class="small">A effort 3: '
    + f'{float(scores[0]["reach"])*float(scores[0]["impact"])*float(scores[0]["confidence"])/3:.2f}'
    + ' | C confidence 70%: '
    + f'{float(scores[2]["reach"])*float(scores[2]["impact"])*0.7/float(scores[2]["effort"]):.2f}'
    + '</text><rect x="800" y="25" width="170" height="26" rx="3" fill="'
    + AMBER
    + '"/><text x="815" y="43" class="tag">Assumptions</text>'
)
save("rice-scores.svg", wrap_svg("RICE scores with sensitivity cases", "Ranks public issue reach proxies multiplied by assumed impact, confidence, and effort; text shows two changed-assumption scenarios.", 990, 480, body))

roadmap_cards = [
    ("Now", "A  SDK theme discovery", "Metric: publish rate*"),
    ("Next", "C  Permission discovery", "Metric: admin discovery*"),
    ("Next", "B  Connector validation", "Metric: use-case fit*"),
    ("Later", "D / E  Reassess", "Metric: workflow success*"),
]
roadmap_body = '<text x="30" y="42" class="heading">Proposed sequence</text><rect x="850" y="18" width="120" height="26" rx="3" fill="' + AMBER + '"/><text x="868" y="36" class="tag">Assumptions</text>'
for index, (horizon, title, metric) in enumerate(roadmap_cards):
    x = 28 + index * 244
    color = TEAL if horizon == "Now" else ("#d8a54d" if horizon == "Next" else "#8799a2")
    roadmap_body += (
        f'<rect x="{x}" y="78" width="220" height="195" rx="4" fill="#ffffff" stroke="{color}" stroke-width="2"/>'
        f'<rect x="{x}" y="78" width="220" height="38" fill="{color}"/>'
        f'<text x="{x+14}" y="103" fill="#ffffff" style="fill:#ffffff" class="body">{horizon}</text>'
        f'<text x="{x+14}" y="150" class="body">{title}</text>'
        f'<text x="{x+14}" y="204" class="small">{metric}</text>'
    )
save("roadmap.svg", wrap_svg("Assumption-based roadmap", "Now, Next, Later proposed order with success metrics identified as assumptions.", 1010, 310, roadmap_body))

matrix_rows = [
    ("Embed theming mechanism", ("D", "IReportTheme\nembed config"), ("D", "Tokens\n(Ant v5)"), ("P", "Issue #59237\nrequest only"), ("D", "Admin themes\n+ Embed SDK"), ("P", "Embed API v3\n(theme not found)")),
    ("CSS-variable theming", ("N", "Not found in\nread docs"), ("N", "Not found for\nembeds"), ("P", "Public request\nonly"), ("N", "Not found in\nread docs"), ("N", "Not found in\nread docs")),
    ("Runtime theme change", ("D", "applyTheme /\nresetTheme"), ("P", "SDK theme passing\n(vendor blog)"), ("U", "Not researched"), ("D", "theme + _theme\nURL arguments"), ("P", "Workbook params\nchange at runtime")),
    ("Per-dashboard/report theme", ("D", "Per-report\ntheme JSON"), ("D", "Per-dashboard\nthemes"), ("U", "Not researched"), ("D", "Dashboard / Explore;\nnot embedded Looks"), ("P", "Per-view theme not\nfound in docs")),
    ("Theme management API", ("U", "Not researched"), ("D", "Theme UI + REST\nPOST /api/v1/theme"), ("U", "Not researched"), ("D", "Themes admin UI;\nTheme API schema"), ("U", "Not found in\nread docs")),
    ("Theme precedence", ("N", "Not found in\nread docs"), ("P", "PR #40763; fix\nstatus unverified"), ("U", "Not researched"), ("D", "Default > theme >\n_theme"), ("U", "Not found in\nread docs")),
]
cols = ["Power BI", "Superset", "Metabase SDK", "Looker", "Tableau"]
matrix_body = '<text x="24" y="40" class="heading">Competitor embedding and theme evidence</text>'
matrix_body += '<text x="24" y="66" class="small">Green = documented; amber = partial or public request; grey = not found in reviewed docs; dashed = not researched.</text>'
matrix_body += '<text x="20" y="121" class="small">Capability</text>'
label_width = 255
column_start = 280
column_width = 174
for j, col in enumerate(cols):
    x = column_start + j * column_width
    label = col.replace(" ", "\n") if col == "Metabase SDK" else col
    if col == "Metabase SDK":
        matrix_body += f'<text x="{x+78}" y="103" class="small" text-anchor="middle">Metabase</text><text x="{x+78}" y="120" class="small" text-anchor="middle">SDK</text>'
    else:
        matrix_body += f'<text x="{x+78}" y="112" class="small" text-anchor="middle">{col}</text>'
status_style = {"D": (TEAL, ""), "P": (AMBER, ""), "N": (GREY, ""), "U": ("#ffffff", ' stroke-dasharray="4 3"')}
for i, (label, *cells) in enumerate(matrix_rows):
    y = 136 + i * 62
    matrix_body += f'<text x="20" y="{y+28}" class="small">{label}</text>'
    for j, (status, text) in enumerate(cells):
        x = column_start + j * column_width
        fill, dash = status_style[status]
        matrix_body += f'<rect x="{x}" y="{y}" width="164" height="54" rx="2" fill="{fill}" stroke="#9aa7ad"{dash}/>'
        lines = text.split("\n")
        text_y = y + (27 - (len(lines)-1) * 7)
        matrix_body += f'<text x="{x+6}" y="{text_y}" class="cell">'
        matrix_body += "".join(f'<tspan x="{x+6}" dy="{0 if line_index == 0 else 14}">{line_text}</tspan>' for line_index, line_text in enumerate(lines))
        matrix_body += '</text>'
save("competitor-matrix.svg", wrap_svg("Competitor embedding and theme evidence matrix", "Official documentation findings for Power BI Embedded, Apache Superset, public Metabase requests, Looker, and Tableau. Evidence states distinguish documented, partial, not found in docs read, and not researched.", 1180, 520, matrix_body).replace(".small{font-size:13px}", ".small{font-size:12px}.cell{font-size:11px}"))

journey = [
    ("Evaluate", "Compare product fit"),
    ("Integrate", "Configure embed"),
    ("Brand / Theme", "Map design tokens"),
    ("Launch", "Preview / publish"),
    ("Operate", "Monitor / update"),
]
journey_body = '<text x="30" y="42" class="heading">Hypothetical embed developer journey</text><rect x="815" y="18" width="145" height="26" rx="3" fill="' + AMBER + '"/><text x="835" y="36" class="tag">Hypothesis</text>'
for i, (stage, detail) in enumerate(journey):
    x = 24 + i * 194
    journey_body += f'<rect x="{x}" y="98" width="174" height="126" rx="4" fill="#f4f7f8" stroke="#8d9da4"/>'
    journey_body += f'<text x="{x+12}" y="134" class="body">{stage}</text><text x="{x+12}" y="174" class="small">{detail}</text>'
    if i < len(journey)-1:
        journey_body += f'<path d="M{x+174} 161h14m-5 -5 5 5-5 5" fill="none" stroke="{TEAL}" stroke-width="2"/>'
save("embed-journey.svg", wrap_svg("Hypothetical embed developer journey", "Evaluate, integrate, brand/theme, launch, operate. Every stage is a hypothesis pending interviews.", 1000, 260, journey_body))

glance = ["Problem", "Users", "Goals", "Scope", "Metrics", "Risks"]
glance_body = '<text x="30" y="42" class="heading">PRD at a glance</text><rect x="780" y="18" width="170" height="26" rx="3" fill="' + AMBER + '"/><text x="798" y="36" class="tag">Proposed design</text>'
for i, label in enumerate(glance):
    x = 28 + (i % 3) * 320
    y = 80 + (i // 3) * 118
    glance_body += f'<rect x="{x}" y="{y}" width="286" height="84" rx="4" fill="#f4f7f8" stroke="#aab6bb"/><text x="{x+16}" y="{y+34}" class="heading">{label}</text><text x="{x+16}" y="{y+61}" class="small">See draft PRD section</text>'
save("prd-at-a-glance.svg", wrap_svg("PRD at a glance", "Proposed PRD summary categories: problem, users, goals, scope, metrics, and risks.", 1000, 330, glance_body))

def wireframe(filename, title, mode):
    body = f'<text x="24" y="36" class="heading">{title}</text><rect x="750" y="15" width="220" height="26" rx="3" fill="{AMBER}"/><text x="770" y="33" class="tag">Wireframe - proposed design</text>'
    body += '<rect x="30" y="62" width="930" height="470" fill="#f7f7f7" stroke="#69757a"/><rect x="30" y="62" width="930" height="52" fill="#e5e5e5" stroke="#69757a"/><text x="52" y="94" class="body">Embedded analytics theme</text>'
    if mode == "config":
        body += '<rect x="58" y="140" width="400" height="350" fill="#ffffff" stroke="#929292"/><text x="82" y="174" class="body">Theme variables</text><text x="82" y="220" class="small">Brand primary</text><rect x="240" y="198" width="180" height="34" fill="#f0f0f0" stroke="#777"/><text x="82" y="275" class="small">Surface</text><rect x="240" y="253" width="180" height="34" fill="#f0f0f0" stroke="#777"/><text x="82" y="330" class="small">Font family</text><rect x="240" y="308" width="180" height="34" fill="#f0f0f0" stroke="#777"/><text x="82" y="385" class="small">Font size</text><rect x="240" y="363" width="180" height="34" fill="#f0f0f0" stroke="#777"/><rect x="620" y="420" width="140" height="42" fill="#dedede" stroke="#777"/><text x="660" y="447" class="small">Preview</text>'
    elif mode == "preview":
        body += '<rect x="58" y="140" width="240" height="350" fill="#ffffff" stroke="#929292"/><text x="82" y="174" class="body">Draft settings</text><rect x="82" y="200" width="190" height="24" fill="#e5e5e5"/><rect x="82" y="242" width="190" height="24" fill="#e5e5e5"/><rect x="82" y="284" width="190" height="24" fill="#e5e5e5"/><rect x="330" y="140" width="590" height="350" fill="#ffffff" stroke="#929292"/><text x="356" y="174" class="body">Preview</text><rect x="356" y="195" width="520" height="64" fill="#e9e9e9"/><rect x="356" y="280" width="250" height="120" fill="#f1f1f1" stroke="#bbb"/><rect x="626" y="280" width="250" height="120" fill="#f1f1f1" stroke="#bbb"/><text x="356" y="448" class="small">Validation and error state area</text>'
    else:
        body += '<rect x="180" y="145" width="620" height="320" fill="#ffffff" stroke="#929292"/><text x="218" y="190" class="heading">Publish theme?</text><text x="218" y="236" class="body">Review changes and intended workspace</text><rect x="218" y="265" width="520" height="82" fill="#f1f1f1" stroke="#bbb"/><text x="238" y="300" class="small">Summary of variables and validation state</text><rect x="490" y="385" width="100" height="40" fill="#e1e1e1" stroke="#777"/><text x="518" y="411" class="small">Cancel</text><rect x="620" y="385" width="118" height="40" fill="#d4d4d4" stroke="#777"/><text x="644" y="411" class="small">Publish</text>'
    save(filename, wrap_svg(title, "Low-fidelity grayscale wireframe; proposed design, not a product screenshot.", 1000, 560, body))


wireframe("wireframe-theming-1-config.svg", "Theme configuration", "config")
wireframe("wireframe-theming-2-preview.svg", "Theme preview", "preview")
wireframe("wireframe-theming-3-publish.svg", "Theme publish", "publish")