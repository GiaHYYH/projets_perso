from pydantic import BaseModel

class UtilisateurCreation(BaseModel):
    usr_mail: str
    usr_mdp: str
    usr_nom: str | None = None
    usr_prenom: str | None = None 
    usr_niveau: str 
    usr_formation: str 

class UtilisateurConnexion(BaseModel):
    usr_mail: str
    usr_mdp: str


#from pydantic import BaseModel, EmailStr, Field

#class UtilisateurConnexion(BaseModel):
    #usr_mail: EmailStr
    #usr_mdp: str = Field(min_length=14)