from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
from collections import deque
import math
import os
import random
import textwrap

import numpy as np

ROOT = r"C:\Users\dotv5\Desktop\Alcine"
SRC = os.path.join(ROOT, "MAP.png")

OUTS = [
    (os.path.join(ROOT, "aresia-continent-map.png"), "PNG", {}),
    (os.path.join(ROOT, "aresia-continent-map.webp"), "WEBP", {"quality": 94, "method": 6}),
    (os.path.join(ROOT, "continent-map-polished.png"), "PNG", {}),
    (os.path.join(ROOT, "continent-map-polished.webp"), "WEBP", {"quality": 94, "method": 6}),
    (os.path.join(ROOT, "continent-map.webp"), "WEBP", {"quality": 94, "method": 6}),
    (os.path.join(ROOT, "site", "assets", "continent-map.webp"), "WEBP", {"quality": 94, "method": 6}),
    (os.path.join(ROOT, "site", "assets", "continent-map-polished.png"), "PNG", {}),
    (os.path.join(ROOT, "site", "assets", "aresia-continent-map.png"), "PNG", {}),
]

random.seed(42)
rng = np.random.default_rng(42)


def font_path(*names):
    for name in names:
        path = os.path.join(r"C:\Windows\Fonts", name)
        if os.path.exists(path):
            return path
    raise FileNotFoundError(names[0])


SERIF_BOLD = font_path("georgiab.ttf", "timesbd.ttf", "cambriab.ttf", "BOD_B.TTF")
SERIF = font_path("georgia.ttf", "times.ttf", "cambria.ttc", "BASKVILL.TTF")
THAI_BOLD = font_path("tahomabd.ttf", "leelawdb.ttf", "LeelawUI.ttf")
THAI = font_path("tahoma.ttf", "leelawad.ttf", "LeelawUI.ttf")


def f(path, size):
    return ImageFont.truetype(path, size)


# color, reference point, label point, shield point are in the original MAP.png coordinate space.
COUNTRIES = [
    ("eryndor", (237, 28, 36), (552, 398), (590, 530), (590, 430), "Eryndor Empire", "จักรวรรดิเอรินดอร์", "Eryndor", (154, 45, 34), "dragon", "mountain", "huge"),
    ("nordland", (255, 242, 0), (503, 163), (505, 150), (505, 205), "Nordland", "นอร์ดแลนด์", "Nordhold", (214, 174, 73), "snow", "mountain", "small"),
    ("drakvain", (185, 122, 87), (314, 585), (310, 575), (315, 505), "Drakvain", "เดรกเวน", "Drakhold", (136, 84, 45), "mountain", "mountain", "medium"),
    ("lysenn", (161, 251, 142), (247, 805), (245, 780), (245, 850), "Lysenn March", "มาร์ชลิเซนน์", "Lysenn", (103, 149, 84), "leaf", "forest", "small"),
    ("luminas", (167, 201, 162), (279, 966), (280, 950), (280, 1010), "Luminas Holy State", "รัฐศักดิ์สิทธิ์ลูมินาส", "Luminas", (143, 152, 100), "cross", "forest", "small"),
    ("solmire", (249, 255, 177), (313, 1143), (305, 1145), (305, 1085), "Solmire Empire", "จักรวรรดิโซลไมร์", "Solmire", (196, 148, 58), "sun", "desert", "medium"),
    ("velmora", (0, 162, 232), (470, 770), (462, 792), (480, 700), "Velmora Republic", "สาธารณรัฐเวลโมรา", "Velmora", (31, 133, 153), "scales", "hills", "large"),
    ("lacoss", (63, 72, 204), (477, 927), (470, 932), (380, 900), "Kingdom of Lacoss", "อาณาจักรลาคอส", "Lacoss", (43, 80, 139), "lion", "snow", "large"),
    ("myrthale", (115, 201, 181), (360, 1048), (360, 1045), (360, 1008), "Myrthale", "เมอร์เธล", "Myrthale", (53, 126, 120), "wave", "coast", "tiny"),
    ("arclight", (201, 71, 94), (399, 1073), (400, 1075), (402, 1038), "Arclight Theocracy", "เทวรัฐอาร์คไลท์", "Arclight", (142, 47, 66), "star", "hills", "tiny"),
    ("edevane", (0, 201, 155), (446, 1071), (447, 1070), (447, 1036), "Edevane Principality", "รัฐเอเดเวน", "Edevane", (42, 118, 107), "iris", "forest", "tiny"),
    ("vardane", (117, 83, 83), (503, 1072), (503, 1072), (503, 1038), "Vardane", "วาร์เดน", "Vardane", (94, 66, 55), "tower", "hills", "tiny"),
    ("dornwich", (117, 78, 117), (569, 1074), (570, 1075), (570, 1038), "Dornwich", "ดอร์นวิช", "Dornwich", (86, 61, 87), "tower", "hills", "tiny"),
    ("roserainne", (255, 192, 217), (428, 1169), (430, 1160), (430, 1100), "Roserainne Kingdom", "อาณาจักรโรสเรนน์", "Roserainne", (179, 95, 110), "rose", "fields", "medium"),
    ("eldoria", (230, 234, 205), (545, 1186), (555, 1165), (555, 1105), "Eldoria Kingdom", "อาณาจักรเอลดอเรีย", "Eldoria", (177, 159, 105), "wheat", "fields", "medium"),
    ("demeris", (234, 217, 218), (616, 1145), (618, 1135), (618, 1085), "Demeris Coast", "ชายฝั่งเดเมริส", "Demeris", (169, 132, 121), "anchor", "coast", "small"),
    ("brannor", (3, 0, 234), (664, 1013), (660, 1015), (660, 970), "Brannor Coast", "ชายฝั่งบรานนอร์", "Brannor", (36, 64, 160), "wave", "coast", "small"),
    ("ferros", (12, 234, 0), (730, 943), (735, 940), (735, 880), "Ferros", "เฟอร์รอส", "Ferros", (61, 129, 60), "hammer", "mountain", "small"),
    ("aetherion", (112, 146, 190), (700, 794), (723, 815), (705, 730), "Aetherion Kingdom", "อาณาจักรเอเธอเรียน", "Aetherion", (78, 102, 127), "tower", "mountain", "large"),
    ("sylvaris", (200, 191, 231), (852, 737), (850, 735), (850, 680), "Sylvaris Kingdom", "อาณาจักรซิลวาริส", "Sylvaris", (137, 107, 154), "iris", "forest", "medium"),
    ("valessia", (234, 54, 128), (837, 554), (835, 555), (832, 505), "Valessia March", "มาร์ชวาเลสเซีย", "Valessia", (173, 62, 103), "spear", "hills", "small"),
    ("ravenmark", (117, 22, 63), (917, 521), (912, 525), (912, 470), "Ravenmark Duchy", "ดัชชีเรเวนมาร์ก", "Ravenmark", (111, 37, 54), "raven", "forest", "small"),
    ("norviel", (34, 177, 76), (885, 408), (884, 408), (885, 350), "Norviel Federation", "สหพันธรัฐนอร์เวียล", "Norviel", (51, 121, 73), "tree", "forest", "medium"),
    ("aurell", (255, 127, 39), (772, 85), (772, 86), (772, 45), "Aurell", "ออเรล", "Aurell", (184, 98, 46), "sun", "hills", "tiny"),
    ("nocthar", (29, 46, 46), (827, 51), (828, 52), (828, 20), "Nocthar", "น็อกธาร์", "Nocthar", (39, 61, 58), "raven", "forest", "tiny"),
    ("galdren", (127, 127, 127), (829, 95), (830, 96), (830, 135), "Galdren League", "สันนิบาตกัลเดรน", "Galdren", (100, 98, 86), "fort", "mountain", "tiny"),
    ("orvessa", (170, 173, 146), (896, 71), (900, 72), (900, 128), "Orvessa", "ออร์เวสซา", "Orvessa", (126, 137, 100), "leaf", "fields", "tiny"),
    ("carthane", (201, 164, 195), (949, 49), (950, 50), (950, 15), "Carthane", "คาร์เธน", "Carthane", (154, 100, 150), "star", "hills", "tiny"),
    ("prythia", (201, 128, 196), (994, 66), (995, 66), (995, 112), "Prythia", "พริเธีย", "Prythia", (160, 92, 151), "iris", "hills", "tiny"),
    ("durnholt", (201, 142, 107), (961, 97), (962, 98), (962, 134), "Durnholt", "เดิร์นโฮลต์", "Durnholt", (142, 83, 66), "fort", "hills", "tiny"),
    ("varelia", (202, 234, 102), (407, 1324), (455, 1315), (407, 1285), "Republic of Varelia", "สาธารณรัฐวาเรเลีย", "Varelia", (83, 142, 76), "anchor", "coast", "small"),
]


def as_dict(row):
    keys = ["key", "source_color", "point", "label", "shield", "name", "thai", "capital", "fill", "symbol", "theme", "size"]
    return dict(zip(keys, row))


countries = [as_dict(c) for c in COUNTRIES]
src = Image.open(SRC).convert("RGB")
arr = np.array(src)
h0, w0 = arr.shape[:2]


def connected_components(mask):
    visited = np.zeros(mask.shape, dtype=bool)
    comps = []
    ys, xs = np.nonzero(mask)
    for sy, sx in zip(ys, xs):
        if visited[sy, sx]:
            continue
        stack = [(int(sy), int(sx))]
        visited[sy, sx] = True
        pts = []
        minx = maxx = int(sx)
        miny = maxy = int(sy)
        while stack:
            y, x = stack.pop()
            pts.append((y, x))
            minx, maxx = min(minx, x), max(maxx, x)
            miny, maxy = min(miny, y), max(maxy, y)
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                ny, nx = y + dy, x + dx
                if 0 <= ny < h0 and 0 <= nx < w0 and mask[ny, nx] and not visited[ny, nx]:
                    visited[ny, nx] = True
                    stack.append((ny, nx))
        if len(pts) >= 40:
            comps.append((len(pts), (minx, miny, maxx, maxy), pts))
    return comps


def fill_holes(mask):
    inv = ~mask
    seen = np.zeros(mask.shape, dtype=bool)
    q = deque()
    h, w = mask.shape
    for x in range(w):
        for y in (0, h - 1):
            if inv[y, x] and not seen[y, x]:
                seen[y, x] = True
                q.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if inv[y, x] and not seen[y, x]:
                seen[y, x] = True
                q.append((y, x))
    while q:
        y, x = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and inv[ny, nx] and not seen[ny, nx]:
                seen[ny, nx] = True
                q.append((ny, nx))
    return mask | (inv & ~seen)


def pick_mask(country):
    color = np.array(country["source_color"], dtype=np.int16)
    diff = np.abs(arr.astype(np.int16) - color).sum(axis=2)
    comps = connected_components(diff < 10)
    px, py = country["point"]

    def score(comp):
        count, (x0, y0, x1, y1), _ = comp
        return math.hypot((x0 + x1) / 2 - px, (y0 + y1) / 2 - py) - math.log(max(count, 1)) * 2

    count, bbox, pts = min(comps, key=score)
    out = np.zeros((h0, w0), dtype=bool)
    for y, x in pts:
        out[y, x] = True
    pil = Image.fromarray((out * 255).astype(np.uint8), "L").filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.MinFilter(3))
    out = fill_holes(np.array(pil) > 80)
    country["mask0"] = out
    country["area0"] = count


for country in countries:
    pick_mask(country)

union0 = np.zeros((h0, w0), dtype=bool)
for country in countries:
    union0 |= country["mask0"]
ys, xs = np.nonzero(union0)
pad = 22
cl, ct = max(int(xs.min()) - pad, 0), max(int(ys.min()) - pad, 0)
cr, cb = min(int(xs.max()) + pad, w0 - 1), min(int(ys.max()) + pad, h0 - 1)
crop_w, crop_h = cr - cl + 1, cb - ct + 1

w, h = 2400, 1800
map_h = 1660
scale = map_h / crop_h
map_w = int(crop_w * scale)
map_x, map_y = 600, 70


def t(point):
    x, y = point
    return int(round(map_x + (x - cl) * scale)), int(round(map_y + (y - ct) * scale))


def resize_mask(mask):
    crop = Image.fromarray((mask[ct: cb + 1, cl: cr + 1] * 255).astype(np.uint8), "L")
    return crop.resize((map_w, map_h), Image.Resampling.LANCZOS)


for country in countries:
    country["mask"] = resize_mask(country["mask0"])
    country["label_xy"] = t(country["label"])
    country["shield_xy"] = t(country["shield"])


def ocean_background():
    base = np.array([23, 60, 70], dtype=np.float32)
    noise = rng.normal(0, 11, (h, w, 1))
    ygrad = np.linspace(1.1, 0.82, h)[:, None, None]
    xgrad = np.linspace(0.95, 1.07, w)[None, :, None]
    data = np.clip(base * ygrad * xgrad + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(data, "RGB").convert("RGBA")


canvas = ocean_background()
draw = ImageDraw.Draw(canvas)
gold = (187, 139, 72, 255)
dark = (39, 31, 23, 255)
cream = (239, 218, 176, 255)

for off, col, width in [(18, dark, 5), (28, gold, 2), (34, (230, 210, 165, 210), 1)]:
    draw.rectangle((off, off, w - off, h - off), outline=col, width=width)
for sx, sy in [(1, 1), (-1, 1), (1, -1), (-1, -1)]:
    cx = 48 if sx == 1 else w - 48
    cy = 48 if sy == 1 else h - 48
    for radius in (28, 48, 70):
        x0, x1 = sorted([cx - sx * radius, cx + sx * radius])
        y0, y1 = sorted([cy - sy * radius, cy + sy * radius])
        start = 180 if sx == 1 and sy == 1 else 270 if sx == -1 and sy == 1 else 90 if sx == 1 else 0
        draw.arc((x0, y0, x1, y1), start=start, end=start + 90, fill=gold, width=2)

land_mask = Image.new("L", (w, h), 0)
for country in countries:
    layer = Image.new("L", (w, h), 0)
    layer.paste(country["mask"], (map_x, map_y))
    land_mask = ImageChops.lighter(land_mask, layer)

shadow = land_mask.filter(ImageFilter.MaxFilter(47)).filter(ImageFilter.GaussianBlur(18))
coast = land_mask.filter(ImageFilter.MaxFilter(31)).filter(ImageFilter.GaussianBlur(10))
shadow_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
shadow_layer.paste(Image.new("RGBA", (w, h), (0, 0, 0, 120)), (0, 0), shadow)
canvas.alpha_composite(shadow_layer)
coast_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
coast_layer.paste(Image.new("RGBA", (w, h), (220, 205, 150, 105)), (0, 0), coast)
canvas.alpha_composite(coast_layer)


def country_texture(fill, width, height, theme):
    color = np.array(fill, dtype=np.float32)
    noise = rng.normal(0, 18, (height, width, 1))
    wave = np.sin(np.linspace(0, math.pi * 8, width)[None, :, None] + rng.random() * 6) * 5
    data = color + noise + wave
    tint = {
        "snow": np.array([28, 42, 70]),
        "desert": np.array([211, 164, 76]),
        "forest": np.array([35, 85, 48]),
        "mountain": np.array([70, 55, 45]),
    }.get(theme)
    if tint is not None:
        data = data * 0.88 + tint * 0.12
    return Image.fromarray(np.clip(data, 0, 255).astype(np.uint8), "RGB").convert("RGBA")


for country in sorted(countries, key=lambda c: c["area0"], reverse=True):
    full_mask = Image.new("L", (w, h), 0)
    full_mask.paste(country["mask"], (map_x, map_y))
    bbox = full_mask.getbbox()
    if not bbox:
        continue
    x0, y0, x1, y1 = bbox
    tex = country_texture(country["fill"], x1 - x0, y1 - y0, country["theme"])
    canvas.paste(tex, (x0, y0), full_mask.crop(bbox))

border_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
for country in countries:
    full_mask = Image.new("L", (w, h), 0)
    full_mask.paste(country["mask"], (map_x, map_y))
    edge = ImageChops.subtract(full_mask.filter(ImageFilter.MaxFilter(11)), full_mask.filter(ImageFilter.MinFilter(7))).filter(ImageFilter.GaussianBlur(0.45))
    tmp = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    tmp.paste(Image.new("RGBA", (w, h), (55, 43, 31, 230)), (0, 0), edge)
    border_layer.alpha_composite(tmp)
    gold_edge = ImageChops.subtract(full_mask.filter(ImageFilter.MaxFilter(5)), full_mask.filter(ImageFilter.MinFilter(3))).filter(ImageFilter.GaussianBlur(0.35))
    tmp = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    tmp.paste(Image.new("RGBA", (w, h), (173, 134, 74, 90)), (0, 0), gold_edge)
    border_layer.alpha_composite(tmp)
canvas.alpha_composite(border_layer)
draw = ImageDraw.Draw(canvas)


def draw_mountain(d, x, y, s, col=(62, 49, 36, 185)):
    d.polygon([(x - s, y + s), (x, y - s), (x + s, y + s)], outline=col, fill=(70, 60, 48, 70))
    d.line([(x, y - s), (x - s // 3, y + s // 3)], fill=(235, 220, 185, 100), width=max(1, s // 7))
    d.polygon([(x + s // 2, y + s), (x + s * 3 // 2, y), (x + s * 2, y + s)], outline=col, fill=(70, 60, 48, 55))


def draw_tree(d, x, y, s, col=(35, 76, 44, 165)):
    d.rectangle((x - s // 8, y + s // 4, x + s // 8, y + s), fill=(72, 49, 29, 130))
    d.polygon([(x, y - s), (x - s // 2, y + s // 3), (x + s // 2, y + s // 3)], fill=col)
    d.polygon([(x, y - s // 2), (x - int(s * 0.62), y + s // 2), (x + int(s * 0.62), y + s // 2)], fill=col)


def draw_city(d, x, y, s, col=(43, 34, 25, 175)):
    d.rectangle((x - s, y - s // 2, x + s, y + s // 2), outline=col, fill=(60, 48, 38, 70), width=max(1, s // 8))
    d.rectangle((x - s // 2, y - s, x + s // 2, y + s // 2), outline=col, fill=(60, 48, 38, 70), width=max(1, s // 8))
    d.polygon([(x - s // 2, y - s), (x, y - int(s * 1.45)), (x + s // 2, y - s)], outline=col, fill=(90, 65, 40, 90))


def draw_dunes(d, x, y, s, col=(102, 69, 35, 120)):
    for i in range(3):
        yy = y + i * s // 3
        d.arc((x - s, yy - s // 2, x + s, yy + s // 2), 180, 360, fill=col, width=max(1, s // 8))


terrain = Image.new("RGBA", (w, h), (0, 0, 0, 0))
td = ImageDraw.Draw(terrain)
for country in countries:
    full_mask = Image.new("L", (w, h), 0)
    full_mask.paste(country["mask"], (map_x, map_y))
    bbox = full_mask.getbbox()
    if not bbox:
        continue
    x0, y0, x1, y1 = bbox
    count = {"huge": 95, "large": 45, "medium": 28, "small": 14, "tiny": 5}[country["size"]]
    placed = 0
    for _ in range(count * 28):
        if placed >= count:
            break
        x = random.randint(x0 + 8, x1 - 8)
        y = random.randint(y0 + 8, y1 - 8)
        if full_mask.getpixel((x, y)) < 150:
            continue
        if math.hypot(x - country["label_xy"][0], y - country["label_xy"][1]) < (95 if country["size"] in ("huge", "large") else 50):
            continue
        s = random.randint(11, 20) if country["size"] in ("huge", "large", "medium") else random.randint(7, 11)
        theme = country["theme"]
        if theme in ("mountain", "snow") and random.random() < 0.62:
            draw_mountain(td, x, y, s)
        elif theme == "forest" or (theme == "snow" and random.random() < 0.35):
            draw_tree(td, x, y, s)
        elif theme == "desert":
            draw_dunes(td, x, y, s)
        elif theme in ("fields", "hills"):
            draw_tree(td, x, y, s) if random.random() < 0.45 else draw_mountain(td, x, y, s)
        else:
            draw_city(td, x, y, s)
        placed += 1
canvas.alpha_composite(terrain)
draw = ImageDraw.Draw(canvas)


def draw_river(points, color=(39, 110, 145, 165)):
    draw.line(points, fill=(13, 40, 53, 130), width=9, joint="curve")
    draw.line(points, fill=color, width=5, joint="curve")
    draw.line(points, fill=(135, 205, 218, 110), width=1, joint="curve")


draw_river([t(p) for p in [(405, 625), (500, 650), (615, 675), (710, 640), (800, 610)]])
draw_river([t(p) for p in [(650, 785), (705, 820), (770, 835), (825, 810)]], (55, 128, 158, 145))


def shield_points(cx, cy, width, height):
    return [
        (cx - width / 2, cy - height / 2),
        (cx + width / 2, cy - height / 2),
        (cx + width * 0.45, cy - height * 0.05),
        (cx + width * 0.26, cy + height * 0.28),
        (cx, cy + height / 2),
        (cx - width * 0.26, cy + height * 0.28),
        (cx - width * 0.45, cy - height * 0.05),
    ]


def draw_symbol(d, symbol, cx, cy, s, col, darkcol):
    width = max(1, int(s / 14))
    if symbol == "dragon":
        d.polygon([(cx - s * .35, cy + s * .05), (cx - s * .08, cy - s * .32), (cx + s * .05, cy + s * .02)], fill=darkcol)
        d.polygon([(cx + s * .1, cy + s * .04), (cx + s * .42, cy - s * .26), (cx + s * .32, cy + s * .12)], fill=darkcol)
        d.arc((cx - s * .25, cy - s * .28, cx + s * .38, cy + s * .35), 105, 345, fill=darkcol, width=max(2, int(s * .09)))
        d.ellipse((cx + s * .22, cy - s * .30, cx + s * .43, cy - s * .10), fill=darkcol)
        d.polygon([(cx + s * .39, cy - s * .24), (cx + s * .56, cy - s * .32), (cx + s * .43, cy - s * .17)], fill=darkcol)
    elif symbol == "lion":
        d.ellipse((cx - s * .25, cy - s * .12, cx + s * .20, cy + s * .25), fill=col)
        d.ellipse((cx + s * .08, cy - s * .34, cx + s * .36, cy - s * .08), fill=col)
        d.arc((cx - s * .48, cy - s * .30, cx - s * .10, cy + s * .28), 210, 80, fill=col, width=max(2, int(s * .10)))
        d.line((cx - s * .05, cy + s * .20, cx - s * .25, cy + s * .44), fill=col, width=max(2, int(s * .08)))
        d.line((cx + s * .15, cy + s * .18, cx + s * .34, cy + s * .42), fill=col, width=max(2, int(s * .08)))
        d.polygon([(cx + s * .05, cy - s * .35), (cx + s * .15, cy - s * .55), (cx + s * .25, cy - s * .35)], fill=col)
    elif symbol == "scales":
        d.line((cx, cy - s * .40, cx, cy + s * .38), fill=col, width=width * 2)
        d.line((cx - s * .42, cy - s * .18, cx + s * .42, cy - s * .18), fill=col, width=width * 2)
        for sign in (-1, 1):
            bx = cx + sign * s * .30
            d.line((bx, cy - s * .18, bx - sign * s * .08, cy + s * .08), fill=col, width=width)
            d.line((bx, cy - s * .18, bx + sign * s * .08, cy + s * .08), fill=col, width=width)
            d.arc((bx - s * .17, cy + s * .03, bx + s * .17, cy + s * .20), 0, 180, fill=col, width=width * 2)
    elif symbol in ("tower", "fort"):
        d.rectangle((cx - s * .25, cy - s * .28, cx + s * .25, cy + s * .38), outline=col, width=width * 2)
        for offset in (-.22, 0, .22):
            d.rectangle((cx + offset * s - s * .08, cy - s * .44, cx + offset * s + s * .08, cy - s * .28), fill=col)
        d.rectangle((cx - s * .07, cy + s * .08, cx + s * .07, cy + s * .38), fill=col)
    elif symbol == "anchor":
        d.line((cx, cy - s * .42, cx, cy + s * .30), fill=col, width=width * 2)
        d.ellipse((cx - s * .12, cy - s * .50, cx + s * .12, cy - s * .26), outline=col, width=width * 2)
        d.arc((cx - s * .42, cy - s * .05, cx + s * .42, cy + s * .55), 20, 160, fill=col, width=width * 2)
        d.line((cx - s * .22, cy - s * .18, cx + s * .22, cy - s * .18), fill=col, width=width * 2)
    elif symbol in ("snow", "star"):
        for angle in range(0, 180, 30):
            a = math.radians(angle)
            d.line((cx - math.cos(a) * s * .42, cy - math.sin(a) * s * .42, cx + math.cos(a) * s * .42, cy + math.sin(a) * s * .42), fill=col, width=width)
        d.ellipse((cx - s * .11, cy - s * .11, cx + s * .11, cy + s * .11), fill=col)
    elif symbol == "mountain":
        d.polygon([(cx - s * .45, cy + s * .32), (cx - s * .08, cy - s * .35), (cx + s * .18, cy + s * .32)], outline=col, width=width * 2)
        d.polygon([(cx - s * .04, cy + s * .32), (cx + s * .25, cy - s * .16), (cx + s * .48, cy + s * .32)], outline=col, width=width * 2)
    elif symbol in ("leaf", "tree"):
        d.line((cx, cy + s * .38, cx, cy - s * .25), fill=col, width=width * 2)
        d.ellipse((cx - s * .42, cy - s * .40, cx + s * .08, cy + s * .05), outline=col, width=width * 2)
        d.ellipse((cx - s * .08, cy - s * .28, cx + s * .42, cy + s * .18), outline=col, width=width * 2)
    elif symbol == "cross":
        d.rectangle((cx - s * .08, cy - s * .42, cx + s * .08, cy + s * .42), fill=col)
        d.rectangle((cx - s * .32, cy - s * .12, cx + s * .32, cy + s * .05), fill=col)
    elif symbol == "sun":
        for angle in range(0, 360, 30):
            a = math.radians(angle)
            d.line((cx + math.cos(a) * s * .22, cy + math.sin(a) * s * .22, cx + math.cos(a) * s * .45, cy + math.sin(a) * s * .45), fill=col, width=width)
        d.ellipse((cx - s * .22, cy - s * .22, cx + s * .22, cy + s * .22), outline=col, width=width * 2)
    elif symbol == "rose":
        for angle in range(0, 360, 72):
            a = math.radians(angle)
            ex, ey = cx + math.cos(a) * s * .18, cy + math.sin(a) * s * .18
            d.ellipse((ex - s * .16, ey - s * .11, ex + s * .16, ey + s * .11), fill=col)
        d.ellipse((cx - s * .10, cy - s * .10, cx + s * .10, cy + s * .10), fill=darkcol)
    elif symbol == "hammer":
        for angle in (-35, 35):
            a = math.radians(angle)
            x1, y1 = cx - math.sin(a) * s * .38, cy + math.cos(a) * s * .38
            x2, y2 = cx + math.sin(a) * s * .28, cy - math.cos(a) * s * .28
            d.line((x1, y1, x2, y2), fill=col, width=width * 2)
            d.rectangle((x2 - s * .18, y2 - s * .06, x2 + s * .18, y2 + s * .06), fill=col)
    elif symbol == "raven":
        d.pieslice((cx - s * .48, cy - s * .32, cx + s * .40, cy + s * .46), 205, 355, fill=darkcol)
        d.polygon([(cx + s * .22, cy - s * .05), (cx + s * .52, cy - s * .16), (cx + s * .28, cy + s * .05)], fill=darkcol)
    elif symbol == "spear":
        d.line((cx - s * .32, cy + s * .38, cx + s * .28, cy - s * .35), fill=col, width=width * 2)
        d.polygon([(cx + s * .28, cy - s * .35), (cx + s * .45, cy - s * .48), (cx + s * .36, cy - s * .24)], fill=col)
    elif symbol == "iris":
        for angle in range(0, 360, 60):
            a = math.radians(angle)
            d.line((cx, cy, cx + math.cos(a) * s * .42, cy + math.sin(a) * s * .42), fill=col, width=width)
        d.ellipse((cx - s * .13, cy - s * .13, cx + s * .13, cy + s * .13), fill=col)
    elif symbol == "wave":
        for i in range(3):
            yy = cy - s * .2 + i * s * .2
            d.arc((cx - s * .42, yy - s * .15, cx + s * .10, yy + s * .16), 180, 360, fill=col, width=width * 2)
            d.arc((cx - s * .02, yy - s * .15, cx + s * .48, yy + s * .16), 180, 360, fill=col, width=width * 2)
    elif symbol == "wheat":
        d.line((cx, cy + s * .40, cx, cy - s * .36), fill=col, width=width * 2)
        for i in range(5):
            yy = cy + s * .18 - i * s * .14
            d.line((cx, yy, cx - s * .25, yy - s * .12), fill=col, width=width)
            d.line((cx, yy, cx + s * .25, yy - s * .12), fill=col, width=width)


def draw_shield(d, cx, cy, size, fill, symbol, accent=(226, 190, 105, 255)):
    sw, sh = size, int(size * 1.18)
    pts = shield_points(cx, cy, sw, sh)
    d.polygon([(x + 4, y + 6) for x, y in pts], fill=(0, 0, 0, 95))
    d.polygon(pts, fill=(38, 31, 25, 255))
    inner = shield_points(cx, cy, sw * .86, sh * .86)
    d.polygon(inner, fill=tuple(fill) + (255,))
    d.line(inner + [inner[0]], fill=accent, width=max(2, int(size * .045)))
    d.line([(cx - sw * .36, cy - sh * .27), (cx + sw * .36, cy - sh * .27)], fill=(245, 220, 145, 160), width=max(1, int(size * .035)))
    dark_symbol = (18, 16, 15, 245) if symbol in ("dragon", "raven") else accent
    draw_symbol(d, symbol, cx, cy + size * .04, size * .58, accent, dark_symbol)


for country in countries:
    sx, sy = country["shield_xy"]
    size = {"huge": 88, "large": 72, "medium": 58, "small": 42, "tiny": 30}[country["size"]]
    draw_shield(draw, sx, sy, size, country["fill"], country["symbol"])


def centered_lines(d, x, y, lines, fonts, fills, strokes, spacing=4):
    heights = []
    total = 0
    for text, font, stroke in zip(lines, fonts, strokes):
        bbox = d.textbbox((0, 0), text, font=font, stroke_width=stroke)
        height = bbox[3] - bbox[1]
        heights.append(height)
        total += height
    total += spacing * (len(lines) - 1)
    yy = y - total / 2
    for i, (text, font) in enumerate(zip(lines, fonts)):
        d.text((x, yy), text, font=font, anchor="ma", align="center", fill=fills[i], stroke_width=strokes[i], stroke_fill=(45, 33, 25, 230))
        yy += heights[i] + spacing


for country in countries:
    x, y = country["label_xy"]
    size = country["size"]
    if size == "huge":
        centered_lines(draw, x, y, [country["name"], f"({country['thai']})", f"เมืองหลวง: {country['capital']}"], [f(SERIF_BOLD, 58), f(THAI_BOLD, 26), f(THAI_BOLD, 20)], [(248, 231, 196, 255)] * 3, [3, 2, 2], 2)
    elif size == "large":
        if country["key"] in ("velmora", "aetherion"):
            fonts = [f(SERIF_BOLD, 34), f(THAI_BOLD, 18), f(THAI_BOLD, 15)]
        elif country["key"] == "lacoss":
            fonts = [f(SERIF_BOLD, 40), f(THAI_BOLD, 21), f(THAI_BOLD, 16)]
        else:
            fonts = [f(SERIF_BOLD, 42), f(THAI_BOLD, 22), f(THAI_BOLD, 16)]
        centered_lines(draw, x, y, [country["name"], f"({country['thai']})", f"เมืองหลวง: {country['capital']}"], fonts, [(248, 231, 196, 255)] * 3, [3, 2, 1], 1)
    elif size == "medium":
        label_name = country["name"]
        if country["key"] in ("solmire", "roserainne", "eldoria"):
            label_name = label_name.replace(" Empire", "").replace(" Kingdom", "")
        centered_lines(draw, x, y, [label_name, f"({country['thai']})"], [f(SERIF_BOLD, 23), f(THAI_BOLD, 14)], [(248, 231, 196, 255)] * 2, [2, 1], 0)
    elif size == "small":
        short = country["name"].replace(" Federation", "").replace(" Kingdom", "").replace(" Republic", "").replace(" March", "")
        centered_lines(draw, x, y, [short, country["thai"]], [f(SERIF_BOLD, 22), f(THAI_BOLD, 14)], [(247, 231, 196, 255)] * 2, [2, 1], 0)
    else:
        centered_lines(draw, x, y, [country["name"].split()[0]], [f(SERIF_BOLD, 15)], [(247, 231, 196, 245)], [1], 0)

bx1, by1 = t((398, 1245))
bx2, by2 = t((405, 1300))
draw.line((bx1, by1, bx2, by2), fill=(45, 34, 25, 230), width=4)
for i in range(6):
    yy = by1 + (by2 - by1) * i / 5
    draw.line((bx1 - 12, yy, bx1 + 18, yy), fill=(215, 180, 110, 190), width=2)


def draw_compass(cx, cy, radius):
    draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), outline=gold, width=2)
    for i in range(16):
        angle = math.radians(i * 22.5)
        rr = radius if i % 2 == 0 else radius * .65
        draw.line((cx, cy, cx + math.sin(angle) * rr, cy - math.cos(angle) * rr), fill=(202, 170, 105, 170), width=1)
    for angle, label in [(0, "N"), (90, "E"), (180, "S"), (270, "W")]:
        a = math.radians(angle)
        draw.text((cx + math.sin(a) * (radius + 28), cy - math.cos(a) * (radius + 28)), label, font=f(SERIF_BOLD, 28), anchor="mm", fill=cream, stroke_width=2, stroke_fill=(30, 25, 20, 180))
    draw.polygon([(cx, cy - radius + 8), (cx - 11, cy + 8), (cx, cy), (cx + 11, cy + 8)], fill=(225, 195, 125, 230), outline=dark)
    draw.polygon([(cx, cy + radius - 8), (cx - 8, cy - 5), (cx, cy), (cx + 8, cy - 5)], fill=(75, 60, 45, 230), outline=dark)


def draw_ship(x, y, s):
    draw.arc((x - s, y, x + s, y + s // 2), 0, 180, fill=(195, 160, 105, 170), width=3)
    draw.line((x, y, x, y - s), fill=(195, 160, 105, 170), width=2)
    draw.polygon([(x + 2, y - s), (x + 2, y - 5), (x + s // 2, y - 10)], fill=(215, 205, 175, 120), outline=(160, 130, 80, 130))
    draw.polygon([(x - 2, y - s + 10), (x - 2, y - 3), (x - s // 2, y - 8)], fill=(215, 205, 175, 110), outline=(160, 130, 80, 130))


draw_compass(w - 210, 235, 72)
for ship in [(1980, 560, 34), (2150, 1110, 30), (1775, 1590, 28), (255, 1545, 30)]:
    draw_ship(*ship)

draw_shield(draw, 1890, 1100, 46, (52, 47, 43), "raven")
centered_lines(draw, 2020, 1120, ["Ironhold Isles", "หมู่เกาะไอรอนโฮลด์"], [f(SERIF_BOLD, 26), f(THAI_BOLD, 16)], [(238, 220, 181, 245)] * 2, [2, 1], 1)
for ox, oy in [(1880, 1160), (1935, 1175), (2025, 1150), (1985, 1218)]:
    draw.ellipse((ox - 18, oy - 10, ox + 25, oy + 15), fill=(105, 83, 50, 190), outline=(43, 32, 22, 220), width=2)
    draw_mountain(draw, ox + 2, oy, 11, (52, 42, 30, 180))


def parchment_panel(x, y, width, height, alpha=214):
    panel = Image.new("RGBA", (width, height), (210, 188, 142, alpha))
    pn = rng.normal(0, 10, (height, width, 1))
    pa = np.clip(np.array(panel).astype(np.int16) + np.concatenate([pn, pn, pn, np.zeros((height, width, 1))], axis=2), 0, 255).astype(np.uint8)
    p = Image.fromarray(pa, "RGBA")
    mask = Image.new("L", (width, height), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, width, height), radius=5, fill=255)
    canvas.paste(p, (x, y), mask)
    draw.rectangle((x, y, x + width, y + height), outline=(62, 46, 31, 230), width=3)
    draw.rectangle((x + 8, y + 8, x + width - 8, y + height - 8), outline=(153, 106, 55, 200), width=1)


draw.text((54, 58), "ทวีปอาเรเซีย", font=f(THAI_BOLD, 64), fill=(246, 220, 160, 255), stroke_width=2, stroke_fill=(27, 22, 18, 230))
draw.text((58, 134), "(ARESIA CONTINENT)", font=f(SERIF_BOLD, 34), fill=(238, 210, 158, 250), stroke_width=1, stroke_fill=(27, 22, 18, 220))
draw.line((54, 190, 434, 190), fill=gold, width=2)
intro = "ทวีปที่หลายอาณาจักรแย่งชิงอำนาจ\nศูนย์กลางสงครามคือจักรวรรดิเอรินดอร์\nและดินแดนเก่าของ Lacoss ทางตอนล่าง"
for i, line in enumerate(intro.split("\n")):
    draw.text((54, 214 + i * 34), line, font=f(THAI, 24), fill=(232, 211, 174, 245), stroke_width=1, stroke_fill=(18, 22, 20, 160))

parchment_panel(48, 350, 450, 680, 218)
draw.text((78, 382), "ชาติมหาอำนาจ", font=f(THAI_BOLD, 30), fill=(52, 37, 25, 255))
keymap = {country["key"]: country for country in countries}
legend_items = [
    ("eryndor", "มหาอำนาจทหารและศัตรูหลักของ Lacoss"),
    ("lacoss", "อาณาจักรเก่าของราชวงศ์และตระกูล Alcine"),
    ("velmora", "รัฐการค้าและศูนย์กลางเส้นทางเศรษฐกิจ"),
    ("aetherion", "อาณาจักรหุบเขาและนักเวทแนวหน้า"),
    ("varelia", "รัฐเกาะทางใต้และจุดรวมผู้ลี้ภัย"),
]
ly = 438
for key, desc in legend_items:
    country = keymap[key]
    draw_shield(draw, 92, ly + 32, 48, country["fill"], country["symbol"])
    draw.text((128, ly), country["name"], font=f(SERIF_BOLD, 22), fill=(45, 31, 22, 255))
    draw.text((128, ly + 27), f"({country['thai']})", font=f(THAI_BOLD, 15), fill=(65, 45, 31, 255))
    for j, line in enumerate(textwrap.wrap(desc, width=31)[:2]):
        draw.text((128, ly + 52 + j * 20), line, font=f(THAI, 15), fill=(66, 49, 35, 255))
    ly += 116

parchment_panel(48, 1070, 330, 260, 214)
draw.text((78, 1095), "สัญลักษณ์", font=f(THAI_BOLD, 28), fill=(52, 37, 25, 255))
for i, label in enumerate(["เมืองหลวง", "เมืองสำคัญ", "เทือกเขา", "ป่าไม้", "ทะเล/มหาสมุทร"]):
    yy = 1140 + i * 36
    ix = 92
    if i == 0:
        draw.regular_polygon((ix, yy, 12), n_sides=5, rotation=-90, fill=(120, 74, 28, 255), outline=(70, 45, 25, 255))
    elif i == 1:
        draw.ellipse((ix - 8, yy - 8, ix + 8, yy + 8), outline=(70, 45, 25, 255), width=2)
    elif i == 2:
        draw_mountain(draw, ix, yy + 3, 10, (70, 45, 25, 220))
    elif i == 3:
        draw_tree(draw, ix, yy + 2, 10, (45, 88, 46, 220))
    else:
        draw.arc((ix - 18, yy - 5, ix + 8, yy + 11), 180, 360, fill=(70, 45, 25, 220), width=2)
        draw.arc((ix, yy - 5, ix + 26, yy + 11), 180, 360, fill=(70, 45, 25, 220), width=2)
    draw.text((122, yy - 12), label, font=f(THAI, 18), fill=(60, 43, 30, 255))

for text, xy in [
    ("The Western Ocean\n(มหาสมุทรตะวันตก)", (250, 1370)),
    ("The Eastern Ocean\n(มหาสมุทรตะวันออก)", (2020, 1360)),
    ("The Southern Sea\n(ทะเลใต้)", (1865, 1660)),
]:
    centered_lines(draw, xy[0], xy[1], text.split("\n"), [f(SERIF, 24), f(THAI, 17)], [(226, 206, 170, 210)] * 2, [1, 1], 2)

sx, sy = 74, h - 94
draw.line((sx, sy, sx + 340, sy), fill=(238, 218, 170, 240), width=5)
for i in range(6):
    x = sx + i * 68
    draw.line((x, sy - 12, x, sy + 12), fill=(238, 218, 170, 240), width=2)
    draw.text((x, sy + 18), str(i * 100), font=f(SERIF, 16), fill=(238, 218, 170, 230), anchor="ma")
draw.text((sx + 380, sy + 18), "km", font=f(SERIF, 18), fill=(238, 218, 170, 230), anchor="ma")

grain = Image.effect_noise((w, h), 18).convert("L").point(lambda p: 32 if p > 140 else 0)
grain_layer = Image.new("RGBA", (w, h), (255, 235, 190, 0))
grain_layer.putalpha(grain)
canvas.alpha_composite(grain_layer)
canvas = canvas.filter(ImageFilter.UnsharpMask(radius=1.2, percent=80, threshold=3))
rgb = canvas.convert("RGB")

for path, fmt, kwargs in OUTS:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    rgb.save(path, fmt, **kwargs)

print(f"saved {OUTS[0][0]} {rgb.size[0]}x{rgb.size[1]}")
