import os
import threading
import tkinter as tk
import re
from tkinter import messagebox
from pytube import YouTube
from pydub import AudioSegment

def download_audio_from_youtube(url):
    try:
        yt = YouTube(url)

        def on_progress(stream, chunk, bytes_remaining):
            total_size = stream.filesize
            bytes_downloaded = total_size - bytes_remaining
            percentage = bytes_downloaded / total_size * 100
            progress_label.config(text=f"Baixando... {percentage:.2f}%")
            if percentage >= 100:
                progress_label.config(text="Download completo. Finalizando...")
            root.update_idletasks()

        yt.register_on_progress_callback(on_progress)

        stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()

        title = yt.title

        def clean_filename(filename):
            return re.sub(r'[\\/*?:"<>|]', "", filename)

        clean_title = clean_filename(title)

        output_path = os.path.expanduser("~/Downloads")
        out_file = stream.download(output_path=output_path, filename="temp_audio")

        new_file = os.path.join(output_path, clean_title + '.mp3')

        AudioSegment.from_file(out_file).export(new_file, format='mp3')

        os.remove(out_file)

        messagebox.showinfo("Sucesso", f"{yt.title} foi baixado e salvo como {new_file}")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao baixar o áudio: {e}")
    finally:
        progress_label.config(text="")
        download_button.config(state=tk.NORMAL)


def on_download_button_click():
    url = url_entry.get()
    if url:
        download_button.config(state=tk.DISABLED)
        progress_label.config(text="Iniciando download...")
        threading.Thread(target=download_audio_from_youtube, args=(url,)).start()
    else:
        messagebox.showwarning("Aviso", "Por favor, insira o link do vídeo do YouTube.")


root = tk.Tk()
root.title("YouTube MP3 Downloader")

url_label = tk.Label(root, text="Link do YouTube:")
url_label.pack(pady=10)

url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

download_button = tk.Button(root, text="Baixar Áudio", command=on_download_button_click)
download_button.pack(pady=20)

progress_label = tk.Label(root, text="", fg="blue")
progress_label.pack(pady=10)

root.mainloop()
