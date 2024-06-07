from pytube import YouTube
from pydub import AudioSegment
import os


def download_audio_from_youtube(url):
    yt = YouTube(url)

    stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()

    output_path = os.path.expanduser("~/Downloads")
    out_file = stream.download(output_path=output_path, filename="temp_audio")

    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'

    AudioSegment.from_file(out_file).export(new_file, format='mp3')

    os.remove(out_file)

    print(f"{yt.title} foi baixado e salvo como {new_file}")


if __name__ == "__main__":
    url = input("Insira o link do vídeo do YouTube: ")
    download_audio_from_youtube(url)
