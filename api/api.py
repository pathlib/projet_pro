from typing import Any
import time
from fastapi import FastAPI, Body, Query
from fastapi.responses import HTMLResponse
from service import logique
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request,APIRouter
from prometheus_fastapi_instrumentator import Instrumentator


app = FastAPI()


Instrumentator().instrument(app).expose(app)
@app.middleware("http")
def times(request,call_next):
    start = time.time()
    response = call_next(request)
    end = time.time()
    print(f"Temps : {end - start:.3f}s")
    return response


limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# gestion propre de l'erreur 429
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)
router=APIRouter(prefix="/v2")



# affiche la page d acceuil et la gui
@app.get("/", response_class=HTMLResponse)
@limiter.limit("3/second")
def home(request: Request):
    return logique.home()

# affiche la page d acceuil et la gui
@router.get("/", response_class=HTMLResponse)
@limiter.limit("3/second")
def home2(request: Request):
    return logique.home2()


# recherche les donnees par id
@app.get("/donnees/{id}")
@limiter.limit("3/second")
def recherche_donnee(request: Request,id:str):
    return logique.recherche_donnee(id)


# afficher  des donnees
# les donnnee ne son pas coupoer
@app.get("/donnees")
@limiter.limit("3/second")
def get_donnee(request: Request,limit: int = Query(10, ge=1), offset: int = Query(0, ge=0)):
    return logique.get_donnee(limit, offset)


# ajouter les donnees
@app.post("/donnees", status_code=201)
@limiter.limit("5/second")
def create_donnee(request: Request,donnee_add: str = Body(...)):
    return logique.create_donnee(donnee_add)


# modification des donnees
@app.put("/donnees/{id}")
@limiter.limit("3/second")
def update_donnee(request: Request,id: int, donnee_add: str = Body(...)):
    return logique.update_donnee(id, donnee_add)


# suppresion des donnees
@app.delete("/donnees/{id}")
@limiter.limit("3/second")
def delete_donnee(request: Request,id: int):
    return logique.delete_donnee(id)

@app.get("/ping")
@limiter.limit("3/second")
def ping(request: Request):
    return logique.ping()

@app.get("/ready")
@limiter.limit("3/second")
def db(request: Request):
    return logique.ready()

app.include_router(router)