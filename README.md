# Air Quality DataOps/MLOps

Plateforme universitaire de surveillance de la qualité de l'air. Le projet est
construit progressivement ; cette première étape fournit PostgreSQL en local.

## Démarrer PostgreSQL

Depuis la racine du dépôt, copier `.env.example` vers `.env`, puis remplacer le
mot de passe d'exemple par une valeur locale. Démarrer le service :

```powershell
Copy-Item .env.example .env
docker compose -f infra/docker-compose.yml up -d
docker compose -f infra/docker-compose.yml ps
```

Le schéma initial est créé au premier démarrage dans la base configurée. Pour
arrêter PostgreSQL sans supprimer les données :

```powershell
docker compose -f infra/docker-compose.yml down
```

Les variables de connexion sont décrites dans `.env.example`. Le volume nommé
`postgres_data` conserve les données entre les redémarrages.
