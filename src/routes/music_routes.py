from flask import Blueprint, request, jsonify
from src.services.genius import get_songs
#from src.services.redis import get_cache, set_cache, clear_cache
#from src.services.dynamo import save_dynamo
import uuid

music_bp = Blueprint("music_bp", __name__)

@music_bp.route("/musicas", methods=["GET"])
def get_musicas():
    artista = request.args.get("artista")
    usar_cache = request.args.get("cache", "true").lower() == "true"
    transaction_id = str(uuid.uuid4())   
    
    if not artista:
        return jsonify({"erro": "Informe o nome do artista"}), 400

    musicas = get_songs(artista)

    if not musicas:
        return jsonify({
            "transaction_id": transaction_id,
            "erro": f"Nao foi encontrado nenhuma musica para o artista informado: '{artista}'"
        }), 404

    return jsonify({
        "transaction_id": transaction_id,
        "data": musicas,
        "fonte": "genius"
    })