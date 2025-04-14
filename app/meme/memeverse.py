from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
from PIL import Image, ImageDraw, ImageFont
from transformers import pipeline, set_seed
import os
import uuid

router = APIRouter()

# Inicializa o modelo
gerador = pipeline("text-generation", model="pierreguillou/gpt2-small-portuguese")
set_seed(42)

os.makedirs("uploaded_images", exist_ok=True)
os.makedirs("generated_memes", exist_ok=True)

@router.post("/")
async def criar_meme(imagem: UploadFile = File(...), frase: str = Form(...)):
    prompt = f"Crie uma legenda engraçada para um meme com a frase: {frase}"
    resultado = gerador(prompt, max_length=60, num_return_sequences=1)
    legenda = resultado[0]["generated_text"].split(":")[-1].strip()

    nome_arquivo = f"{uuid.uuid4().hex[:8]}_{imagem.filename}"
    caminho_entrada = os.path.join("uploaded_images", nome_arquivo)
    with open(caminho_entrada, "wb") as f:
        f.write(await imagem.read())

    img = Image.open(caminho_entrada).convert("RGB")
    draw = ImageDraw.Draw(img)

    try:
        fonte = ImageFont.truetype("DejaVuSans-Bold.ttf", size=int(img.width * 0.05))
    except:
        fonte = ImageFont.load_default()

    palavras = legenda.split()
    linhas, linha = [], ""
    for palavra in palavras:
        if fonte.getlength(linha + " " + palavra) < img.width - 40:
            linha += " " + palavra
        else:
            linhas.append(linha)
            linha = palavra
    linhas.append(linha)

    altura_texto = len(linhas) * int(fonte.size * 1.2)
    y = img.height - altura_texto - 20

    for l in linhas:
        texto = l.strip()
        largura_texto = fonte.getlength(texto)
        x = (img.width - largura_texto) / 2
        for dx in [-1, 1]:
            for dy in [-1, 1]:
                draw.text((x + dx, y + dy), texto, font=fonte, fill="black")
        draw.text((x, y), texto, font=fonte, fill="white")
        y += int(fonte.size * 1.2)

    nome_meme = f"meme_{uuid.uuid4().hex[:8]}.jpg"
    caminho_saida = os.path.join("generated_memes", nome_meme)
    img.save(caminho_saida)

    return {
        "mensagem_gerada": legenda,
        "url_meme": f"/criar-meme/meme/{nome_meme}"
    }

@router.get("/meme/{filename}")
def servir_meme(filename: str):
    caminho = os.path.join("generated_memes", filename)
    if os.path.exists(caminho):
        return FileResponse(caminho, media_type="image/jpeg")
    return {"erro": "Meme não encontrado"}

  