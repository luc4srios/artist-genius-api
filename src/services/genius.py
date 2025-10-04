from dotenv import load_dotenv
import requests
import os

load_dotenv()
GENIUS_API_TOKEN = os.getenv("GENIUS_API_TOKEN")
HEADERS = {"Authorization": f"Bearer {GENIUS_API_TOKEN}"}

if not GENIUS_API_TOKEN:
    raise ValueError("genius_api_token não foi configurada")

def get_songs(artista, max_results=10):
    url = "https://api.genius.com/search"
    params = {"q": artista}

    response = requests.get(url, headers=HEADERS, params=params)

    if response.status_code != 200:
        return {"erro": "Falha na requisicao Genius ({response.status_code})"}
    
    data = response.json()
    hits = data["response"]["hits"]

    musicas = []
    for hit in hits[:max_results]:
        musica = {
            "title": hit["result"]["title"],
            "url": hit["result"]["url"]
        }
        musicas.append(musica)

    return musicas