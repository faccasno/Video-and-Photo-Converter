from PIL import Image
from utils import make_output_path

SUPPORTED_IMAGE_FORMATS = {
    "jpg": "JPEG",
    "jpeg": "JPEG",
    "png": "PNG",
    "bmp": "BMP",
    "webp": "WEBP",
    "gif": "GIF",
    "tiff": "TIFF",
    "tif": "TIFF",
    "ico": "ICO",
    "pbm": "PPM",      # Pillow конвертирует PBM/PGM/PPM через PPM
    "pgm": "PPM",
    "ppm": "PPM",
    "xbm": "XBM"
}

def convert_image(input_path: str, output_format: str) -> str:
    fmt = output_format.lower()
    if fmt not in SUPPORTED_IMAGE_FORMATS:
        raise ValueError(f"Неподдерживаемый формат изображения: {fmt}")

    output_path = make_output_path(input_path, "." + fmt)

    with Image.open(input_path) as img:
        # Для форматов без альфа-канала конвертируем в RGB
        if fmt in ("jpg", "jpeg", "bmp"):
            img = img.convert("RGB")

        save_fmt = SUPPORTED_IMAGE_FORMATS[fmt]
        if fmt in ("jpg", "jpeg"):
            # Можно менять качество: 1–95, 85 — хороший баланс
            img.save(output_path, format=save_fmt, quality=85, optimize=True)
        elif fmt == "webp":
            img.save(output_path, format=save_fmt, quality=80, lossless=False)
        else:
            img.save(output_path, format=save_fmt)

    return output_path
