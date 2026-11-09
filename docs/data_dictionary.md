# Dictionnaire de données — Phase 1

| Table | Rôle | Champs principaux |
|---|---|---|
| `sensors` | Référentiel des capteurs | `sensor_id` (clé), `location`, `created_at` |
| `air_quality_measurements` | Mesures horodatées | identifiant, capteur, date de mesure, lieu, polluants, température, humidité |
| `anomalies` | Anomalies rattachées à une mesure | mesure, date de détection, règle, gravité, description |
| `model_predictions` | Prédictions historisées | capteur optionnel, date, modèle/version, résultat, score, caractéristiques JSON |

Les mesures utilisent `TIMESTAMPTZ` pour conserver un instant non ambigu. Les
valeurs de mesure restent nullable afin de représenter des données manquantes ;
les contrôles métier et les valeurs aberrantes relèvent du pipeline de traitement.
La paire capteur/instant est unique pour rendre les écritures rejouables.
