create table apply (
    application_id SERIAL PRIMARY KEY,   -- Identifiant unique de la postulation
    user_id INT NOT NULL,                -- L'ID de l'utilisateur qui a postulé
    job_id INT NOT NULL, 
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,  -- Clé étrangère vers la table `users`
    FOREIGN KEY (job_id) REFERENCES jobs(job_ID) ON DELETE CASCADE     -- Clé étrangère vers la table `jobs`
)