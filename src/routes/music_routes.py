from flask import Blueprint, request, jsonify
from src.services.genius import get_songs
from src.services.redis import get_cache, set_cache, clear_cache
from src.services.dynamo import save_dynamo
import uuid
import time

music_bp = Blueprint("music_bp", __name__)

@music_bp.route("/musicas", methods=["GET"])
def get_musicas():
    artista = request.args.get("artista")
    usar_cache = request.args.get("cache", "true").lower() == "true"
    
    if not artista:
        return jsonify({"erro": "O parâmetro 'artista' é obrigatório."}), 400

    if usar_cache:
        cached_data = get_cache(artista)
        if cached_data:
            transaction_id = str(uuid.uuid4())
            return jsonify({
                "transaction_id": transaction_id, 
                "data": cached_data,
                "fonte": "cache"
            })

    if not usar_cache:
        clear_cache(artista)
        transaction_id = str(uuid.uuid4())
    else:
        transaction_id = str(uuid.uuid4())

    musicas = get_songs(artista)

    if not musicas:
        return jsonify({
            "transaction_id": transaction_id,
            "erro": f"Nao foi encontrado nenhuma musica para o artista informado: '{artista}'"
        }), 404

    payload = {
        "transaction_id": transaction_id,
        "artista": artista,
        "musicas": musicas,
        "timestamp": int(time.time()),
        "fonte": "genius"
    }

    save_dynamo(payload)
    set_cache(artista, musicas, transaction_id)

    return jsonify({
        "transaction_id": transaction_id,
        "data": musicas,
        "fonte": "genius"
    })