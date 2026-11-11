# Air Quality DataOps/MLOps

Plateforme universitaire de surveillance de la qualité de l'air. Le projet est
construit progressivement ; les premières étapes fournissent PostgreSQL, Kafka
et un simulateur de capteurs en local.

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

Kafka démarre en mode KRaft avec un listener externe sur `localhost:9092` et un
listener interne pour les services Compose. Les topics `raw_data`,
`processed_data` et `anomalies` sont créés au démarrage. Cette configuration à
un seul broker est destinée au développement et à la démonstration locale.

## Simuler les capteurs

Installer les dépendances Python puis lancer le producteur depuis la racine :

```powershell
python -m pip install -r requirements.txt
python -m src.ingestion.producer
```

Le producteur envoie un événement JSON par seconde dans `raw_data` par défaut.
Les paramètres `KAFKA_BOOTSTRAP_SERVERS`, `KAFKA_TOPIC` et
`PRODUCER_INTERVAL_SECONDS` peuvent être définis dans l'environnement. Arrêter
avec `Ctrl+C`.
