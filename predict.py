from cog import BasePredictor, Input, Path
from PIL import Image, ImageDraw, ImageFont
import os

class Predictor(BasePredictor):
    def setup(self):
        # Nessun modello pesante — solo Pillow
        pass

    def predict(
        self,
        width: int = Input(description="Width of the image", ge=1, le=4096, default=512),
        height: int = Input(description="Height of the image", ge=1, le=4096, default=512),
        text: str = Input(description="Text to display", default="PLACEHOLDER"),
        color: str = Input(description="Background color in hex (e.g. #FF0000)", default="#E0E0E0"),
        text_color: str = Input(description="Text color in hex", default="#000000")
    ) -> Path:
        # Crea immagine
        img = Image.new("RGB", (width, height), color)
        draw = ImageDraw.Draw(img)

        # Carica un font (usa font di sistema o fallback)
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size=max(20, int(height * 0.15)))
        except:
            font = ImageFont.load_default()

        # Calcola posizione testo centrato
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (width - text_width) // 2
        y = (height - text_height) // 2

        # Disegna testo
        draw.text((x, y), text, fill=text_color, font=font)

        # Salva
        output_path = "/tmp/output.png"
        img.save(output_path)
        return Path(output_path)
