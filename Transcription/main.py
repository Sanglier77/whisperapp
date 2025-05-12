"""Script pour choisir et transcrire un audio"""

import tkinter as tk
from tkinter import filedialog
from tkinter import *
from tkinter import ttk
import subprocess
import threading
from PIL import Image, ImageTk
from pathlib import Path
import logging

path_file_save = Path.home() / "Downloads"
BASE_DIR = Path(__file__).resolve().parent
logging.basicConfig(filename=BASE_DIR / "main.log", level=logging.INFO)


def file():
    """Récupère l'adresse du fichier à transcrire

    Returns:
        str: chemin du dossier
    """
    global pathfile_to_transcription
    pathfile_to_transcription = filedialog.askopenfilename(initialdir= "C:\\",title="Selectionner un Fichier Audio",filetypes=(("all files","*.*"),("mp3 files","*.mp3"),("wav files","*.wav")))
    text_file.config(text=pathfile_to_transcription)
    return pathfile_to_transcription

def transcription():
    """Vérifie si filename contient un str puis lance la barre de chargement.
       Lance la transcription avec une autre fonctione à l'intérieur
       Utilisation de threading pour éviter de fichier la fenêtre utilisateur
    """
    if pathfile_to_transcription is None:
        text_file = tk.Label(window, text="Aucun fichier sélectionné.")
        text_file.pack()
        return

    progress.start()

    # Lancer la transcription dans un thread pour ne pas bloquer l'interface
    def run_transcription():
        """Lance une commande dans le CMD pour lancer whisper avec Filename, puis de le sauvegarder sur path_file_save au format TXT
        """
        # Le processus de transcription doit être lancé ici
        subprocess.run(['whisper', pathfile_to_transcription, '--language', 'fr', '--output_dir', path_file_save, '--output_format', 'txt'])
        
        # Une fois la transcription terminée
        progress.stop()

    # Démarrer la transcription dans un thread
    threading.Thread(target=run_transcription, daemon=True).start()


#Début de la configuration de la fenêtre.

header_picture = BASE_DIR / "Image" / "Logo.png"
pathfile_to_transcription = None
color_font = "#222222"
color_text = "#e9e9e9"

# Création de la fenêtre
window = tk.Tk()

#Ajout de l'image d'en tête 
image = Image.open(header_picture) 
photo = ImageTk.PhotoImage(image)
canvas = tk.Canvas(window, width = image.size[0], height = image.size[1], bg=color_font)
canvas.create_image(0,0, anchor = tk.NW, image=photo)
canvas.pack()

#Configuration de la fenêtre, TITRE etc ...
window.title("T.A")
window.geometry("700x500")
window.configure(bg=color_font)
title = tk.Label(window, text="Transcription audio", font=("Arial", 20), width=20, height=2,fg=color_text, bg=color_font)
title.pack()
window.iconbitmap(BASE_DIR / "Image" / "Icon.ico")

#Panneau séparant le bouton d'ajour de l'audio et le texte
my_paned = tk.PanedWindow(window, orient="horizontal")
my_paned.pack(fill="both", expand=True)
 
left_frame = tk.Frame(my_paned , background=color_font, width=200, height=1)
right_frame = tk.Frame(my_paned , background=color_font, width=200, height=1)
 
my_paned.add(left_frame)
my_paned.add(right_frame)

text_file = tk.Label(right_frame, text="Aucun audio séléctionné",fg=color_text, bg=color_font)
text_file.pack()
button_add_audio = tk.Button(left_frame, text="Ajouter votre audio !", command=file)
button_add_audio.pack()

#def frame
frame = tk.Frame(window, width=100, height=110, bg=color_font)
frame.pack()

# Button for start def transcription()
button_transcription = tk.Button(window, text="Transcrire votre audio !", command=transcription)
button_transcription.pack()

# Barre de progression
progress = ttk.Progressbar(window, mode='indeterminate')
progress.pack(pady=30)

#def frame
frame = tk.Frame(window, width=170, height=40,bg=color_font)
frame.pack()

#Info
text_info = tk.Label(window, text="Le fichier texte sera enregistré dans le dossier téléchargement de l'ordinateur",fg=color_text, bg=color_font)
text_info.pack()
create_by = tk.Label(window, text="Crée par AUFILS Clément",fg=color_text, bg=color_font)
create_by.pack()


window.mainloop()
