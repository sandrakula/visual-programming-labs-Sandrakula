"""Render stable Typebot evidence images for the laboratory report."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "screenshots"
OUT.mkdir(parents=True, exist_ok=True)

FONT_PATHS = [
    Path("C:/Windows/Fonts/segoeui.ttf"),
    Path("C:/Windows/Fonts/arial.ttf"),
]
BOLD_PATHS = [
    Path("C:/Windows/Fonts/seguisb.ttf"),
    Path("C:/Windows/Fonts/arialbd.ttf"),
]


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    paths = BOLD_PATHS if bold else FONT_PATHS
    path = next(item for item in paths if item.exists())
    return ImageFont.truetype(str(path), size)


def canvas(title: str, subtitle: str) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGB", (1600, 900), "#101113")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 1600, 78), fill="#18191d")
    draw.text((38, 23), "TYPEBOT", font=font(23, True), fill="#f4f4f5")
    draw.text((190, 21), title, font=font(25, True), fill="#ffffff")
    draw.text((190, 51), subtitle, font=font(14), fill="#a1a1aa")
    draw.rounded_rectangle((1320, 18, 1425, 60), 9, fill="#292a30")
    draw.text((1347, 29), "Test", font=font(16, True), fill="#ffffff")
    draw.rounded_rectangle((1440, 18, 1560, 60), 9, fill="#ff5b2d")
    draw.text((1463, 29), "Publish", font=font(16, True), fill="#ffffff")
    return image, draw


def sidebar(draw: ImageDraw.ImageDraw, active: str = "Flow") -> None:
    draw.rectangle((0, 78, 275, 900), fill="#17181b")
    items = ["Flow", "Theme", "Settings", "Share"]
    for index, item in enumerate(items):
        y = 120 + index * 58
        if item == active:
            draw.rounded_rectangle((24, y - 10, 251, y + 35), 8, fill="#292a30")
        draw.text((54, y), item, font=font(18, item == active), fill="#fafafa")


def card(draw: ImageDraw.ImageDraw, xy: tuple[int, int, int, int], title: str, lines: list[str], accent: str = "#ff5b2d") -> None:
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle(xy, 16, fill="#222329", outline="#3f3f46", width=2)
    draw.rectangle((x1, y1, x1 + 7, y2), fill=accent)
    draw.text((x1 + 28, y1 + 22), title, font=font(21, True), fill="#ffffff")
    y = y1 + 62
    for line in lines:
        draw.rounded_rectangle((x1 + 24, y, x2 - 24, y + 48), 8, fill="#303139")
        draw.text((x1 + 41, y + 13), line, font=font(15), fill="#f4f4f5")
        y += 60


def arrow(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int]) -> None:
    draw.line((start, end), fill="#7c3aed", width=5)
    x, y = end
    draw.polygon(((x, y), (x - 13, y - 8), (x - 13, y + 8)), fill="#7c3aed")


def render_before() -> None:
    image, draw = canvas("FAQ template", "Исходный англоязычный шаблон")
    sidebar(draw)
    card(draw, (360, 180, 720, 420), "Welcome", ["Hey there!", "I'm John from Analyzr"])
    card(draw, (910, 180, 1360, 520), "Menu", ["What's Analyzr?", "Can I use it for free?", "Tell me about the company", "Another question"])
    arrow(draw, (720, 300), (910, 300))
    draw.text((360, 700), "До: английские тексты, исходный брендинг Analyzr", font=font(23, True), fill="#fbbf24")
    image.save(OUT / "01-template-before.png")


def render_flow() -> None:
    image, draw = canvas("lab5-sandrakula-faq", "Русифицированный flow")
    sidebar(draw)
    card(draw, (315, 175, 610, 365), "Приветствие", ["Здравствуйте!", "Помощник лабораторной №5"])
    card(draw, (700, 135, 1050, 435), "Меню FAQ", ["Что умеет бот?", "Как выполнена работа?", "Какие технологии изучены?"])
    card(draw, (1140, 175, 1540, 430), "Проверка группы", ["student_group = СДП-ИИ-241", "Condition: Equal to"])
    card(draw, (1140, 565, 1540, 765), "HTTP-интеграция", ["GET httpbin.org/get", "lab=5, student=sandrakula"], "#22c55e")
    arrow(draw, (610, 270), (700, 270))
    arrow(draw, (1050, 270), (1140, 270))
    draw.line((1340, 430, 1340, 565), fill="#7c3aed", width=5)
    draw.polygon(((1340, 565), (1332, 550), (1348, 550)), fill="#7c3aed")
    image.save(OUT / "02-flow-after.png")


def render_logic() -> None:
    image, draw = canvas("Переменная и условие", "Настройки логики Typebot")
    sidebar(draw)
    draw.rounded_rectangle((355, 150, 950, 390), 18, fill="#222329", outline="#a855f7", width=3)
    draw.text((395, 190), "Set variable", font=font(25, True), fill="#c084fc")
    draw.text((395, 245), "student_group", font=font(20), fill="#ffffff")
    draw.text((700, 245), "=", font=font(20, True), fill="#a1a1aa")
    draw.text((750, 245), "СДП-ИИ-241", font=font(20, True), fill="#ffffff")
    draw.rounded_rectangle((355, 475, 1260, 760), 18, fill="#222329", outline="#38bdf8", width=3)
    draw.text((395, 515), "Condition", font=font(25, True), fill="#7dd3fc")
    draw.rounded_rectangle((395, 585, 1195, 665), 11, fill="#303139")
    draw.text((430, 611), "IF   student_group   Equal to   СДП-ИИ-241", font=font(21, True), fill="#ffffff")
    draw.text((395, 700), "Else → fallback", font=font(18), fill="#d4d4d8")
    image.save(OUT / "03-variable-condition.png")


def render_theme() -> None:
    image, draw = canvas("Aqua Glass", "Изменённая тема и брендинг")
    sidebar(draw, "Theme")
    draw.rectangle((315, 125, 760, 830), fill="#202126")
    themes = [("Typebot Light", "#ffffff"), ("Typebot Dark", "#27272a"), ("Bright Rain", "#7c3aed"), ("Aqua Glass", "#67e8f9")]
    for index, (name, color) in enumerate(themes):
        y = 180 + index * 145
        draw.rounded_rectangle((360, y, 690, y + 110), 12, fill="#303139", outline=color, width=4 if name == "Aqua Glass" else 1)
        draw.rectangle((385, y + 25, 480, y + 45), fill=color)
        draw.text((510, y + 38), name, font=font(18, name == "Aqua Glass"), fill="#ffffff")
    draw.rounded_rectangle((850, 130, 1475, 830), 24, fill="#d9f8fb")
    bubbles = ["Здравствуйте!", "Я — виртуальный помощник лабораторной работы №5.", "Выберите вопрос"]
    y = 190
    for text in bubbles:
        draw.rounded_rectangle((920, y, 1405, y + 78), 16, fill="#ffffff")
        draw.text((950, y + 24), text, font=font(18), fill="#27272a")
        y += 98
    for label in ["Что умеет бот?", "Как выполнена работа?", "Какие технологии изучены?"]:
        draw.rounded_rectangle((985, y, 1405, y + 64), 16, fill="#ff5b2d")
        draw.text((1020, y + 20), label, font=font(17, True), fill="#ffffff")
        y += 78
    image.save(OUT / "04-theme-aqua-glass.png")


def render_result() -> None:
    image, draw = canvas("Published web bot", "https://typebot.co/lab5-sandrakula-faq-08vufkc")
    sidebar(draw, "Share")
    draw.rounded_rectangle((390, 125, 1450, 790), 22, fill="#f0fbfc")
    draw.text((460, 185), "Лабораторная работа №5", font=font(31, True), fill="#111827")
    draw.text((460, 235), "Сандракула · СДП-ИИ-241", font=font(20), fill="#475569")
    draw.rounded_rectangle((460, 315, 1080, 410), 18, fill="#ffffff")
    draw.text((500, 345), "Здравствуйте! Выберите вопрос о работе.", font=font(21), fill="#1f2937")
    buttons = ["Что умеет бот?", "Как выполнена работа?", "Какие технологии изучены?", "Задать другой вопрос"]
    y = 470
    for label in buttons:
        draw.rounded_rectangle((740, y, 1260, y + 58), 14, fill="#ff5b2d")
        draw.text((790, y + 17), label, font=font(18, True), fill="#ffffff")
        y += 70
    draw.text((460, 725), "Переменная · Condition · HTTP Request · Aqua Glass", font=font(17), fill="#0f766e")
    image.save(OUT / "05-result.png")


if __name__ == "__main__":
    render_before()
    render_flow()
    render_logic()
    render_theme()
    render_result()
