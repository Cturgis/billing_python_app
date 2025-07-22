# Application de facturation - Installation & Fonctionnalités

## Identifiants par défaut

- **Administrateur**
  - Nom d'utilisateur : `admin`
  - Mot de passe : `adminpassword`
- **Client**
  - Nom d'utilisateur : `customer`
  - Mot de passe : `customerpassword`

## Fonctionnalités

- **Authentification utilisateur** : Connexion/déconnexion, rôles administrateur et client.
- **Panneau d'administration** : Gérer les utilisateurs, produits, factures et clients.
- **Tableau de bord client** : Voir la boutique, acheter des produits et consulter les factures.
- **Gestion des factures** : Créer, consulter et gérer les factures.
- **Gestion des produits** : Ajouter, modifier et supprimer des produits.
- **Gestion des groupes** : Les utilisateurs sont automatiquement assignés aux groupes 'admin' ou 'customer'.

## Démarrage rapide (Docker Compose)

1. **Cloner le dépôt** (si ce n'est pas déjà fait) :
   ```sh
   git clone https://github.com/Cturgis/billing_python_app.git
   cd Python
   ```

2. **Construire et démarrer l'application :**
   ```sh
   docker-compose up --build
   ```
   Cela va :
   - Démarrer PostgreSQL et pgAdmin
   - Construire et lancer l'application Django
   - Exécuter les migrations et créer les utilisateurs par défaut

3. **Accéder à l'application :**
   - Application Django : [http://localhost:8000](http://localhost:8000)
   - Panneau d'administration : [http://localhost:8000/admin/](http://localhost:8000/admin/)
   - pgAdmin : [http://localhost:15432](http://localhost:15432) (identifiant : admin@pgadmin.com / mot de passe : password)

## Développement
- Le code de l'application se trouve dans le répertoire `projects/`.
- Les fichiers statiques sont dans `billing/static/billing/`.
- Les modèles sont dans `billing/templates/billing/`.
- Pour ajouter des fonctionnalités, modifier ou ajouter des fichiers dans les dossiers d'applications Django appropriés.

## Remarques
- L'application crée et assigne automatiquement des utilisateurs aux groupes au démarrage.
- Pour changer les identifiants par défaut, modifier la commande de gestion dans `billing/management/commands/create_default_users.py`.
- Pour la production, mettre à jour les secrets et envisager d'utiliser `collectstatic` et un serveur prêt pour la production.
