# Job Finder 🚀

## Salut ! 👋

Bienvenue sur ma petite application Job Finder ! J'ai essayé de rendre tout ça aussi simple et intuitif que possible.

## Docker Compose  🐳

J'ai mis en place un Docker Compose qui gère tout.
il execute surtout le script create_default_users.py dans user_manager

## Comment lancer l'application ? 🚀

1. Clone le repo
2. À la racine :
   ```bash
   docker-compose up
   ```
3. Rends-toi sur http://localhost:8000 et voilà !
   4. Il arrive que django se lance plus vite que postgres, dans ce cas on peut tout redemarrer : 
   ```bash
   docker compose down
   docker compose up
   ```

## Comptes par défaut 👤

j'ai préparé 3 comptes :

| Type de compte | Nom d'utilisateur | Mot de passe | Description |
|---------------|-------------------|--------------|-------------|
| Admin         | admin             | adminpass    | Accès à tout |
| JobSeeker     | jobseeker         | jobseekerpass | Un demandeur d'emploi |
| Agency        | agency            | agencypass   | Une entreprise qui recrute |

## gestion utilisateur 🔐

Le système de gestion utilisateur est axé autour du middleware CheckProfile :

- Un utilisateur non connecté est redirigé vers la page de login
- Un utilisateur connecté sans groupe est redirigé vers select_profile pour choisir son type de profil
- Un utilisateur avec le groupe JobSeeker mais sans profil JobSeeker est redirigé vers register_jobseeker
- Un utilisateur avec le groupe Agency mais sans profil Agency est redirigé vers register_agency
- Un utilisateur avec un profil complet peut naviguer normalement dans l'application

## Architecture du projet 🏗️

Le projet est découpé en deux applications Django :
- `user_manager` : gère tout ce qui est authentification, inscription, profils utilisateurs
- `job_finder` : contient les fonctionnalités métier (dashboard, offres d'emploi, etc.)

## Et voilà ! 🎉

Voila voila. Beaucoup d'IA pour réussir coder aussi vite, mais surtout beaucoup de papier et le tronc dev a la main pour donner a manger a l agent,
Serein sur la comprehension de ce que j'ai fais.

Happy testing! 🧪
