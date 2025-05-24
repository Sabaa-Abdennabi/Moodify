import random
import time
import json
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from kafka import KafkaProducer

# --- Paramètres à renseigner ---
CLIENT_ID = "734aafef80964f24ab1e2754d7e6958c"
CLIENT_SECRET = "3f28a87d472b49b6a8c3d8eec1ffa7be"
REDIRECT_URI = "https://384e-197-14-206-17.ngrok-free.app"
SCOPE = "user-read-currently-playing user-read-playback-state"

# --- Création de l'authentification OAuth ---
sp_oauth = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE,
    cache_path=".cache"  # fichier pour stocker le token et refresh token
)

# --- Obtenir un token valide (ouvre le navigateur la 1ère fois) ---
token_info = sp_oauth.get_access_token(as_dict=True)
print("Token info:", token_info)
if not token_info:
    print("❌ Aucun token trouvé dans .cache. Lance une auth d'abord.")
    exit()

if sp_oauth.is_token_expired(token_info):
    token_info = sp_oauth.refresh_access_token(token_info["refresh_token"])

access_token = token_info["access_token"]
print("Token d'accès :", access_token)
# --- Créer l'objet Spotify avec token d'accès ---
sp = Spotify(auth=access_token)

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

print("Démarrage du monitoring des morceaux écoutés en temps réel...")

# --- Boucle infinie pour lire la musique en cours toutes les 5 secondes ---
while True:
    try:
        if sp_oauth.is_token_expired(token_info):
            token_info = sp_oauth.refresh_access_token(token_info["refresh_token"])
            sp = Spotify(auth=token_info["access_token"])

        current = sp.current_user_playing_track()
        if current and current['item']:
            track = current["item"]

            if track["type"] != "track":
                print("⚠️ Ce n'est pas un morceau standard. Type:", track["type"])
                continue

            features = {
                "valence": 0.8,
                "energy": 0.8,
                "danceability": 0.8,
                "acousticness": random.uniform(0, 1),
                "instrumentalness": random.uniform(0, 1),
                "speechiness": random.uniform(0, 1)
            }
            print(features)

            if features is None:
                print("⚠️ Pas de features pour ce morceau.")
                continue

            track_data = {
                "user_id": "user_001",
                "track_id": track["id"],
                "track_name": track["name"],
                "valence": features["valence"],
                "energy": features["energy"],
                "danceability": features["danceability"],
                "acousticness": features["acousticness"],
                "instrumentalness": features["instrumentalness"],
                "speechiness": features["speechiness"],
                "duration_ms": track["duration_ms"],
                "timestamp": str(int(time.time()))
            }
            print("🎶 Morceau en cours :" ,track_data )
            producer.send("spotify-stream", value=track_data)
            print(f"Sent to Kafka: {track['id']}, {"user_id"}")
        else:
            print("Aucun morceau en lecture actuellement.")
    except Exception as e:
        print("Erreur :", e)

    time.sleep(10)

