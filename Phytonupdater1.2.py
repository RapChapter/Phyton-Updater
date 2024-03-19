import tkinter as tk
from tkinter import messagebox, colorchooser
import subprocess
import requests
import random

def check_for_updates():
    current_version = "1.2"
    try:
        response = requests.get("https://raw.githubusercontent.com/RapChapter/Phyton-Updater/main/version.txt")
        if response.status_code == 200:  # Überprüfe, ob das Repository gefunden wurde
            latest_version = response.text.strip()
            if latest_version != current_version:
                response = messagebox.askyesno("Update verfügbar", "Es ist ein Update verfügbar. Möchtest du es installieren?")
                if response == tk.YES:
                    download_and_install_update()
            else:
                messagebox.showinfo("Kein Update verfügbar", "Dein Programm ist auf dem neuesten Stand.")
        else:
            messagebox.showerror("Fehler", "Repository nicht gefunden. Überprüfen Sie die GitHub-URL.")
    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler beim Überprüfen auf Updates: {str(e)}")

def download_and_install_update():
    try:
        subprocess.run(["git", "clone", "https://github.com/RapChapter/Phyton-Updater.git"])
        messagebox.showinfo("Update durchgeführt", "Das Update wurde erfolgreich installiert.")
        root.destroy()
    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler beim Installieren des Updates: {str(e)}")

def change_color():
    color = colorchooser.askcolor(title="Choose Text Color")
    if color[1]:
        label.config(fg=color[1])

def random_color():
    random_hex_color = f"#{random.randint(0, 0xFFFFFF):06x}"
    label.config(fg=random_hex_color)

root = tk.Tk()
root.title("Mein Programm")

# Setze die gewünschte Breite und Höhe des Fensters (3-mal größer)
window_width = 900
window_height = 600
root.geometry(f"{window_width}x{window_height}")

label = tk.Label(root, text="Hallo", font=("Helvetica", 24))
label.pack(pady=20)

color_button = tk.Button(root, text="Farbe ändern", command=change_color)
color_button.pack()

random_color_button = tk.Button(root, text="Zufällige Farbe", command=random_color)
random_color_button.pack()

update_button = tk.Button(root, text="Nach Updates suchen", command=check_for_updates)
update_button.pack()

version_label = tk.Label(root, text="Version 1.0")
version_label.pack(side=tk.BOTTOM)

root.mainloop()
