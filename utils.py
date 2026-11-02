import os
from pathlib import Path

# Расширенные списки расширений
IMAGE_EXTS = {
    ".jpg", ".jpeg", ".png", ".bmp", ".webp", ".gif",
    ".tiff", ".tif", ".ico", ".pbm", ".pgm", ".ppm", ".xbm"
}

VIDEO_EXTS = {
    ".mp4", ".mov", ".avi", ".mkv", ".webm", ".flv",
    ".wmv", ".m4v", ".mpg", ".mpeg", ".ts", ".mts",
    ".3gp", ".ogv", ".rmvb"
}

def get_extension(path: str) -> str:
    return Path(path).suffix.lower()

def make_output_path(input_path: str, new_ext: str) -> str:
    p = Path(input_path)
    return str(p.with_suffix(new_ext))

def is_image(path: str) -> bool:
    ext = get_extension(path)
    return ext in IMAGE_EXTS

def is_video(path: str) -> bool:
    ext = get_extension(path)
    return ext in VIDEO_EXTS
