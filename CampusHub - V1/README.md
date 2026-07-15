CAMPUSHUB

Projet créer par Georgia Eraste.

Permet aux étudiants de centraliser toutes choses pour leurs devoirs et révisions sur un compte personnel. Les étudiants pourront, avec un compte, gérer leurs matières, les tâches qu’ils doivent compléter (tels que créer des fiches de révisions, des projets/devoirs à faire, etc.), et compléter leur calendrier.


## Installations nécessairesannotated-doc==0.0.4
- fastapi == 0.139.0
- passlib == 1.7.4
- psycopg == 3.3.4
- PyJWT==2.13.0
- python-dotenv==1.2.2
- uvicorn == 0.50.2


## Base de données

Le modèle de données est constitué de quatre tables principales :

- `t_utilisateur_usr`
- `t_matiere_mat`
- `t_tache_tac`
- `t_lien_matiere_tache_lmt`

Les utilisateurs possèdent plusieurs matières.

Les tâches peuvent être associées à plusieurs matières grâce à une table d'association.

Les suppressions utilisent `ON DELETE CASCADE` lorsque cela correspond aux règles métier.

## backend

server.py est le point d'entrée du backend de CampusHub. Il créer l'application FastAPI et assemble les différents composants du projet, tel que l'enregistrement des routes.

database.py est responsable de toute la communication entre le backend Python et PostgreSQL.

models.py permet de définir les modèles Pydantic, permettant notamment la validation des données.

utilisateurs.py contient toutes les routes qui concernent les utilisateurs. Concerne notamment l'inscription et la connexion d'un compte.

matieres.py contient toutes les routes qui concernent les matières. Concerne nottament leur création, modification et suppression.

taches.py contient toutes les routes qui concernent les tâches. Concerne nottament leur création, modification et suppression.

auth.py permet de créer et de valider des "jetons", ou JWT.

dependencies.py permet de gérer l'utilisateur connecté.
