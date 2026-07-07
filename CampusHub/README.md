CAMPUSHUB

Projet créer par Georgia Eraste.

Permet aux étudiants de centraliser toutes choses pour leurs devoirs et révisions sur un compte personnel. Les étudiants pourront, avec un compte, gérer leurs matières, les tâches qu’ils doivent compléter (tels que créer des fiches de révisions, des projets/devoirs à faire, etc.), et compléter leur calendrier.

## Base de données

Le modèle de données est constitué de quatre tables principales :

- `t_utilisateur_usr`
- `t_matiere_mat`
- `t_tache_tac`
- `t_lien_matiere_tache_lmt`

Les utilisateurs possèdent plusieurs matières.

Les tâches peuvent être associées à plusieurs matières grâce à une table d'association.

Les suppressions utilisent `ON DELETE CASCADE` lorsque cela correspond aux règles métier.
