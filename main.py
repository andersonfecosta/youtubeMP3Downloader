import os
import tkinter as tk
from tkinter import messagebox
from pytube import YouTube
from pydub import AudioSegment


def download_audio_from_youtube(url):
    try:
        yt = YouTube(url)

        stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()

        output_path = os.path.expanduser("~/Downloads")
        out_file = stream.download(output_path=output_path, filename="temp_audio")

        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'

        AudioSegment.from_file(out_file).export(new_file, format='mp3')

        os.remove(out_file)

        messagebox.showinfo("Sucesso", f"{yt.title} foi baixado e salvo como {new_file}")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao baixar o áudio: {e}")


def on_download_button_click():
    url = url_entry.get()
    if url:
        download_audio_from_youtube(url)
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

root.mainloop()
