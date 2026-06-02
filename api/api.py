from fastapi import FastAPI, Body, Query
from fastapi.responses import HTMLResponse
from service import logique

app = FastAPI()


# affiche la page d acceuil et la gui
@app.get("/", response_class=HTMLResponse)
def home():
    return logique.home()


# recherche les donnees par id
@app.get("/donnees/{id}")
def recherche_donnee(id: int):
    return logique.recherche_donnee(id)


# afficher  des donnees
@app.get("/donnees")
def get_donnee(limit: int = Query(10, ge=1), offset: int = Query(0, ge=0)):
    return logique.get_donnee(limit, offset)


# ajouter les donnees
@app.post("/donnees", status_code=201)
def create_donnee(donnee_add: str = Body(...)):
    return logique.create_donnee(donnee_add)


# modification des donnees
@app.put("/donnees/{id}")
def update_donnee(id: int, donnee_add: str = Body(...)):
    return logique.update_donnee(id, donnee_add)


# suppresion des donnees
@app.delete("/donnees/{id}")
def delete_donnee(id: int):
    return logique.delete_donnee(id)
