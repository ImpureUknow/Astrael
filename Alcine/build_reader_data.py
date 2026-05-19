from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).parent
SITE = ROOT / "site"
OUTPUT = SITE / "chapters.js"


def sort_key(path: Path) -> tuple[int, float]:
    match = re.match(r"^(\d+(?:\.\d+)?)\s+-\s+", path.name)
    value = float(match.group(1)) if match else 9999.0
    return (0 if value == 0 else 1, value)


def parse_first_heading(content: str) -> tuple[str, str]:
    match = re.search(r"^##\s+ตอนที่\s+([0-9.]+)\s+—\s+(.+)$", content, re.MULTILINE)
    if not match:
        return ("?", "ไม่มีชื่อ")
    return (match.group(1), match.group(2).strip())


def main() -> None:
    files = sorted(ROOT.glob("*.txt"), key=sort_key)
    chapters = []

    for path in files:
        if path.name == "Story.txt":
            continue
        if not re.match(r"^\d+(?:\.\d+)?\s+-\s+", path.name):
            continue

        content = path.read_text(encoding="utf-8")
        number, title = parse_first_heading(content)
        chapters.append(
            {
                "id": number.replace(".", "-"),
                "number": number,
                "title": title,
                "filename": path.name,
                "content": content,
            }
        )

    payload = "window.ASTRAEL_CHAPTERS = " + json.dumps(chapters, ensure_ascii=False, indent=2) + ";\n"
    OUTPUT.write_text(payload, encoding="utf-8")
    print(f"Wrote {OUTPUT} with {len(chapters)} chapters")


if __name__ == "__main__":
    main()
