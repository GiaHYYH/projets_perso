-- =====================================================
-- Projet : CampusHub
-- Fichier : 002_tests_sql.sql
-- Description : Tests pour vérifier si les tables principales fonctionnent.
-- Auteur : G. Eraste
-- Date : 07 Juillet 2026
-- =====================================================

--TEST 1 : création d'un utilisateur
INSERT INTO t_utilisateur_usr
VALUES ('erastegeorgia@gmail.com', 'Cre@ti0n', 'Eraste', 'Georgia', 'L3', 'Informatique');

--TEST 2 : création de 2 matières
INSERT INTO t_matiere_mat (mat_nom, usr_mail)
VALUES ('Programmation C', 'erastegeorgia@gmail.com');

INSERT INTO t_matiere_mat (mat_nom, mat_couleur, usr_mail)
VALUES ('Anglais', '#215E61', 'erastegeorgia@gmail.com');

--TEST 3 : double création de la même matière
-- RÉSULTAT ATTENDU : refus
INSERT INTO t_matiere_mat
VALUES ("Programmation C", "erastegeorgia@gmail.com");

--TEST 4 : créer une tâche + associer à 2 matières
INSERT INTO t_tache_tac (tac_nom)
VALUES ('Faire fiches de révision');

INSERT INTO t_lien_matiere_tache_lmt
VALUES (1, 1);

INSERT INTO t_lien_matiere_tache_lmt
VALUES (2, 1);

--TEST 5 : supprimer une matière
--RÉSULTAT ATTENDU : disparition de la matière + de la ligne
--correspondante dans la table associative + la tâche existe toujours
DELETE FROM t_matiere_mat WHERE mat_id=1;

--TEST 6 : supprimer l'utilisateur
--RÉSULTAT ATTENDU : utilisateur + matières + table de liason
--supprimée/vide + voir table tâches
DELETE FROM t_utilisateur_usr WHERE usr_mail='erastegeorgia@gmail.com';