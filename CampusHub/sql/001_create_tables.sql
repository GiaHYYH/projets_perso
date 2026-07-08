-- =====================================================
-- Projet : CampusHub
-- Fichier : 001_create_tables.sql
-- Description : Création des tables principales
-- Auteur : G. Eraste
-- Date : 06 Juillet 2026
-- =====================================================

--table qui instancie un profil étudiant
CREATE TABLE t_utilisateur_usr (
    usr_mail VARCHAR(254) PRIMARY KEY,
    usr_mdp VARCHAR(255) NOT NULL,
    usr_nom VARCHAR(100),
    usr_prenom VARCHAR(100),
    usr_niveau CHAR(2) NOT NULL CHECK (usr_niveau IN ('L1', 'L2', 'L3', 'M1', 'M2')),
    usr_formation VARCHAR(255) NOT NULL 
);

--table qui instancie une matière
CREATE TABLE t_matiere_mat (
    mat_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    mat_nom VARCHAR(255) NOT NULL,
    mat_couleur CHAR(7) DEFAULT '#FFFFFF',
    usr_mail VARCHAR(255) NOT NULL,
    
    CONSTRAINT fk_mat_usr FOREIGN KEY (usr_mail) REFERENCES t_utilisateur_usr(usr_mail) ON DELETE CASCADE, 

    CONSTRAINT uq_mat_nom_usr_mail UNIQUE (usr_mail, mat_nom)

);

--table qui instancie une tâche
CREATE TABLE t_tache_tac (
    tac_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    tac_nom VARCHAR(100) NOT NULL,
    tac_duree INT NULL CHECK (tac_duree > 0),
    tac_status CHAR(1) NOT NULL DEFAULT 'A' CHECK (tac_status IN ('A', 'E', 'T')),
    usr_mail VARCHAR(255) NOT NULL,
    
    CONSTRAINT fk_tac_usr FOREIGN KEY (usr_mail) REFERENCES t_utilisateur_usr(usr_mail) ON DELETE CASCADE
);

--table de liason entre t_tache_tac & t_matiere_mat
CREATE TABLE t_lien_matiere_tache_lmt (
    mat_id INT NOT NULL,
    tac_id INT NOT NULL,

    CONSTRAINT pk_lmt_compo PRIMARY KEY (mat_id, tac_id),

    CONSTRAINT fk_lmt_mat FOREIGN KEY (mat_id) REFERENCES t_matiere_mat(mat_id) ON DELETE CASCADE,

    CONSTRAINT fk_lmt_tac FOREIGN KEY (tac_id) REFERENCES t_tache_tac(tac_id) ON DELETE CASCADE
);