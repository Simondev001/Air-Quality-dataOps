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

PostgreSQL devient sain lorsque `pg_isready` confirme sa disponibilité. Le
script `sql/init.sql` s'exécute automatiquement uniquement lors de la première
initialisation du volume `postgres_data`. Les modifications ultérieures du
schéma nécessiteront une migration dédiée.

Kafka fonctionne en mode KRaft avec un seul broker. Après son contrôle de
santé, le service `kafka-init` crée `raw_data`, `processed_data` et `anomalies`.
Les applications lancées sur l'hôte utilisent `localhost:9092`; les services
dans Compose utilisent le listener interne `kafka:9094`.

Pour installer et lancer le simulateur :

```powershell
python -m pip install -r requirements.txt
python -m src.ingestion.producer
```

Le producteur cible `localhost:9092` et publie dans `raw_data` par défaut.
Configurez les variables d'environnement correspondantes pour changer ces
valeurs.

Arrêt sans perte de données :

```powershell
docker compose -f infra/docker-compose.yml down
```

La suppression du volume efface les données locales ; ne l'utilisez que si vous
souhaitez réinitialiser explicitement la base.
