import csv
import hashlib
import json
import os
import time
from collections import OrderedDict
from urllib.parse import urlencode
from urllib.request import Request, urlopen


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
OUT = os.path.join(DOCS, "related_work_matrix.csv")
STATE = os.path.join(DOCS, "sweep_state.json")


QUERIES = [
    "robot fault containment hierarchy",
    "hierarchical fault tolerance robotics",
    "fault containment control robot",
    "runtime assurance robotics fault",
    "robot safety shield hierarchy",
    "modular robot failure propagation",
    "distributed fault isolation robot systems",
    "resilient robot control hierarchy",
    "cascade failure containment engineering",
    "subsumption architecture robot failure",
    "robot recovery behavior fault",
    "robotics resilient system architecture",
    "robot fault diagnosis and recovery",
    "hierarchical control fault tolerance",
    "safe robot execution monitor",
    "robotic system reliability architecture",
]


def fetch_crossref(query, rows=100, cursor="*"):
    base = "https://api.crossref.org/works"
    params = {
        "query": query,
        "rows": rows,
        "cursor": cursor,
        "select": "DOI,title,author,container-title,created,type,abstract",
    }
    url = base + "?" + urlencode(params)
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8", errors="replace"))


def load_state():
    if os.path.exists(STATE):
        with open(STATE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"done": {}, "rows": []}


def save_state(state):
    os.makedirs(DOCS, exist_ok=True)
    with open(STATE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def norm_text(x):
    if not x:
        return ""
    return " ".join(str(x).replace("\n", " ").split())


def make_key(doi, title):
    basis = (doi or "") + "|" + norm_text(title).lower()
    return hashlib.sha1(basis.encode("utf-8", errors="ignore")).hexdigest()


def extract_items(msg):
    items = msg.get("items", [])
    return items, msg.get("next-cursor")


def main():
    state = load_state()
    done = state["done"]
    rows = state["rows"]
    seen = {row["key"] for row in rows}
    target = 1100
    for qi, query in enumerate(QUERIES):
        if done.get(query):
            continue
        cursor = "*"
        page = 0
        while True:
            try:
                payload = fetch_crossref(query, rows=100, cursor=cursor)
            except Exception as e:
                state["last_error"] = {"query": query, "error": repr(e), "page": page}
                save_state(state)
                break
            msg = payload.get("message", {})
            items, next_cursor = extract_items(msg)
            if not items:
                break
            for item in items:
                title = (item.get("title") or [""])[0]
                doi = item.get("DOI", "")
                key = make_key(doi, title)
                if key in seen:
                    continue
                authors = item.get("author") or []
                author0 = ""
                if authors:
                    a = authors[0]
                    author0 = " ".join([a.get("given", ""), a.get("family", "")]).strip()
                rows.append({
                    "key": key,
                    "query": query,
                    "title": norm_text(title),
                    "doi": doi,
                    "venue": norm_text((item.get("container-title") or [""])[0]),
                    "year": str((item.get("created", {}).get("date-parts", [[None]])[0][0]) or ""),
                    "type": item.get("type", ""),
                    "author0": author0,
                    "source": "crossref",
                    "problem_claimed": "",
                    "mechanism": "",
                    "hidden_assumptions": "",
                    "fixed_variables": "",
                    "ignored_failures": "",
                    "novelty_pressure": "",
                    "open_questions": "",
                })
                seen.add(key)
            save_state({"done": done, "rows": rows, "last_error": state.get("last_error")})
            if len(rows) >= target:
                break
            if not next_cursor or next_cursor == cursor:
                break
            cursor = next_cursor
            page += 1
            time.sleep(0.2)
        done[query] = True
        save_state({"done": done, "rows": rows, "last_error": state.get("last_error")})
        if len(rows) >= target:
            break

    # enrich later in separate passes
    fieldnames = [
        "key", "query", "title", "doi", "venue", "year", "type", "author0", "source",
        "problem_claimed", "mechanism", "hidden_assumptions", "fixed_variables",
        "ignored_failures", "novelty_pressure", "open_questions",
    ]
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {OUT}")


if __name__ == "__main__":
    main()
