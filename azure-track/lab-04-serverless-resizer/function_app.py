import io
import logging
import os

import azure.functions as func
from azure.storage.blob import BlobServiceClient, ContentSettings
from PIL import Image, ImageOps, UnidentifiedImageError

app = func.FunctionApp()
Image.MAX_IMAGE_PIXELS = 200_000_000
THUMB_WIDTH = 200
JPEG_QUALITY = 85

FORMAT_MAP = {
    "JPEG": ("JPEG", "image/jpeg", ".jpg"),
    "PNG": ("PNG", "image/png", ".png"),
    "WEBP": ("WEBP", "image/webp", ".webp"),
    "GIF": ("JPEG", "image/jpeg", ".jpg"),
    "BMP": ("JPEG", "image/jpeg", ".jpg"),
    "TIFF": ("JPEG", "image/jpeg", ".jpg"),
}

@app.function_name(name="resize_image")
@app.blob_trigger(
    arg_name="input_blob",
    path="uploads/{name}",
    connection="AzureWebJobsStorage",
)
def resize_image(input_blob: func.InputStream):
    logging.info("Processing %s (%s bytes)", input_blob.name, input_blob.length)
    try:
        image = Image.open(io.BytesIO(input_blob.read()))
        input_format = image.format
        image = ImageOps.exif_transpose(image)
        output_format, content_type, extension = FORMAT_MAP.get(
            input_format, ("JPEG", "image/jpeg", ".jpg")
        )
        image = convert_mode(image, output_format)
        width, height = image.size
        if width > THUMB_WIDTH:
            new_height = round(height * THUMB_WIDTH / width)
            image = image.resize(
                (THUMB_WIDTH, new_height), Image.Resampling.LANCZOS
            )

        output = io.BytesIO()
        options = {"format": output_format, "optimize": True}
        if output_format == "JPEG":
            options["quality"] = JPEG_QUALITY
        image.save(output, **options)
        output.seek(0)

        base = os.path.splitext(os.path.basename(input_blob.name))[0]
        output_name = f"{base}{extension}"
        service = BlobServiceClient.from_connection_string(
            os.environ["AzureWebJobsStorage"]
        )
        target = service.get_blob_client(
            container="thumbnails", blob=output_name
        )
        target.upload_blob(
            output,
            overwrite=True,
            content_settings=ContentSettings(content_type=content_type),
        )
        logging.info("Thumbnail written: thumbnails/%s", output_name)
    except UnidentifiedImageError:
        logging.warning("Skipped unsupported image: %s", input_blob.name)
    except Exception:
        logging.exception("Processing failed: %s", input_blob.name)
        raise

def convert_mode(image, output_format):
    if output_format == "JPEG":
        if image.mode in ("RGBA", "LA"):
            background = Image.new("RGB", image.size, (255, 255, 255))
            background.paste(image, mask=image.getchannel("A"))
            return background
        if image.mode == "P":
            image = image.convert("RGBA")
            background = Image.new("RGB", image.size, (255, 255, 255))
            background.paste(image, mask=image.getchannel("A"))
            return background
        if image.mode != "RGB":
            return image.convert("RGB")
    if output_format == "PNG" and image.mode == "CMYK":
        return image.convert("RGB")
    if output_format == "WEBP" and image.mode == "P":
        return image.convert("RGBA")
    if output_format == "WEBP" and image.mode == "CMYK":
        return image.convert("RGB")
    return image