from __future__ import annotations

import math
import random
from collections import deque
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont
import numpy as np


ROOT = Path(__file__).parent
SOURCE = ROOT / "MAP.png"
OUT_PNG = ROOT / "aresia-continent-map-v3.png"
OUT_WEBP = ROOT / "aresia-continent-map-v3.webp"

SCALE = 1.38
OFFSET = (520, 180)
CANVAS = (2140, 2300)


def font_path(*names: str) -> str:
    for name in names:
        path = Path(r"C:\Windows\Fonts") / name
        if path.exists():
            return str(path)
    raise FileNotFoundError(names[0])


SERIF = font_path("georgia.ttf", "times.ttf")
SERIF_BOLD = font_path("georgiab.ttf", "timesbd.ttf")
THAI = font_path("tahoma.ttf", "leelawad.ttf")
THAI_BOLD = font_path("tahomabd.ttf", "leelawdb.ttf")


def f(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


COUNTRIES = [
    dict(name="Eryndor Empire", color=(237, 28, 36), fill=(142, 42, 33), symbol="dragon", pos=(575, 421), size="hero"),
    dict(name="Kingdom of Lacoss", color=(63, 72, 204), fill=(41, 77, 145), symbol="lion", pos=(469, 937), size="hero"),
    dict(name="Kingdom of Velmora", color=(0, 162, 232), fill=(28, 124, 157), symbol="scales", pos=(469, 774), size="major"),
    dict(name="Kingdom of Aetherion", color=(112, 146, 190), fill=(83, 102, 122), symbol="tower", pos=(704, 799), size="major"),
    dict(name="Republic of Varelia", color=(202, 234, 102), fill=(71, 118, 64), symbol="anchor", pos=(405, 1322), size="major"),

    dict(name="Rothmere", color=(185, 122, 87), fill=(130, 88, 55), symbol="stag", pos=(314, 597), size="mid"),
    dict(name="Lysenne", color=(161, 251, 142), fill=(89, 132, 75), symbol="lily", pos=(242, 800), size="mid"),
    dict(name="Marrowen", color=(167, 201, 162), fill=(91, 112, 88), symbol="tree", pos=(276, 982), size="small"),

    dict(name="Solvane", color=(249, 255, 177), fill=(167, 128, 47), symbol="sun", pos=(304, 1146), size="mid"),
    dict(name="Rosvaria", color=(255, 192, 217), fill=(145, 78, 99), symbol="rose", pos=(424, 1183), size="mid"),
    dict(name="Caldria", color=(230, 234, 205), fill=(141, 123, 81), symbol="wheat", pos=(540, 1194), size="mid"),
    dict(name="Demeris", color=(234, 217, 218), fill=(121, 96, 98), symbol="shell", pos=(617, 1138), size="small"),
    dict(name="Vardane", color=(201, 71, 94), fill=(118, 47, 53), symbol="spear", pos=(394, 1071), size="tiny"),
    dict(name="Tiravel", color=(115, 201, 181), fill=(52, 118, 111), symbol="wave", pos=(356, 1050), size="tiny"),
    dict(name="Edevane", color=(201, 141, 141), fill=(127, 83, 79), symbol="star", pos=(461, 1064), size="tiny"),
    dict(name="Brannor", color=(117, 83, 83), fill=(91, 61, 47), symbol="anvil", pos=(501, 1071), size="tiny"),
    dict(name="Morvane", color=(117, 78, 117), fill=(88, 59, 87), symbol="crown", pos=(568, 1072), size="tiny"),
    dict(name="Selvarn", color=(3, 0, 234), fill=(37, 63, 138), symbol="falcon", pos=(660, 1030), size="small"),
    dict(name="Verdalis", color=(12, 234, 0), fill=(55, 119, 50), symbol="leaf", pos=(726, 938), size="small"),

    dict(name="Merenhal", color=(34, 177, 76), fill=(47, 106, 61), symbol="oak", pos=(881, 403), size="mid"),
    dict(name="Valessia", color=(234, 54, 128), fill=(140, 59, 91), symbol="bridge", pos=(835, 553), size="small"),
    dict(name="Ravennair", color=(117, 22, 63), fill=(91, 39, 53), symbol="raven", pos=(920, 528), size="small"),
    dict(name="Seravelle", color=(200, 191, 231), fill=(112, 96, 142), symbol="pearl", pos=(857, 722), size="mid"),

    dict(name="Aurell", color=(255, 242, 0), fill=(180, 134, 38), symbol="star", pos=(510, 157), size="mid"),
    dict(name="Dravik", color=(255, 127, 39), fill=(151, 80, 35), symbol="axe", pos=(773, 84), size="tiny"),
    dict(name="Nocthar", color=(29, 46, 46), fill=(53, 59, 59), symbol="moon", pos=(827, 49), size="tiny"),
    dict(name="Galdren", color=(127, 127, 127), fill=(97, 96, 92), symbol="mountain", pos=(830, 96), size="tiny"),
    dict(name="Orvessa", color=(170, 173, 146), fill=(110, 113, 89), symbol="plow", pos=(899, 68), size="tiny"),
    dict(name="Halcyra", color=(201, 164, 195), fill=(130, 99, 125), symbol="chalice", pos=(950, 47), size="tiny"),
    dict(name="Berynth", color=(201, 142, 107), fill=(132, 91, 60), symbol="horn", pos=(960, 92), size="tiny"),
    dict(name="Prythia", color=(201, 128, 196), fill=(131, 82, 129), symbol="spiral", pos=(996, 66), size="tiny"),
]


def sxy(x: float, y: float) -> tuple[int, int]:
    return (int(OFFSET[0] + x * SCALE), int(OFFSET[1] + y * SCALE))


def shield_points(cx: float, cy: float, width: float, height: float) -> list[tuple[float, float]]:
    return [
        (cx - width / 2, cy - height / 2),
        (cx + width / 2, cy - height / 2),
        (cx + width * 0.44, cy - height * 0.05),
        (cx + width * 0.23, cy + height * 0.27),
        (cx, cy + height / 2),
        (cx - width * 0.23, cy + height * 0.27),
        (cx - width * 0.44, cy - height * 0.05),
    ]


def draw_symbol(draw: ImageDraw.ImageDraw, symbol: str, cx: int, cy: int, size: int, accent, dark) -> None:
    width = max(2, size // 10)
    if symbol == "dragon":
        draw.arc((cx - size * .34, cy - size * .30, cx + size * .34, cy + size * .30), 90, 350, fill=dark, width=width)
        draw.polygon([(cx - size * .28, cy + size * .02), (cx - size * .04, cy - size * .30), (cx + size * .04, cy + size * .02)], fill=dark)
        draw.polygon([(cx + size * .08, cy + size * .02), (cx + size * .34, cy - size * .22), (cx + size * .28, cy + size * .12)], fill=dark)
    elif symbol == "lion":
        draw.ellipse((cx - size * .25, cy - size * .08, cx + size * .14, cy + size * .22), fill=accent)
        draw.ellipse((cx + size * .06, cy - size * .30, cx + size * .28, cy - size * .08), fill=accent)
        draw.arc((cx - size * .42, cy - size * .18, cx - size * .10, cy + size * .24), 210, 80, fill=accent, width=width)
    elif symbol == "scales":
        draw.line((cx, cy - size * .30, cx, cy + size * .28), fill=accent, width=width)
        draw.line((cx - size * .34, cy - size * .12, cx + size * .34, cy - size * .12), fill=accent, width=width)
        for sign in (-1, 1):
            bx = cx + sign * size * .24
            draw.arc((bx - size * .14, cy + size * .00, bx + size * .14, cy + size * .18), 0, 180, fill=accent, width=width)
    elif symbol == "tower":
        draw.rectangle((cx - size * .18, cy - size * .24, cx + size * .18, cy + size * .28), outline=accent, width=width)
        for offset in (-.18, 0, .18):
            draw.rectangle((cx + offset * size - size * .05, cy - size * .34, cx + offset * size + size * .05, cy - size * .24), fill=accent)
    elif symbol in {"tree", "oak"}:
        draw.line((cx, cy + size * .28, cx, cy - size * .08), fill=accent, width=width)
        draw.ellipse((cx - size * .30, cy - size * .26, cx + size * .10, cy + size * .04), outline=accent, width=width)
        draw.ellipse((cx - size * .04, cy - size * .22, cx + size * .32, cy + size * .08), outline=accent, width=width)
    elif symbol == "stag":
        draw.ellipse((cx - size * .18, cy - size * .06, cx + size * .12, cy + size * .18), outline=accent, width=width)
        draw.line((cx - size * .08, cy - size * .10, cx - size * .22, cy - size * .28), fill=accent, width=width)
        draw.line((cx + size * .06, cy - size * .10, cx + size * .20, cy - size * .28), fill=accent, width=width)
    elif symbol == "lily":
        draw.polygon([(cx, cy - size * .32), (cx - size * .18, cy + size * .10), (cx, cy + size * .02), (cx + size * .18, cy + size * .10)], fill=accent)
        draw.line((cx, cy + size * .02, cx, cy + size * .28), fill=accent, width=width)
    elif symbol == "sun":
        for angle in range(0, 360, 45):
            a = math.radians(angle)
            draw.line((cx + math.cos(a) * size * .18, cy + math.sin(a) * size * .18, cx + math.cos(a) * size * .34, cy + math.sin(a) * size * .34), fill=accent, width=max(2, width // 2))
        draw.ellipse((cx - size * .14, cy - size * .14, cx + size * .14, cy + size * .14), outline=accent, width=width)
    elif symbol == "rose":
        for angle in range(0, 360, 72):
            a = math.radians(angle)
            ex, ey = cx + math.cos(a) * size * .12, cy + math.sin(a) * size * .12
            draw.ellipse((ex - size * .12, ey - size * .08, ex + size * .12, ey + size * .08), fill=accent)
    elif symbol == "wheat":
        draw.line((cx, cy + size * .28, cx, cy - size * .26), fill=accent, width=width)
        for i in range(4):
            yy = cy + size * .14 - i * size * .11
            draw.line((cx, yy, cx - size * .16, yy - size * .08), fill=accent, width=max(2, width // 2))
            draw.line((cx, yy, cx + size * .16, yy - size * .08), fill=accent, width=max(2, width // 2))
    elif symbol == "shell":
        draw.arc((cx - size * .25, cy - size * .14, cx + size * .25, cy + size * .28), 180, 360, fill=accent, width=width)
        for dx in (-.16, 0, .16):
            draw.line((cx, cy + size * .18, cx + dx * size, cy - size * .02), fill=accent, width=max(2, width // 2))
    elif symbol == "spear":
        draw.line((cx, cy + size * .26, cx, cy - size * .18), fill=accent, width=width)
        draw.polygon([(cx, cy - size * .34), (cx - size * .12, cy - size * .14), (cx + size * .12, cy - size * .14)], fill=accent)
    elif symbol == "wave":
        draw.arc((cx - size * .28, cy - size * .10, cx + size * .02, cy + size * .16), 180, 360, fill=accent, width=width)
        draw.arc((cx - size * .02, cy - size * .10, cx + size * .28, cy + size * .16), 180, 360, fill=accent, width=width)
    elif symbol == "star":
        pts = []
        for i in range(10):
            angle = -math.pi / 2 + i * math.pi / 5
            radius = size * .34 if i % 2 == 0 else size * .15
            pts.append((cx + math.cos(angle) * radius, cy + math.sin(angle) * radius))
        draw.polygon(pts, fill=accent)
    elif symbol == "anvil":
        draw.polygon([(cx - size * .28, cy - size * .02), (cx + size * .24, cy - size * .02), (cx + size * .14, cy + size * .12), (cx - size * .12, cy + size * .12)], fill=accent)
        draw.rectangle((cx - size * .10, cy + size * .12, cx + size * .12, cy + size * .24), fill=accent)
    elif symbol == "crown":
        draw.polygon([(cx - size * .28, cy + size * .18), (cx - size * .20, cy - size * .18), (cx, cy + size * .02), (cx + size * .20, cy - size * .18), (cx + size * .28, cy + size * .18)], fill=accent)
    elif symbol == "falcon":
        draw.polygon([(cx - size * .30, cy + size * .18), (cx - size * .04, cy - size * .18), (cx + size * .30, cy + size * .02), (cx + size * .04, cy - size * .02)], fill=accent)
    elif symbol == "leaf":
        draw.ellipse((cx - size * .26, cy - size * .20, cx + size * .26, cy + size * .20), outline=accent, width=width)
        draw.line((cx - size * .14, cy + size * .18, cx + size * .16, cy - size * .16), fill=accent, width=max(2, width // 2))
    elif symbol == "bridge":
        draw.arc((cx - size * .28, cy - size * .06, cx + size * .28, cy + size * .24), 180, 360, fill=accent, width=width)
        draw.line((cx - size * .24, cy + size * .10, cx + size * .24, cy + size * .10), fill=accent, width=width)
    elif symbol == "raven":
        draw.pieslice((cx - size * .30, cy - size * .18, cx + size * .30, cy + size * .22), 200, 350, fill=dark)
    elif symbol == "pearl":
        draw.ellipse((cx - size * .18, cy - size * .18, cx + size * .18, cy + size * .18), outline=accent, width=width)
    elif symbol == "axe":
        draw.line((cx - size * .18, cy + size * .26, cx + size * .12, cy - size * .24), fill=accent, width=width)
        draw.polygon([(cx + size * .06, cy - size * .24), (cx + size * .28, cy - size * .16), (cx + size * .16, cy + size * .02)], fill=accent)
    elif symbol == "moon":
        draw.ellipse((cx - size * .20, cy - size * .22, cx + size * .20, cy + size * .22), fill=accent)
        draw.ellipse((cx - size * .08, cy - size * .22, cx + size * .22, cy + size * .18), fill=dark)
    elif symbol == "mountain":
        draw.polygon([(cx - size * .28, cy + size * .22), (cx, cy - size * .26), (cx + size * .28, cy + size * .22)], outline=accent)
    elif symbol == "plow":
        draw.line((cx - size * .24, cy + size * .18, cx + size * .18, cy - size * .18), fill=accent, width=width)
        draw.line((cx - size * .10, cy + size * .18, cx + size * .18, cy + size * .18), fill=accent, width=width)
    elif symbol == "chalice":
        draw.arc((cx - size * .20, cy - size * .22, cx + size * .20, cy + size * .12), 0, 180, fill=accent, width=width)
        draw.line((cx, cy + size * .12, cx, cy + size * .26), fill=accent, width=width)
        draw.line((cx - size * .18, cy + size * .26, cx + size * .18, cy + size * .26), fill=accent, width=width)
    elif symbol == "horn":
        draw.arc((cx - size * .26, cy - size * .18, cx + size * .26, cy + size * .22), 210, 30, fill=accent, width=width)
    elif symbol == "spiral":
        for radius in (size * .08, size * .16, size * .24):
            draw.arc((cx - radius, cy - radius, cx + radius, cy + radius), 10, 320, fill=accent, width=max(2, width // 2))
    elif symbol == "anchor":
        draw.line((cx, cy - size * .28, cx, cy + size * .22), fill=accent, width=width)
        draw.ellipse((cx - size * .08, cy - size * .36, cx + size * .08, cy - size * .20), outline=accent, width=width)
        draw.arc((cx - size * .28, cy - size * .02, cx + size * .28, cy + size * .30), 20, 160, fill=accent, width=width)


def draw_shield(draw: ImageDraw.ImageDraw, country: dict, center: tuple[int, int], size: int) -> None:
    accent = (224, 190, 118, 255)
    dark = (26, 20, 16, 255)
    cx, cy = center
    points = shield_points(cx, cy, size, size * 1.18)
    draw.polygon([(x + 4, y + 5) for x, y in points], fill=(0, 0, 0, 90))
    draw.polygon(points, fill=(28, 23, 20, 255))
    inner = shield_points(cx, cy, size * .84, size * .84 * 1.18)
    draw.polygon(inner, fill=country["fill"] + (255,))
    draw.line(inner + [inner[0]], fill=accent, width=max(2, size // 16))
    symbol_dark = dark if country["symbol"] in {"dragon", "raven", "moon"} else accent
    draw_symbol(draw, country["symbol"], cx, cy + int(size * .04), int(size * .56), accent, symbol_dark)


def textured_fill(base_color: tuple[int, int, int], size: tuple[int, int], seed: int) -> Image.Image:
    rng = np.random.default_rng(seed)
    noise = rng.integers(-12, 13, size=(size[1], size[0], 1), dtype=np.int16)
    base = np.array(base_color, dtype=np.int16).reshape(1, 1, 3)
    pixels = np.clip(base + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(pixels, mode="RGB")


def fill_holes(mask: Image.Image) -> Image.Image:
    inverse = ImageChops.invert(mask)
    flood = inverse.copy()
    ImageDraw.floodfill(flood, (0, 0), 0)
    holes = flood.point(lambda p: 255 if p else 0)
    return ImageChops.lighter(mask, holes)


def flood_region_mask(passable: np.ndarray, seed: tuple[int, int]) -> Image.Image:
    height, width = passable.shape
    sx, sy = seed
    seen = np.zeros_like(passable, dtype=np.uint8)
    queue = deque([(sx, sy)])
    seen[sy, sx] = 1
    while queue:
        x, y = queue.popleft()
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < width and 0 <= ny < height and not seen[ny, nx] and passable[ny, nx]:
                seen[ny, nx] = 1
                queue.append((nx, ny))
    return Image.fromarray(seen * 255, mode="L")


def text(draw: ImageDraw.ImageDraw, xy, value: str, font, anchor="mm", fill=(245, 232, 205, 255), stroke=2):
    draw.text(xy, value, font=font, anchor=anchor, fill=fill, stroke_width=stroke, stroke_fill=(26, 20, 16, 220))


def main() -> None:
    source = Image.open(SOURCE).convert("RGB")
    source_array = np.array(source)
    near_white = np.all(source_array > 245, axis=2)
    near_black = np.all(source_array < 35, axis=2)
    passable = ~(near_white | near_black)
    scaled_size = (int(source.width * SCALE), int(source.height * SCALE))

    ocean = textured_fill((20, 48, 58), CANVAS, 18).convert("RGBA")
    ocean_draw = ImageDraw.Draw(ocean)
    for _ in range(800):
        x = random.randint(0, CANVAS[0] - 1)
        y = random.randint(0, CANVAS[1] - 1)
        ocean_draw.point((x, y), fill=(220, 205, 165, random.randint(15, 40)))

    map_layer = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    outline_mask = Image.new("L", scaled_size, 0)

    for idx, country in enumerate(COUNTRIES):
        mask = flood_region_mask(passable, country["pos"])
        mask = fill_holes(mask)
        mask = mask.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.MinFilter(9))
        mask = mask.resize(scaled_size, Image.Resampling.NEAREST)
        fill_img = textured_fill(country["fill"], scaled_size, idx + 1).convert("RGBA")
        map_layer.paste(fill_img, OFFSET, mask)
        outline_mask = ImageChops.lighter(outline_mask, mask)

    border = outline_mask.filter(ImageFilter.MaxFilter(7))
    border = ImageChops.subtract(border, outline_mask)
    border_img = Image.new("RGBA", scaled_size, (0, 0, 0, 0))
    border_img.putalpha(border)
    solid_border = Image.new("RGBA", scaled_size, (26, 20, 16, 255))
    map_layer.paste(solid_border, OFFSET, border)

    land_edge = outline_mask.filter(ImageFilter.MaxFilter(15))
    land_edge = ImageChops.subtract(land_edge, outline_mask.filter(ImageFilter.MaxFilter(3)))
    edge_layer = Image.new("RGBA", scaled_size, (221, 187, 121, 0))
    edge_layer.putalpha(land_edge.point(lambda p: min(90, p)))
    map_layer.alpha_composite(edge_layer, OFFSET)

    result = Image.alpha_composite(ocean, map_layer)
    draw = ImageDraw.Draw(result)

    # Decorative frame and title.
    draw.rectangle((32, 32, CANVAS[0] - 32, CANVAS[1] - 32), outline=(191, 148, 79, 255), width=4)
    draw.rectangle((44, 44, CANVAS[0] - 44, CANVAS[1] - 44), outline=(105, 77, 43, 255), width=2)
    text(draw, (110, 110), "ทวีปอาเรเซีย", f(THAI_BOLD, 48), anchor="lm")
    text(draw, (112, 160), "(ARESIA CONTINENT)", f(SERIF_BOLD, 28), anchor="lm")

    # Shields and country labels.
    for country in COUNTRIES:
        center = sxy(*country["pos"])
        shield_size = {"hero": 82, "major": 62, "mid": 52, "small": 42, "tiny": 30}[country["size"]]
        draw_shield(draw, country, center, shield_size)
        if country["size"] in {"hero", "major", "mid"}:
            label_offset = {"hero": 72, "major": 58, "mid": 48}[country["size"]]
            label_font = {
                "hero": f(SERIF_BOLD, 31),
                "major": f(SERIF_BOLD, 23),
                "mid": f(SERIF_BOLD, 20),
            }[country["size"]]
            text(draw, (center[0], center[1] + label_offset), country["name"], label_font)

    # Major legend.
    by_name = {country["name"]: country for country in COUNTRIES}
    legend_x = 110
    legend_y = 260
    text(draw, (legend_x, legend_y), "MAJOR POWERS", f(SERIF_BOLD, 26), anchor="lm")
    legend_y += 56
    for name in ["Eryndor Empire", "Kingdom of Lacoss", "Kingdom of Velmora", "Kingdom of Aetherion", "Republic of Varelia"]:
        country = by_name[name]
        draw_shield(draw, country, (legend_x + 28, legend_y), 42)
        text(draw, (legend_x + 70, legend_y), name, f(SERIF_BOLD, 18), anchor="lm")
        legend_y += 60

    # Smaller states legend for readability.
    left_minor = [
        "Rothmere", "Lysenne", "Marrowen", "Solvane", "Rosvaria", "Caldria",
        "Demeris", "Merenhal", "Valessia", "Ravennair", "Seravelle", "Aurell",
    ]
    right_minor = [
        "Vardane", "Tiravel", "Edevane", "Brannor", "Morvane", "Selvarn", "Verdalis",
        "Dravik", "Nocthar", "Galdren", "Orvessa", "Halcyra", "Berynth", "Prythia",
    ]
    text(draw, (110, 650), "OTHER REALMS", f(SERIF_BOLD, 24), anchor="lm")
    y = 700
    for name in left_minor:
        country = by_name[name]
        draw_shield(draw, country, (132, y), 30)
        text(draw, (160, y), name, f(SERIF_BOLD, 16), anchor="lm")
        y += 42

    y = 700
    x = 350
    for name in right_minor:
        country = by_name[name]
        draw_shield(draw, country, (x, y), 30)
        text(draw, (x + 28, y), name, f(SERIF_BOLD, 16), anchor="lm")
        y += 42

    result = result.convert("RGB")
    result.save(OUT_PNG)
    result.save(OUT_WEBP, "WEBP", quality=95, method=6)
    print(OUT_PNG)


if __name__ == "__main__":
    main()
