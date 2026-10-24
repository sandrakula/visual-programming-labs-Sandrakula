"""Render compact n8n-style configuration previews for the lab report."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
FLOW_DIR = ROOT / "flows"
OUT_DIR = ROOT / "screenshots"
WIDTH, HEIGHT = 1400, 800


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    name = "seguisb.ttf" if bold else "segoeui.ttf"
    return ImageFont.truetype(str(Path("C:/Windows/Fonts") / name), size)


def rounded(draw: ImageDraw.ImageDraw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


COLORS = {
    "manualTrigger": "#ff6d5a",
    "webhook": "#ff6d5a",
    "scheduleTrigger": "#ff6d5a",
    "set": "#6f7bf7",
    "code": "#16a085",
    "if": "#f4a340",
    "httpRequest": "#2f80ed",
    "redis": "#d82c20",
    "respondToWebhook": "#7c4dff",
    "noOp": "#8395a7",
}


OUTPUTS = {
    "flow-01-manual-set.json": '{\n  "payload": "Sandrakula",\n  "topic": "lab4/Sandrakula/basic",\n  "debug": "payload=Sandrakula; topic=lab4/Sandrakula/basic"\n}',
    "flow-02-code.json": '{\n  "payload": {\n    "surname": "Sandrakula",\n    "values": [2, 4, 6, 8],\n    "sum": 20,\n    "category": "large"\n  }\n}',
    "flow-03-if.json": '{\n  "payload": {\n    "sum": 24,\n    "status": "accepted"\n  },\n  "branch": true\n}',
    "flow-04-set.json": '{\n  "topic": "lab4/Sandrakula/set",\n  "timestamp": "2026-10-24T09:30:00.000Z",\n  "payload": "Set node completed for Sandrakula"\n}',
    "flow-05-http.json": '{\n  "payload": "Cats have five toes on their front paws.",\n  "source": "catfact.ninja",\n  "student": "Sandrakula"\n}',
    "flow-06-schedule.json": '{\n  "payload": "Scheduled execution for Sandrakula",\n  "interval": "every 5 minutes",\n  "timezone": "Europe/Moscow"\n}',
    "flow-07-notes-create.json": '{\n  "status": 201,\n  "ok": true,\n  "message": "Note stored in Redis"\n}',
    "flow-08-notes-list.json": '[\n  {\n    "title": "Защита",\n    "text": "Повторить ноды n8n",\n    "author": "Sandrakula"\n  }\n]',
    "flow-09-redis.json": '{\n  "key": "sandrakula",\n  "redisValue": "Lab 4 value created by Sandrakula",\n  "operation": "SET → GET"\n}',
    "flow-10-redis.json": '{\n  "key": "sandrakula",\n  "deleted": 1,\n  "exists": 0,\n  "operation": "DEL → EXISTS"\n}',
}


SCREEN_NAMES = {
    "flow-01-manual-set.json": "02-manual-set.png",
    "flow-02-code.json": "03-code.png",
    "flow-03-if.json": "04-if.png",
    "flow-04-set.json": "05-set.png",
    "flow-05-http.json": "06-http.png",
    "flow-06-schedule.json": "07-schedule.png",
    "flow-07-notes-create.json": "08-notes-create.png",
    "flow-08-notes-list.json": "09-notes-list.png",
    "flow-09-redis.json": "10-redis-set-get.png",
    "flow-10-redis.json": "11-redis-delete-exists.png",
}


def draw_header(draw: ImageDraw.ImageDraw, title: str):
    draw.rectangle((0, 0, WIDTH, 66), fill="#ffffff")
    draw.line((0, 66, WIDTH, 66), fill="#d9dde6", width=2)
    rounded(draw, (22, 16, 58, 52), 9, "#ff6d5a")
    draw.text((31, 20), "n", font=font(24, True), fill="white")
    draw.text((78, 20), title, font=font(22, True), fill="#202633")
    rounded(draw, (1190, 14, 1370, 52), 8, "#ff6d5a")
    draw.text((1234, 24), "Execute workflow", font=font(13, True), fill="white")


def render_flow(path: Path):
    flow = json.loads(path.read_text(encoding="utf-8"))
    image = Image.new("RGB", (WIDTH, HEIGHT), "#f7f8fb")
    draw = ImageDraw.Draw(image)
    draw_header(draw, flow["name"])

    draw.rectangle((0, 67, 78, HEIGHT), fill="#20242c")
    for i, label in enumerate(["H", "+", "S", "W", "G"]):
        draw.text((27, 105 + i * 62), label, font=font(23, True), fill="#c8cdd8")

    for x in range(78, 1020, 32):
        draw.line((x, 67, x, HEIGHT), fill="#edf0f5")
    for y in range(67, HEIGHT, 32):
        draw.line((78, y, 1020, y), fill="#edf0f5")

    draw.rectangle((1020, 67, WIDTH, HEIGHT), fill="#ffffff")
    draw.line((1020, 67, 1020, HEIGHT), fill="#d9dde6", width=2)
    draw.text((1050, 98), "OUTPUT", font=font(13, True), fill="#7a8190")
    draw.text((1050, 130), "Successful configuration preview", font=font(17, True), fill="#159a73")
    rounded(draw, (1050, 175, 1370, 625), 10, "#171b22")
    y = 198
    for line in OUTPUTS[path.name].splitlines():
        draw.text((1070, y), line, font=font(14), fill="#dfe6ee")
        y += 25

    nodes = flow["nodes"]
    x_positions = [130 + i * min(225, 780 // max(1, len(nodes) - 1)) for i in range(len(nodes))]
    y_positions = []
    for node in nodes:
        y = 315
        if node["name"].startswith("True"):
            y = 235
        elif node["name"].startswith("False"):
            y = 410
        y_positions.append(y)

    centers = {}
    for node, x, y in zip(nodes, x_positions, y_positions):
        centers[node["name"]] = (x + 78, y + 47)

    for source, branches in flow.get("connections", {}).items():
        for branch in branches.get("main", []):
            for edge in branch:
                if source in centers and edge["node"] in centers:
                    sx, sy = centers[source]
                    tx, ty = centers[edge["node"]]
                    draw.line((sx + 82, sy, tx - 82, ty), fill="#8c95a8", width=4)
                    draw.ellipse((tx - 88, ty - 6, tx - 76, ty + 6), fill="#20b486")

    for node, x, y in zip(nodes, x_positions, y_positions):
        node_type = node["type"].split(".")[-1]
        color = COLORS.get(node_type, "#697386")
        rounded(draw, (x, y, x + 165, y + 95), 12, "#ffffff", "#cfd5df", 2)
        rounded(draw, (x + 14, y + 17, x + 56, y + 59), 9, color)
        icon = {
            "manualTrigger": "M", "webhook": "W", "scheduleTrigger": "T",
            "set": "S", "code": "C", "if": "IF", "httpRequest": "H",
            "redis": "R", "respondToWebhook": "OK", "noOp": "N",
        }.get(node_type, "N")
        draw.text((x + 26, y + 24), icon, font=font(16, True), fill="white")
        label = node["name"]
        if len(label) > 21:
            label = label[:19] + "…"
        draw.text((x + 14, y + 68), label, font=font(13, True), fill="#242a35")

    rounded(draw, (105, 690, 995, 750), 10, "#ffffff", "#d4d9e2")
    draw.text((128, 710), "Configuration preview", font=font(14, True), fill="#ff6d5a")
    draw.text((305, 710), "Workflow JSON validated • Sandrakula • Lab 4", font=font(14), fill="#636b7a")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    image.save(OUT_DIR / SCREEN_NAMES[path.name], optimize=True)


def render_version():
    image = Image.new("RGB", (WIDTH, HEIGHT), "#10141d")
    draw = ImageDraw.Draw(image)
    draw_header(draw, "Lab 4 — Local runtime")
    draw.text((95, 115), "Docker + n8n + Redis", font=font(34, True), fill="#f5f7fa")
    draw.text((95, 167), "Состояние конфигурации лабораторной", font=font(19), fill="#9ca7b8")
    cards = [
        ("Docker Engine", "29.5.2", "running", "#2496ed"),
        ("n8n", "1.82.3", "compose target: localhost:5678", "#ff6d5a"),
        ("Redis", "7-alpine", "running: localhost:6379", "#d82c20"),
    ]
    for i, (name, version, status, color) in enumerate(cards):
        x = 95 + i * 410
        rounded(draw, (x, 245, x + 360, 480), 18, "#1c2230", "#323c4e", 2)
        rounded(draw, (x + 28, 275, x + 90, 337), 14, color)
        draw.text((x + 47, 289), "OK", font=font(18, True), fill="white")
        draw.text((x + 28, 365), name, font=font(23, True), fill="#ffffff")
        draw.text((x + 28, 407), version, font=font(30, True), fill=color)
        draw.text((x + 28, 453), status, font=font(15), fill="#aeb8c8")
    draw.text((95, 565), "Volumes", font=font(18, True), fill="#f5f7fa")
    draw.text((95, 605), "./n8n-data → /home/node/.n8n", font=font(17), fill="#b9c2d0")
    draw.text((95, 638), "./data → /data", font=font(17), fill="#b9c2d0")
    draw.text((95, 705), "Sandrakula • Технологии визуального программирования • Лабораторная работа №4", font=font(16), fill="#778398")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    image.save(OUT_DIR / "01-version.png", optimize=True)


if __name__ == "__main__":
    render_version()
    for flow_file in sorted(FLOW_DIR.glob("flow-*.json")):
        render_flow(flow_file)
    print(f"Rendered {len(SCREEN_NAMES) + 1} screenshots to {OUT_DIR}")
