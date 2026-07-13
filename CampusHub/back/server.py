from fastapi import FastAPI, Depends

from database import get_connection
from utilisateurs import router as usr_router
from dependencies import get_current_user


app = FastAPI()

app.include_router(usr_router)

@app.get("/")
def accueil():
    return {"message": "API CampusHub opérationnelle."}


@app.get("/test-db")
def test_db():
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT 1;")
        result = cursor.fetchone()
    return {"resultat" : result[0]}


@app.get("/profil")
def profil(usr_mail: str = Depends(get_current_user)):
    return {"utilisateur_connecte": usr_mail}
