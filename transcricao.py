import tkinter as tk
from tkinter import messagebox
from pytubefix import YouTube
from pytubefix.cli import on_progress
import whisper
import os
import subprocess

# Function to add line breaks every 100 characters
def add_line_breaks(text, interval=100):
    return '\n'.join(text[i:i+interval] for i in range(0, len(text), interval))

# Function to process the YouTube video
def process_video():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Erro", "Por favor, insira a URL do vídeo do YouTube.")
        return

    try:
        # Create the "baixado" directory if it doesn't exist
        if not os.path.exists("baixado"):
            os.makedirs("baixado")

        yt = YouTube(url, on_progress_callback=on_progress)
        ys = yt.streams.get_audio_only()
        audio_path = os.path.join("baixado", "audio.mp3")
        ys.download(filename=audio_path)
        ys.download(mp3=True)

        model = whisper.load_model("base")
        result = model.transcribe(audio_path)

        formatted_text = add_line_breaks(result["text"], 100)
        transcription_path = os.path.join("baixado", "transcricao.txt")

        with open(transcription_path, "w") as f:
            f.write(formatted_text)

        messagebox.showinfo("Sucesso", f"Transcrição concluída e salva em '{transcription_path}'.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

# Function to open the "baixado" folder
def open_folder():
    folder_path = os.path.abspath("baixado")
    subprocess.Popen(f'explorer "{folder_path}"')

# Create the main window
root = tk.Tk()
root.title("Transcritor de YouTube")

# Create and place the URL entry
tk.Label(root, text="URL do vídeo do YouTube:").pack(pady=10)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# Create and place the process button
process_button = tk.Button(root, text="Processar", command=process_video)
process_button.pack(pady=10)

# Create and place the open folder button
open_folder_button = tk.Button(root, text="Abrir Pasta de Arquivos", command=open_folder)
open_folder_button.pack(pady=10)

# Run the application
root.mainloop()
