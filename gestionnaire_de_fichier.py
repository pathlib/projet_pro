from pathlib import Path
import os


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
    a=input("Desktop")
    b=input("fichier ")
    donnee = Path.home()/a/b
    if donnee.exists():
        if donnee.is_dir():
            return donnee
        elif donnee.is_file():
            return donnee


def ouvrir():
    chemin=Path.home()/"Desktop"/"n.txt"
    os.startfile(chemin)


def supprimer():
    b=input("vouler vous vraiment supprimer ?")
    if b == "oui":
        chemin=Path.home()/"Desktop"/"n.txt"
        Path(chemin).unlink()
    else :
        return

def creer():
    chemin=Path.home()/"Desktop"/"n.txt"
    with open(chemin,"w") as fichier:
        print(fichier)

def renomer():
    chemin=Path.home()/"Desktop"/"n.txt"

def copier():
    chemin=Path.home()/"Desktop"/"n.txt"

while True:
    clear_console()
    print("bienvenue")
    m()
    a=input("affiche ouvrir supprimer creer")
    if a == "affiche":
        affiche()

    elif a == "ouvrir":
        ouvrir()

    elif a == "supprimer":
        supprimer()
    elif a == "creer":
        creer()
    elif a == "renomer":
        renomer()

