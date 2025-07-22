# Moodify  
*Analyse d’Humeur Musicale en Temps Réel*  

---

## 1. Objectif du Projet

Créer une plateforme intelligente qui analyse en temps réel l’humeur des musiques jouées par un utilisateur via Spotify, et recommande des titres selon l’émotion musicale détectée chaque semaine.

---

## 2. Sources de Données

- **Streaming :** Spotify Web API  
  - `/me/player/currently-playing` : Titre en cours  
  - `/me/player/recently-played` : Historique  
  - `/audio-features/{track_id}` : Valence, énergie, danseabilité, etc.

- **Batch :** Dataset Kaggle  
  - [Spotify Music Dataset](https://www.kaggle.com/datasets/solomonameh/spotify-music-dataset)

---

## 3. Architecture Big Data

### A. Ingestion

- **Streaming :**  
  Un script Python (cron toutes les 30s ou 1min) interroge l’API Spotify et envoie les données vers Kafka.

- **Batch :**  
  Le dataset Kaggle est traité initialement avec PySpark pour les recommandations futures.  
  Une exécution hebdomadaire analyse l’historique des utilisateurs pour produire des statistiques d’humeur et préparer les recommandations personnalisées.

### B. Traitement

- **Streaming :**  
  Spark Streaming récupère les JSON en entrée (via API simulée), calcule le mood, et sauvegarde les données dans Mongo.

- **Batch :**  
  Script PySpark pour :  
  - Classifier le dataset Kaggle selon les valeurs de valence, énergie, danseabilité, etc.  
  - Analyser l’historique hebdomadaire des utilisateurs pour inférer leurs préférences et affiner les recommandations.

### C. Stockage

- **MongoDB :** Stockage des morceaux joués, moods, et historiques d’écoute sous format JSON structuré.

### D. Visualisation

- **Dashboard React :**  
  - Graphiques en temps réel (barres, radar, cercle chromatique)  
  - Liste des musiques classées par émotion dominante  
  - Analyses globales et par utilisateur  
  - Recommandations basées sur les humeurs récentes et historiques

---

## 4. Stack Technique

| Composant  | Outil                  |
|------------|------------------------|
| Ingestion  | Python script + Kafka  |
| Streaming  | Spark Streaming        |
| Batch      | PySpark                |
| Stockage   | MongoDB                |
| Visualisation | React               |


