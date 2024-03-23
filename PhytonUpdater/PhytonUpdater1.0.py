import tkinter as tk
from tkinter import messagebox, colorchooser
import requests
import os
import zipfile
import time

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
    else:
        messagebox.showinfo("Kein Update verfügbar", "Dein Programm ist auf dem neuesten Stand.")
        root.destroy()  # Schließt das Fenster nach 10 Sekunden
        root.after(10000, root.quit)  # Automatisches Schließen nach 10 Sekunden

def download_and_install_update(download_url):
    try:
        response = requests.get(download_url)
        update_file_name = download_url.split('/')[-1]
        with open(update_file_name, "wb") as file:
            file.write(response.content)
        with zipfile.ZipFile(update_file_name, "r") as zip_ref:
            zip_ref.extractall("update")
        os.remove(update_file_name)
        messagebox.showinfo("Update durchgeführt", "Das Update wurde erfolgreich installiert. Das Programm wird neu gestartet.")
        root.destroy()
        # Starte das Hauptprogramm
        os.system("Hauptprogramm.exe")  # Der Dateiname des Hauptprogramms muss hier entsprechend angegeben werden
    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler beim Installieren des Updates: {str(e)}")
        messagebox.showinfo("Update fehlgeschlagen", "Bitte versuchen Sie es erneut.")

# Initialisiere das Hauptfenster
root = tk.Tk()
root.withdraw()  # Verstecke das Hauptfenster

current_version = "1.0"  # Aktuelle Version des Programms
check_for_updates()  # Überprüfe auf Updates beim Start

root.mainloop()
