import tkinter as tk
from tkinter import messagebox, colorchooser
import requests
import os
import zipfile
import re

def get_latest_version_info():
    try:
        response = requests.get("https://raw.githubusercontent.com/RapChapter/Phyton-Updater/main/version.txt")
        if response.status_code == 200:
            # Version und Download-URL aus der Datei lesen
            version_info = response.text.strip().split(',')
            return {"version": version_info[0], "url": version_info[1]}
        else:
            messagebox.showerror("Fehler", "Fehler beim Zugriff auf die Versionsinformationen.")
    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler beim Abrufen der Versionsinformationen: {str(e)}")

def check_for_updates():
    latest_version_info = get_latest_version_info()
    if latest_version_info and latest_version_info["version"] != current_version:
        response = messagebox.askyesno("Update verfügbar", f"Es ist ein Update auf Version {latest_version_info['version']} verfügbar. Möchtest du es installieren?")
        if response == tk.YES:
            download_and_install_update(latest_version_info["url"])
            return True
    else:
        messagebox.showinfo("Kein Update verfügbar", "Dein Programm ist auf dem neuesten Stand.")
    return False

def download_and_install_update(download_url):
    try:
        response = requests.get(download_url)
        update_file_name = download_url.split('/')[-1]
        with open(update_file_name, "wb") as file:
            file.write(response.content)
        with zipfile.ZipFile(update_file_name, "r") as zip_ref:
            zip_ref.extractall("update")
        os.remove(update_file_name)
        messagebox.showinfo("Update durchgeführt", "Das Update wurde erfolgreich installiert. Bitte starte das Programm neu, um die neue Version zu verwenden.")
        root.destroy()
        # Beachte, dass du den Pfad anpassen musst, um die neue Version korrekt zu starten.
        os.system(f"python update/{update_file_name.replace('.zip', '.py')}")
    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler beim Installieren des Updates: {str(e)}")

def change_color():
    color = colorchooser.askcolor(title="Choose Text Color")
    if color[1]:
        label.config(fg=color[1])

# Initialisiere das Hauptfenster
root = tk.Tk()
root.title("Mein Programm")
window_width = 900
window_height = 600
root.geometry(f"{window_width}x{window_height}")

label = tk.Label(root, text="Hallo", font=("Helvetica", 24))
label.pack(pady=20)

color_button = tk.Button(root, text="Farbe ändern", command=change_color)
color_button.pack()

update_button = tk.Button(root, text="Nach Updates suchen", command=check_for_updates)
update_button.pack()

current_version = "1.0"  # Aktuelle Version des Programms
version_label = tk.Label(root, text=f"Version {current_version}")
version_label.pack(side=tk.BOTTOM)

root.mainloop()
