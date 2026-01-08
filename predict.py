from cog import BasePredictor, Input, Path
from PIL import Image
from rembg import remove

class Predictor(BasePredictor):
    def setup(self):
        pass

    def predict(
        self,
        image: Path = Input(description="Upload a portrait, product, or object photo"),
        format: str = Input(choices=["png", "jpg"], default="png", description="Output format (PNG with transparency or JPG with white background)"),
        background_color: str = Input(default="#FFFFFF", description="Background color in hex (used only for JPG)")
    ) -> Path:
        input_img = Image.open(str(image)).convert("RGB")
        output_img = remove(input_img)

        output_path = "/tmp/output.png"
        if format == "png":
            output_img.save(output_path, "PNG")
        else:
            r = int(background_color[1:3], 16)
            g = int(background_color[3:5], 16)
            b = int(background_color[5:7], 16)
            bg = Image.new("RGB", output_img.size, (r, g, b))
            bg.paste(output_img, mask=output_img.split()[-1])
            bg.save("/tmp/output.jpg", "JPEG", quality=95)
            output_path = "/tmp/output.jpg"

        return Path(output_path)
