# tekee content/ kansion markdown tiedostoista html sivut
# ajetaan dockerfilessä
#
# tiedoston alkuun:
# ---
# title: Otsikko
# order: 10
# topic: aihe
# description: lyhyt kuvaus etusivun korttiin
# nav: no            (jos sivua ei haluta valikkoon)
# ---

import json
import re
import shutil
import sys
from pathlib import Path

import markdown

ROOT = Path(__file__).parent
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "dist"
template = (ROOT / "templates" / "page.html").read_text(encoding="utf-8")

pages = []
for f in (ROOT / "content").glob("*.md"):
    text = f.read_text(encoding="utf-8")
    meta = {}
    if text.startswith("---"):
        _, header, text = text.split("---", 2)
        for line in header.strip().splitlines():
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip()

    if f.stem.endswith("index"):
        name = "index"
    else:
        name = f.stem.split("-", 1)[1]  # 10-kontit -> kontit

    html = markdown.markdown(text, extensions=["fenced_code", "tables"])
    # taulukot diviin niin reunat ja scrollaus toimii
    html = html.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")

    pages.append({
        "name": name,
        "title": meta.get("title", name),
        "order": int(meta.get("order", 99)),
        "topic": meta.get("topic", ""),
        "description": meta.get("description", ""),
        "nav": meta.get("nav", "yes") != "no",
        "html": html,
        # komentojen määrä = taulukon rivit jotka alkaa docker-komennolla tai dockerfile-ohjeella
        "commands": len(re.findall(r"<tr>\n<td><code>(docker |(FROM|WORKDIR|COPY|RUN|ENV|EXPOSE|USER|HEALTHCHECK|CMD|ENTRYPOINT) )", html)),
    })

pages.sort(key=lambda x: x["order"])
nav_pages = [p for p in pages if p["nav"]]


def link(p):
    return "/" if p["name"] == "index" else "/" + p["name"] + ".html"


# etusivun kortit
cards = '<div class="cards">\n'
for p in nav_pages:
    if p["name"] == "index" or not p["description"]:
        continue
    count = f'<span class="count">{p["commands"]} komentoa</span>' if p["commands"] else ""
    cards += (
        f'<a class="card" href="{link(p)}">'
        f'<span class="card-title">{p["title"]}</span>'
        f'<span class="card-desc">{p["description"]}</span>{count}</a>\n'
    )
cards += "</div>"

command_pages = [p for p in pages if p["name"] != "index" and p["commands"]]
total = sum(p["commands"] for p in command_pages)

# sivujen nimet javascriptille (lisäysten linkit)
titles = {p["topic"]: {"title": p["title"], "url": link(p)} for p in pages if p["topic"] and p["topic"] != "*"}

if OUT.exists():
    shutil.rmtree(OUT)
shutil.copytree(ROOT / "static", OUT / "static")

for page in pages:
    nav = ""
    for p in nav_pages:
        active = ' class="active"' if p is page else ""
        nav += f'<li><a href="{link(p)}"{active}>{p["title"]}</a></li>\n'

    content = page["html"].replace("<!-- cards -->", cards)
    content = content.replace("{{total}}", str(total)).replace("{{topics}}", str(len(command_pages)))

    html = template.replace("{{title}}", page["title"])
    html = html.replace("{{nav}}", nav)
    html = html.replace("{{topic}}", page["topic"])
    html = html.replace("{{pages}}", json.dumps(titles, ensure_ascii=False))
    html = html.replace("{{content}}", content)

    (OUT / (page["name"] + ".html")).write_text(html, encoding="utf-8")
    print("tehty", page["name"], page["commands"], "komentoa")
