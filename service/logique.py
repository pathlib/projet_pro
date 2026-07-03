from securite import securites
from pydantic import BaseModel
from fastapi import Query, HTTPException
from utils.loggers import logger
from utils.gui import guis
from base_de_donnees.base_de_donnee import selection, deletion, creation, modification
from typing import Any, Dict,List

class Donnee(BaseModel):
    donnee: str
    id: int


# Affichage de la page d'accueil
def home()-> Any:
    try:
        logger.info("Gui afficher")
        securites.atest()
        return guis()
    except Exception as e:
        logger.error(f"Erreur lors de l'affichage GUI : {e}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")


# Recherche sécurisée
def recherche_donnee(item: Any)->Dict[str, Any]:
    try:
        data = selection()
    except Exception as e:
        logger.error(f"Erreur BDD (selection) : {e}")
        raise HTTPException(
            status_code=500, detail="Erreur interne de la base de données"
        )

    for d in data:
        try:
            if int(d["id"]) == item:
                return {"data": d}
            if str(d["data"]) == item:
                return {"data": d}

        except (ValueError, KeyError) as e:
            logger.warning(f"Donnée corrompue détectée en BDD : {e}")
            continue
    raise HTTPException(status_code=404, detail="Valeur introuvable")


# Obtenir les données avec une limite maximale stricte
def get_donnee(limit: int = Query(10, ge=1, le=100), offset: int = Query(0, ge=0))->Dict[str, Any]:
    try:
        data = selection()
        return {"data": data[offset : offset + limit]}
    except Exception as e:
        logger.error(f"Erreur BDD (get_donnee) : {e}")
        raise HTTPException(
            status_code=500, detail="Erreur interne de la base de données"
        )


# Permet de créer les données de façon sécurisée
def create_donnee(item: str)->List[str]:
    if not item or not item.strip():
        raise HTTPException(status_code=400, detail="Valeur vide interdite")

    try:
        data = selection()
        for d in data:
            if d["donnee"] == item:
                raise HTTPException(status_code=400, detail="La donnée existe déjà")
        creation(item)
        logger.info("Donnée enregistrée")
        return {"message": "La donnée a été sauvegardée"}

    except HTTPException:
        raise  # On laisse passer nos propres erreurs HTTP
    except Exception as e:
        logger.error(f"Erreur critique lors de la création : {e}")
        raise HTTPException(
            status_code=500, detail="Impossible de sauvegarder la donnée"
        )



# Permet la mise à jour sécurisée des données
def update_donnee(item_id: int, donnee_text: str)->Dict[str,str]:
    if not donnee_text or not donnee_text.strip():
        raise HTTPException(status_code=400, detail="Valeur vide interdite")

    try:
        data = selection()
        for d in data:
            if int(d["id"]) == item_id:
                modification(item_id, donnee_text)
                logger.info(f"Donnée {item_id} modifiée")
                return {"message": "Modification réussie"}

        raise HTTPException(status_code=404, detail="Donnée introuvable")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur critique lors de la modification de {item_id} : {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la modification")


# Supprime proprement et gère l'absence de l'élément
def delete_donnee(item: int)->Dict[str,Any]:
    try:
        data = selection()
        for d in data:
            if int(d["id"]) == item:
                deletion(item)
                logger.info(f"Donnée numéro {item} supprimée")
                return {"message": f"La donnée {item} a bien été supprimée"}

        raise HTTPException(status_code=404, detail="Donnée introuvable")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur critique lors de la suppression de {item} : {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la suppression")
def ping():
    return {"message": "Ping reussie"}
