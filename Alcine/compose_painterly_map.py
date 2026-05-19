from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import os

ROOT = r"C:\Users\dotv5\Desktop\Alcine"
BASE = os.path.join(ROOT, "aresia-painterly-base.png")
OUT_PNG = os.path.join(ROOT, "aresia-continent-map-v2.png")
OUT_WEBP = os.path.join(ROOT, "aresia-continent-map-v2.webp")


def font_path(*names):
    for name in names:
        path = os.path.join(r"C:\Windows\Fonts", name)
        if os.path.exists(path):
            return path
    raise FileNotFoundError(names[0])


SERIF_BOLD = font_path("georgiab.ttf", "BASKVILL.TTF", "timesbd.ttf")
SERIF = font_path("georgia.ttf", "BASKVILL.TTF", "times.ttf")
THAI_BOLD = font_path("tahomabd.ttf", "leelawdb.ttf", "LeelawUI.ttf")
THAI = font_path("tahoma.ttf", "leelawad.ttf", "LeelawUI.ttf")


def f(path, size):
    return ImageFont.truetype(path, size)


COUNTRIES = [
    dict(name="Nordland", xy=(580, 125), shield=(580, 82), color=(177, 132, 49), symbol="sun", size="small"),
    dict(name="Drakvain", xy=(390, 365), shield=(390, 315), color=(103, 73, 44), symbol="tower", size="small"),
    dict(name="Eryndor Empire", xy=(705, 355), shield=(710, 280), color=(122, 29, 24), symbol="dragon", size="hero"),
    dict(name="Norviel Federation", xy=(1084, 305), shield=(1085, 255), color=(41, 97, 54), symbol="tree", size="small"),
    dict(name="Ravenmark Duchy", xy=(1090, 445), shield=(1090, 398), color=(104, 35, 51), symbol="raven", size="small"),
    dict(name="Sylvaris Kingdom", xy=(1082, 572), shield=(1082, 520), color=(104, 86, 134), symbol="star", size="small"),
    dict(name="Kingdom of Velmora", xy=(620, 575), shield=(620, 525), color=(20, 106, 135), symbol="scales", size="small"),
    dict(name="Aetherion Kingdom", xy=(842, 605), shield=(842, 553), color=(77, 91, 109), symbol="tower", size="small"),
    dict(name="Kingdom of Lacoss", xy=(595, 705), shield=(595, 640), color=(29, 70, 130), symbol="lion", size="hero"),
    dict(name="Ferros", xy=(922, 724), shield=(922, 678), color=(53, 102, 49), symbol="hammer", size="small"),
    dict(name="Solmire Empire", xy=(394, 850), shield=(394, 804), color=(171, 117, 42), symbol="sun", size="small"),
    dict(name="Roserainne Kingdom", xy=(618, 835), shield=(618, 790), color=(143, 74, 92), symbol="rose", size="small"),
    dict(name="Eldoria Kingdom", xy=(807, 855), shield=(807, 808), color=(154, 128, 81), symbol="wheat", size="small"),
    dict(name="Republic of Varelia", xy=(663, 1018), shield=(663, 970), color=(61, 110, 57), symbol="anchor", size="small"),
]


def shield_points(cx, cy, width, height):
    return [
        (cx - width / 2, cy - height / 2),
        (cx + width / 2, cy - height / 2),
        (cx + width * 0.44, cy - height * 0.05),
        (cx + width * 0.23, cy + height * 0.27),
        (cx, cy + height / 2),
        (cx - width * 0.23, cy + height * 0.27),
        (cx - width * 0.44, cy - height * 0.05),
    ]


def draw_symbol(draw, symbol, cx, cy, s, accent, dark):
    width = max(2, int(s / 10))
    if symbol == "dragon":
        draw.arc((cx - s * .36, cy - s * .26, cx + s * .36, cy + s * .34), 100, 350, fill=dark, width=width)
        draw.polygon([(cx - s * .32, cy + s * .05), (cx - s * .08, cy - s * .30), (cx + s * .02, cy + s * .02)], fill=dark)
        draw.polygon([(cx + s * .08, cy + s * .04), (cx + s * .38, cy - s * .24), (cx + s * .28, cy + s * .14)], fill=dark)
        draw.ellipse((cx + s * .18, cy - s * .30, cx + s * .40, cy - s * .10), fill=dark)
    elif symbol == "lion":
        draw.ellipse((cx - s * .24, cy - s * .10, cx + s * .18, cy + s * .24), fill=accent)
        draw.ellipse((cx + s * .06, cy - s * .34, cx + s * .34, cy - s * .08), fill=accent)
        draw.arc((cx - s * .44, cy - s * .28, cx - s * .10, cy + s * .26), 210, 80, fill=accent, width=width)
        draw.line((cx - s * .06, cy + s * .18, cx - s * .25, cy + s * .42), fill=accent, width=width)
        draw.line((cx + s * .14, cy + s * .18, cx + s * .32, cy + s * .40), fill=accent, width=width)
    elif symbol == "scales":
        draw.line((cx, cy - s * .36, cx, cy + s * .34), fill=accent, width=width)
        draw.line((cx - s * .38, cy - s * .15, cx + s * .38, cy - s * .15), fill=accent, width=width)
        for sign in (-1, 1):
            bx = cx + sign * s * .28
            draw.arc((bx - s * .16, cy + s * .02, bx + s * .16, cy + s * .19), 0, 180, fill=accent, width=width)
            draw.line((bx, cy - s * .15, bx - sign * s * .08, cy + s * .05), fill=accent, width=max(2, width // 2))
            draw.line((bx, cy - s * .15, bx + sign * s * .08, cy + s * .05), fill=accent, width=max(2, width // 2))
    elif symbol == "tower":
        draw.rectangle((cx - s * .22, cy - s * .24, cx + s * .22, cy + s * .34), outline=accent, width=width)
        for offset in (-.20, 0, .20):
            draw.rectangle((cx + offset * s - s * .06, cy - s * .38, cx + offset * s + s * .06, cy - s * .24), fill=accent)
    elif symbol == "tree":
        draw.line((cx, cy + s * .32, cx, cy - s * .10), fill=accent, width=width)
        draw.ellipse((cx - s * .34, cy - s * .32, cx + s * .08, cy + s * .04), outline=accent, width=width)
        draw.ellipse((cx - s * .06, cy - s * .24, cx + s * .36, cy + s * .10), outline=accent, width=width)
    elif symbol == "raven":
        draw.pieslice((cx - s * .40, cy - s * .24, cx + s * .36, cy + s * .36), 205, 355, fill=dark)
        draw.polygon([(cx + s * .18, cy - s * .02), (cx + s * .46, cy - s * .12), (cx + s * .24, cy + s * .08)], fill=dark)
    elif symbol == "star":
        pts = []
        for i in range(10):
            ang = -math.pi / 2 + i * math.pi / 5
            radius = s * .42 if i % 2 == 0 else s * .18
            pts.append((cx + math.cos(ang) * radius, cy + math.sin(ang) * radius))
        draw.polygon(pts, fill=accent)
    elif symbol == "hammer":
        draw.line((cx - s * .30, cy + s * .30, cx + s * .20, cy - s * .24), fill=accent, width=width)
        draw.line((cx + s * .30, cy + s * .30, cx - s * .20, cy - s * .24), fill=accent, width=width)
        draw.rectangle((cx + s * .10, cy - s * .34, cx + s * .34, cy - s * .22), fill=accent)
        draw.rectangle((cx - s * .34, cy - s * .34, cx - s * .10, cy - s * .22), fill=accent)
    elif symbol == "sun":
        for angle in range(0, 360, 45):
            a = math.radians(angle)
            draw.line((cx + math.cos(a) * s * .22, cy + math.sin(a) * s * .22, cx + math.cos(a) * s * .40, cy + math.sin(a) * s * .40), fill=accent, width=max(2, width // 2))
        draw.ellipse((cx - s * .18, cy - s * .18, cx + s * .18, cy + s * .18), outline=accent, width=width)
    elif symbol == "rose":
        for angle in range(0, 360, 72):
            a = math.radians(angle)
            ex, ey = cx + math.cos(a) * s * .16, cy + math.sin(a) * s * .16
            draw.ellipse((ex - s * .14, ey - s * .09, ex + s * .14, ey + s * .09), fill=accent)
        draw.ellipse((cx - s * .08, cy - s * .08, cx + s * .08, cy + s * .08), fill=dark)
    elif symbol == "wheat":
        draw.line((cx, cy + s * .34, cx, cy - s * .30), fill=accent, width=width)
        for i in range(4):
            yy = cy + s * .15 - i * s * .12
            draw.line((cx, yy, cx - s * .20, yy - s * .10), fill=accent, width=max(2, width // 2))
            draw.line((cx, yy, cx + s * .20, yy - s * .10), fill=accent, width=max(2, width // 2))
    elif symbol == "anchor":
        draw.line((cx, cy - s * .34, cx, cy + s * .26), fill=accent, width=width)
        draw.ellipse((cx - s * .10, cy - s * .42, cx + s * .10, cy - s * .22), outline=accent, width=width)
        draw.arc((cx - s * .34, cy - s * .04, cx + s * .34, cy + s * .42), 20, 160, fill=accent, width=width)


def draw_shield(draw, country):
    cx, cy = country["shield"]
    size = 58 if country["size"] == "hero" else 42
    width, height = size, int(size * 1.18)
    accent = (220, 183, 104, 255)
    pts = shield_points(cx, cy, width, height)
    draw.polygon([(x + 3, y + 4) for x, y in pts], fill=(8, 7, 6, 150))
    draw.polygon(pts, fill=(29, 24, 20, 255))
    inner = shield_points(cx, cy, width * .84, height * .84)
    draw.polygon(inner, fill=country["color"] + (255,))
    draw.line(inner + [inner[0]], fill=accent, width=2)
    dark = (18, 15, 12, 255) if country["symbol"] in ("dragon", "raven") else accent
    draw_symbol(draw, country["symbol"], cx, cy + 2, size * .54, accent, dark)


def text_with_shadow(draw, xy, text, font, fill, anchor="mm", stroke=2):
    draw.text(xy, text, font=font, anchor=anchor, fill=fill, stroke_width=stroke, stroke_fill=(20, 15, 12, 220))


def draw_small_shield(draw, cx, cy, color, symbol):
    country = dict(shield=(cx, cy), color=color, symbol=symbol, size="small")
    draw_shield(draw, country)


img = Image.open(BASE).convert("RGBA")
overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay)

# Title block, kept lighter than the sample so the art still breathes.
text_with_shadow(draw, (74, 65), "ทวีปอาเรเซีย", f(THAI_BOLD, 34), (242, 218, 170, 255), anchor="lm", stroke=2)
text_with_shadow(draw, (76, 105), "(ARESIA CONTINENT)", f(SERIF_BOLD, 22), (235, 206, 155, 255), anchor="lm", stroke=2)
draw.line((72, 123, 305, 123), fill=(187, 139, 72, 210), width=2)

# Side panel content to match the atlas feel of the reference image.
panel_x = 50
draw.text((panel_x + 24, 182), "MAJOR POWERS", font=f(SERIF_BOLD, 18), fill=(60, 39, 22, 255), anchor="lm")
major_entries = [
    ("Eryndor Empire", (122, 29, 24), "dragon"),
    ("Kingdom of Lacoss", (29, 70, 130), "lion"),
    ("Kingdom of Velmora", (20, 106, 135), "scales"),
    ("Aetherion Kingdom", (77, 91, 109), "tower"),
    ("Republic of Varelia", (61, 110, 57), "anchor"),
]
entry_y = 225
for name, color, symbol in major_entries:
    draw_small_shield(draw, panel_x + 28, entry_y, color, symbol)
    draw.text((panel_x + 56, entry_y - 7), name, font=f(SERIF_BOLD, 15), fill=(62, 43, 27, 255))
    entry_y += 52

draw.line((panel_x + 20, 498, panel_x + 226, 498), fill=(111, 74, 39, 160), width=1)
draw.text((panel_x + 24, 526), "LEGEND", font=f(SERIF_BOLD, 18), fill=(60, 39, 22, 255), anchor="lm")
legend_rows = ["Capital", "Mountains", "Forest", "Sea"]
legend_y = 560
for i, label in enumerate(legend_rows):
    icon_x = panel_x + 28
    if i == 0:
        points = []
        for j in range(10):
            angle = -math.pi / 2 + j * math.pi / 5
            radius = 9 if j % 2 == 0 else 4
            points.append((icon_x + math.cos(angle) * radius, legend_y + math.sin(angle) * radius))
        draw.polygon(points, fill=(72, 48, 27, 255))
    elif i == 1:
        draw.polygon([(icon_x - 10, legend_y + 7), (icon_x, legend_y - 9), (icon_x + 10, legend_y + 7)], fill=(72, 48, 27, 255))
    elif i == 2:
        draw.line((icon_x, legend_y + 8, icon_x, legend_y - 6), fill=(72, 48, 27, 255), width=3)
        draw.ellipse((icon_x - 9, legend_y - 11, icon_x + 2, legend_y), outline=(72, 48, 27, 255), width=2)
        draw.ellipse((icon_x - 2, legend_y - 8, icon_x + 9, legend_y + 3), outline=(72, 48, 27, 255), width=2)
    else:
        draw.arc((icon_x - 14, legend_y - 5, icon_x + 2, legend_y + 9), 180, 360, fill=(72, 48, 27, 255), width=2)
        draw.arc((icon_x - 1, legend_y - 5, icon_x + 15, legend_y + 9), 180, 360, fill=(72, 48, 27, 255), width=2)
    draw.text((panel_x + 56, legend_y - 8), label, font=f(SERIF, 15), fill=(62, 43, 27, 255))
    legend_y += 34

# Main country crests and labels.
for country in COUNTRIES:
    draw_shield(draw, country)
    font = f(SERIF_BOLD, 28 if country["size"] == "hero" else 18)
    text_with_shadow(draw, country["xy"], country["name"], font, (245, 226, 186, 255), stroke=2)

# Compact capital stars for a more atlas-like feel.
for x, y in [(708, 382), (598, 726), (620, 593), (842, 624), (663, 1037)]:
    text_with_shadow(draw, (x, y), "★", f(SERIF_BOLD, 16), (226, 185, 95, 255), stroke=1)

img = Image.alpha_composite(img, overlay)
img = img.filter(ImageFilter.UnsharpMask(radius=1.0, percent=85, threshold=4))
rgb = img.convert("RGB")
rgb.save(OUT_PNG, "PNG")
rgb.save(OUT_WEBP, "WEBP", quality=95, method=6)
print(OUT_PNG)
