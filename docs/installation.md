# Installation locale — Phase 1

## Prérequis

- Docker Desktop avec Docker Compose v2
- Git

## PostgreSQL

À la racine du dépôt, créez le fichier local `.env` à partir de `.env.example`
et définissez un mot de passe adapté à votre machine. Puis lancez :

```powershell
docker compose -f infra/docker-compose.yml up -d
docker compose -f infra/docker-compose.yml ps
```

Le service devient sain lorsque `pg_isready` confirme la disponibilité. Le
script `sql/init.sql` s'exécute automatiquement uniquement lors de la première
initialisation du volume `postgres_data`. Les modifications ultérieures du
schéma nécessiteront une migration dédiée.

Arrêt sans perte de données :

```powershell
docker compose -f infra/docker-compose.yml down
```

La suppression du volume efface les données locales ; ne l'utilisez que si vous
souhaitez réinitialiser explicitement la base.
