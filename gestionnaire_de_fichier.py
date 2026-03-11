from pathlib import Path
import os
import shutil

def clear_console():
    if os.name == "nt":
        os.system("cls")# Windows
    else:
        os.system("clear")# macOS / Linux


def m():
    dossiers = [
        ("Bureau", "📁"),
        ("Téléchargement", "⬇️"),
        ("Documents", "📄"),
        ("Images", "🖼️"),
        ("Musique", "🎵"),
        ("Vidéos", "🎬"),
        ("Projets", "📂"),
    ]


    for nom, icone in dossiers:
        print(f"[{icone}] {nom}")

def affiche():
    a = input("Desktop")
    b = input("fichier ")
    donnee = Path.home() / a / b
    if donnee.exists():
        if donnee.is_dir():
            return donnee
        elif donnee.is_file():
            return donnee


def ouvrir(b):
    chemin=Path.home()/b
    os.startfile(chemin)
#a metre pour linux et mac

def supprimer(b):
    c=input("vouler vous vraiment supprimer ?")
    if c == "oui":
        chemin=Path.home()/b
        if chemin.is_file():
            Path(chemin).unlink()
        else :
            shutil.rmtree(Path(chemin))

def creer():
    a=input("fichier ou dossier")
    chemin = Path.home() / "Desktop" / "nh.txt"
    if a == "fichier":
        chemin.touch()
    else:
        chemin.mkdir()

def renomer():
    chemin=Path.home()/"Desktop"/"nh.txt"
    nchemin=Path.home()/"Desktop"/"nkl.txt"
    Path(chemin).rename(nchemin)

def copier():
    chemin=Path.home()/"Desktop"/"n.txt"
    nchemin=Path.home()/"Documents"/"n.txt"
    shutil.copy2(Path(chemin), Path(nchemin))


while True:
    clear_console()
    print("bienvenue")
    m()
    b=affiche()
    a=input("affiche ouvrir supprimer creer renomer copier")
    if a == "affiche":
        affiche()
    elif a == "ouvrir":
        ouvrir(b)
    elif a == "supprimer":
        supprimer(b)
    elif a == "creer":
        creer()
    elif a == "renomer":
        renomer()
    elif a == "copier":
        copier()
