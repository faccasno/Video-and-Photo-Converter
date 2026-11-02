import subprocess
import os
import sys
import shutil

def get_resource_path(relative_path):
    """
    Возвращает абсолютный путь к ресурсу.
    Работает и при обычном запуске, и когда программа упакована в --onefile exe.
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def convert_video(input_file, output_format="mp4", output_path=None):
    """
    Конвертирует видео.
    Сохраняет результат рядом с исходным файлом (или в указанную папку),
    а не во временную папку PyInstaller.
    """
    
    # 1. Находим ffmpeg (работает и внутри exe, и снаружи)
    ffmpeg_exe = get_resource_path(os.path.join("bin", "ffmpeg.exe"))
    if not os.path.exists(ffmpeg_exe):
        raise FileNotFoundError(f"Не найден ffmpeg.exe! Путь: {ffmpeg_exe}")

    # 2. Определяем папку для сохранения
    input_dir = os.path.dirname(os.path.abspath(input_file))
    
    if output_path is None:
        save_dir = input_dir
    else:
        save_dir = output_path

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # 3. Формируем имя выходного файла
    file_name = os.path.basename(input_file)
    
    # ПРАВИЛЬНОЕ получение расширения
    # splitext возвращает кортеж (имя_без_расширения, расширение)
    name_without_ext, input_ext = os.path.splitext(file_name)
    input_ext = input_ext.lower()  # Приводим к нижнему регистру
    
    target_ext = "." + output_format.lower()
    
    # Если формат совпадает с исходным, добавляем суффикс, чтобы не затереть оригинал
    if input_ext == target_ext:
        output_filename = f"{name_without_ext}_converted.{output_format}"
    else:
        output_filename = f"{name_without_ext}.{output_format}"
        
    output_full_path = os.path.join(save_dir, output_filename)

    # 4. Команда FFmpeg
    command = [
        ffmpeg_exe,
        "-y",
        "-i", input_file,
        "-c:v", "libx264",
        "-preset", "fast",
        "-c:a", "aac",
        "-b:a", "192k",
        output_full_path
    ]

    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return output_full_path
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.decode('utf-8', errors='ignore')
        raise RuntimeError(f"Ошибка конвертации FFmpeg:\n{error_msg}")
    except FileNotFoundError:
        raise FileNotFoundError("ffmpeg.exe не найден.")

def convert_image(input_file, output_format="jpg"):
    """Конвертация фото через Pillow"""
    from PIL import Image
    
    script_dir = os.path.dirname(os.path.abspath(input_file)) # Сохраняем рядом с оригиналом
    
    fmt = output_format.lower()
    if fmt == "jpeg":
        fmt = "jpg"

    input_name = os.path.splitext(os.path.basename(input_file))[0]
    output_filename = f"{input_name}_converted.{fmt}"
    output_path = os.path.join(script_dir, output_filename)

    try:
        with Image.open(input_file) as img:
            if fmt == "png":
                img.save(output_path, format="PNG")
            elif fmt == "gif":
                img = img.convert("RGB").convert("P", palette=Image.Palette.ADAPTIVE)
                img.save(output_path, format="GIF", optimize=True)
            else:
                if img.mode in ("RGBA", "LA"):
                    background = Image.new("RGB", img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1])
                    img = background
                
                if fmt == "webp":
                    img.save(output_path, format="WEBP", quality=80)
                else:
                    img.save(output_path, format="JPEG", quality=90)
        return output_path
    except Exception as e:
        raise RuntimeError(f"Ошибка конвертации фото: {str(e)}")
