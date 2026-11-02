import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from video_converter import convert_video, convert_image
import os

current_mode = "video"

def on_mode_change():
    global current_mode
    current_mode = var_mode.get()
    if current_mode == "video":
        combo_format.config(values=["mp4", "mov", "mkv", "avi"])
        lbl_desc.config(text="Конвертация видео: H.264 + AAC")
    else:
        combo_format.config(values=["jpg", "png", "webp", "gif"])
        lbl_desc.config(text="Конвертация фото: качество 80-90%")
    combo_format.current(0)

def on_convert_click():
    file_path = filedialog.askopenfilename(
        title="Выберите файл",
        filetypes=[
            ("Media files", "*.mp4 *.avi *.mov *.mkv *.wmv *.jpg *.png *.jpeg *.gif *.webp"),
            ("All files", "*.*")
        ]
    )
    if not file_path:
        return

    if not os.path.exists(file_path):
        messagebox.showerror("Ошибка", "Файл не найден!")
        return

    output_format = combo_format.get()
    if not output_format:
        output_format = "mp4" if current_mode == "video" else "jpg"

    btn_convert.config(state=tk.DISABLED)
    root.update()

    try:
        if current_mode == "video":
            result_path = convert_video(file_path, output_format)
            messagebox.showinfo("Успех", f"Видео конвертировано!\n\nПуть: {result_path}")
        else:
            result_path = convert_image(file_path, output_format)
            messagebox.showinfo("Успех", f"Фото конвертировано!\n\nПуть: {result_path}")
    except FileNotFoundError as e:
        msg = str(e)
        if "ffmpeg" in msg.lower():
            msg = "Не найден ffmpeg.exe! Проверьте папку 'bin'."
        messagebox.showerror("Ошибка системы", msg)
    except RuntimeError as e:
        msg = str(e)
        if "Conversion failed" in msg or "Nothing was written" in msg:
            msg = "Ошибка конвертации. Файл может быть поврежден."
        messagebox.showerror("Ошибка конвертации", msg)
    except Exception as e:
        messagebox.showerror("Неизвестная ошибка", str(e))
    finally:
        btn_convert.config(state=tk.NORMAL)

# --- СОЗДАНИЕ ИНТЕРФЕЙСА ---

root = tk.Tk()
root.title("Универсальный Конвертер (Видео + Фото)")
root.geometry("420x330")  # Чуть больше высота для надежности
root.resizable(False, False)

# Заголовок
lbl_title = tk.Label(root, text="Универсальный Конвертер", font=("Arial", 16, "bold"))
lbl_title.pack(pady=20)

# Фрейм для выбора типа (Видео / Фото)
frame_mode = tk.Frame(root)
frame_mode.pack(pady=5)
var_mode = tk.StringVar(value="video")

rb_video = tk.Radiobutton(frame_mode, text="🎬 Конвертировать ВИДЕО", variable=var_mode, value="video", command=on_mode_change, anchor="w")
rb_photo = tk.Radiobutton(frame_mode, text="📸 Конвертировать ФОТО", variable=var_mode, value="photo", command=on_mode_change, anchor="w")
rb_video.pack(fill="x", padx=20, pady=2)
rb_photo.pack(fill="x", padx=20, pady=2)

# Описание
lbl_desc = tk.Label(root, text="Конвертация видео: H.264 + AAC", font=("Arial", 9), fg="#333")
lbl_desc.pack(pady=5)

# Фрейм для формата
frame_options = tk.Frame(root)
frame_options.pack(pady=10)
lbl_format = tk.Label(frame_options, text="Формат:")
lbl_format.pack(side=tk.LEFT, padx=5)

combo_format = ttk.Combobox(frame_options, values=["mp4", "mov", "mkv", "avi"], state="readonly", width=10)
combo_format.current(0)
combo_format.pack(side=tk.LEFT, padx=5)

# Кнопка
btn_convert = tk.Button(
    root, text="Выбрать файл и конвертировать", command=on_convert_click,
    bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), padx=20, pady=10
)
btn_convert.pack(pady=20)  # Чуть уменьшил отступ, чтобы освободить место внизу

# === ГЛАВНОЕ ИЗМЕНЕНИЕ: НИЖНЯЯ ПАНЕЛЬ ===
# Создаем отдельный фрейм для низа, чтобы элементы не мешали друг другу
frame_bottom = tk.Frame(root)
frame_bottom.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

# Автор (справа в нижнем фрейме)
lbl_author = tk.Label(
    frame_bottom, 
    text="by faccasno", 
    font=("Courier New", 10, "italic"), 
    fg="#888888",
    justify=tk.RIGHT,
    anchor=tk.E
)
lbl_author.pack(side=tk.RIGHT)
# =========================================

root.mainloop()
