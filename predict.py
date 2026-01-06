import replicate
from PIL import Image
import io
import base64

class Predictor:
    def predict(self, image: str):
        """
        image: base64 encoded image
        """

        image_bytes = base64.b64decode(image)
        img = Image.open(io.BytesIO(image_bytes))

        output = replicate.run(
            "dallibrand/background-removal",
            input={"image": img}
        )

        return output
