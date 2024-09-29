import base64
from PIL import Image
from io import BytesIO


def preprocess_image(image: Image.Image) -> str:
    """
    Preprocess the image for GPT analysis.
    Resize the image and convert it to a base64 encoded string.
    """
    # Resize the image to a standard size
    width, height = image.size
    image_size_bytes = width * height * 3
    if image_size_bytes / (1024**2) >= 20:
        return "Image size exceeds 20MB. Please upload an image with a smaller size."
    # Convert the Image object to a BytesIO object
    buffered = BytesIO()
    image.save(buffered,
               format="PNG")  # Save image to the buffer in PNG format
    buffered.seek(0)  # Reset buffer pointer to the beginning
    # Encode the BytesIO content to base64
    img_str = base64.b64encode(buffered.read()).decode('utf-8')
    return img_str
