from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os
import uuid

def get_font_size(draw, frase, image_width, max_width_ratio=0.9):
    font_size = 80
    font_path = "" 
    if not os.path.exists(font_path):
        font_path = None  # Usa fonte padrão do PIL

    while font_size > 50:
        font = ImageFont.truetype(font_path, font_size) if font_path else ImageFont.load_default()
        bbox = draw.textbbox((0, 0), frase, font=font)
        text_width = bbox[2] - bbox[0]
        if text_width <= image_width * max_width_ratio:
            return font
        font_size -= 1

    return ImageFont.truetype(font_path, 12) if font_path else ImageFont.load_default()

def generate_meme(caminho_imagem, frase, posicao):
    image = Image.open(BytesIO(caminho_imagem)).convert("RGB")
    draw = ImageDraw.Draw(image)

    font = get_font_size(draw, frase, image.width)

    bbox = draw.textbbox((0, 0), frase, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    w, h = image.size

    positions = {
        "topo": (w // 2 - text_width // 2, 10),
        "centro": (w // 2 - text_width // 2, h // 2 - text_height // 2),
        "base": (w // 2 - text_width // 2, h - text_height - 10),
    }

    coords = positions.get(posicao, positions["topo"])

    draw.text(coords, frase, fill="white", font=font, stroke_width=2, stroke_fill="black")

    filename = f"{uuid.uuid4().hex}.jpg"
    path = os.path.join("static/memes", filename)
    os.makedirs("static/memes", exist_ok=True)
    image.save(path)

    return path
