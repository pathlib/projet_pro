from pathlib import Path
import os
import shutil
import subprocess
import threading



def clear_console():
    if os.name == "nt":
        os.system("cls")# Windows
    else:
        os.system("clear")# macOS / Linux

def afficheur():
    donnee = Path.home() / a
    if donnee.exists():
        if donnee.is_dir():
            for r in donnee.iterdir():
                print(r)



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
    a = input("Nom du dossier (ex: Desktop): ")
    donnee = Path.home() / a
    if donnee.exists():
        if donnee.is_dir():
            for r in donnee.iterdir():
                print(r)
            b=input("Nom du fichier (ex: Desktop): ")
            donnee = Path.home() / a / b

            return donnee

        elif donnee.is_file():
            print("C'est un fichier :", donnee)
            return donnee
    else:
        print("Le chemin n'existe pas")


def ouvrir(b):
    try:
        chemin=Path.home()/ b
        if os.name == "nt":
            os.startfile(chemin)
        elif os.name == "e":
            subprocess.run(["open", str(chemin)])
        else:
            subprocess.run(["xdg-open", str(chemin)])  # Linux
    except FileNotFoundError:
        print("ficier non trouver")


def supprimer(b):
    c=input("vouler vous vraiment supprimer ?")
    if c == "oui":
        chemin=Path.home()/b
        if chemin.is_file():
            try:
                Path(chemin).unlink()
            except FileNotFoundError:
                print("fichier non trouver")
        else :
            shutil.rmtree(Path(chemin))


def creer(b):
    chemin = Path.home()/ b
    b=input("fichier ou dossier ")
    if b == "fichier":
        chemin.touch()
    else:
        chemin.mkdir()


def renomer(b):
    chemin=Path.home()/b
    nouveaux_nom=input("nouveaux nom ")
    try:
        nchemin=Path.home()/"Desktop"/nouveaux_nom
        Path(chemin).rename(nchemin)
    except FileNotFoundError:
        print("fichier non trouver")


def copier(b):
    chemin=Path.home()/ b
    try:
        nouveaux_chemin=input("nouveaux chemin ")
        nouveaux_nom=input("nouveaux nom ")
        nchemin=Path.home() / nouveaux_chemin / nouveaux_nom
        shutil.copy2(chemin,nchemin)
    except FileNotFoundError:
        print("ficier non trouver")


def deplacer(b):
    chemin = Path.home() / b
    nouveaux_nom=input("nouvel endrois ")
    nchemin = Path.home() / b / nouveaux_nom
    try:
        shutil.move(chemin, nchemin)
    except FileNotFoundError:
        print("fichier non trouver")


def corbeille(b):
    chemin=Path.home()/ b

v=threading.Thread(target=afficheur())
h=threading.Thread(target=affiche())
v.start()
h.start()
v.join()
h.join()


while True:
    clear_console()
    print("bienvenue")
    m()
    b=affiche()
    a=input("affiche ouvrir supprimer creer renomer copier deplacer")
    if a == "affiche":
        affiche()
    elif a == "ouvrir":
        ouvrir(b)
    elif a == "supprimer":
        supprimer(b)
    elif a == "creer":
        creer(b)
    elif a == "renomer":
        renomer(b)
    elif a == "copier":
        copier(b)
    elif a == "deplacer":
        deplacer(b)
