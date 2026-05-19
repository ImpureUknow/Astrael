from __future__ import annotations

import base64
from pathlib import Path


ROOT = Path(__file__).parent
SITE = ROOT / "site"
OUTPUT = ROOT / "astrael-reader-standalone.html"


def main() -> None:
    html = (SITE / "index.html").read_text(encoding="utf-8")
    css = (SITE / "styles.css").read_text(encoding="utf-8")
    chapters = (SITE / "chapters.js").read_text(encoding="utf-8")
    app = (SITE / "app.js").read_text(encoding="utf-8")
    map_b64 = base64.b64encode((SITE / "assets" / "aresia-continent-map-v3.png").read_bytes()).decode("ascii")

    html = html.replace('<link rel="stylesheet" href="./styles.css" />', f"<style>\n{css}\n</style>")
    html = html.replace(
        '<script src="./chapters.js"></script>',
        f'<script>\nwindow.ASTRAEL_INLINE_MAP = "data:image/png;base64,{map_b64}";\n{chapters}\n</script>',
    )
    html = html.replace('<script src="./app.js"></script>', f"<script>\n{app}\n</script>")
    OUTPUT.write_text(html, encoding="utf-8")
    print(OUTPUT)


if __name__ == "__main__":
    main()
