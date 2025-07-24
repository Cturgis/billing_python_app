# Job Finder

## Présentation

- **Admin** : développeur avec tous les droits
- **Agency** : entreprise pouvant poster des offres
- **JobSeeker** : demandeur d'emploi pouvant postuler

## Fonctionnalités principales

- Inscription d'un nouvel utilisateur (JobSeeker par défaut)
- Création d'un profil JobSeeker avec informations personnelles
- Possibilité de compléter un profil d'entreprise (Agency) après inscription
- Authentification (login/logout) avec gestion des groupes
- Tableau de bord après connexion
- Gestion des messages de succès/erreur

## Installation

1. **Cloner le dépôt**
2. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```
3. **Configurer la base de données** (PostgreSQL recommandé, voir `docker-compose.yml`)
4. **Lancer les migrations** :
   ```bash
   python manage.py migrate
   ```
5. **Créer les utilisateurs par défaut** :
   ```bash
   python manage.py create_default_users
   ```
6. **Démarrer le serveur** :
   ```bash
   python manage.py runserver
   ```

## Utilisation avec Docker

- Lancer l'application et la base de données :
  ```bash
  docker-compose up --build
  ```

## Accès par défaut

- **Admin**
  - username: `admin`
  - password: `adminpass`
- **Customer/JobSeeker**
  - username: `customer`
  - password: `customerpass`

## Tests

Pour lancer les tests :
```bash
python manage.py test
```

## Structure des apps

- `user_manager` : gestion des utilisateurs, groupes, authentification, inscription
- `job_finder` : gestion des offres d'emploi, dashboard, etc.

## Routes principales

- `/register` : inscription d'un nouvel utilisateur
- `/register/agency` : compléter le profil entreprise (optionnel)
- `/login` : connexion
- `/logout` : déconnexion
- `/dashboard` : tableau de bord après connexion

## À venir

- Gestion des offres d'emploi
- Recherche et candidature
- Interface d'administration avancée

---

N'hésitez pas à consulter le code source pour plus de détails sur l'implémentation.
