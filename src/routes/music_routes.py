from flask_restx import Namespace, Resource, fields
from src.services.genius import get_songs
from src.services.redis import get_cache, set_cache, clear_cache
from src.services.dynamo import save_dynamo
import uuid
import time

api_ns = Namespace('musicas', description='Operações de músicas')

musica_model = api_ns.model('Musica', {
    'title': fields.String(required=True, description='Título da música'),
    'url': fields.String(required=True, description='URL da música')
})

resposta_model = api_ns.model('Resposta', {
    'transaction_id': fields.String(description='ID da transação'),
    'data': fields.List(fields.Nested(musica_model)),
    'fonte': fields.String(description='Fonte da informação (cache ou genius)')
})

@api_ns.route('')
class Musicas(Resource):
    @api_ns.doc(
        params={
            'artista': 'Nome do artista (usar "-" quando houver espaço)',
            'cache': 'Forçar cache (true/false, padrão true)'
        },
        responses={
            200: 'Sucesso',
            400: "Parâmetro 'artista' é obrigatório",
            404: "Nenhuma música encontrada para o artista"
        }
    )
    @api_ns.marshal_with(resposta_model)
    def get(self):
        artista = api_ns.payload.get("artista") if api_ns.payload else None
        from flask import request
        artista = request.args.get("artista")
        usar_cache = request.args.get("cache", "true").lower() == "true"

        if not artista:
            return {
                "transaction_id": str(uuid.uuid4()),
                "data": [],
                "fonte": f"O parâmetro 'artista' é obrigatório."
            }, 400

        transaction_id = str(uuid.uuid4())

        if usar_cache:
            cached_data = get_cache(artista)
            if cached_data:
                return {
                    "transaction_id": transaction_id,
                    "data": cached_data,
                    "fonte": "cache"
                }

        if not usar_cache:
            clear_cache(artista)

        musicas = get_songs(artista)
        if not musicas:
            return {
                "transaction_id": transaction_id,
                "data": [],
                "fonte": f"Nenhuma música encontrada para '{artista}'"
            }, 404

        payload = {
            "transaction_id": transaction_id,
            "artista": artista,
            "musicas": musicas,
            "timestamp": int(time.time()),
            "fonte": "genius"
        }
        save_dynamo(payload)

        set_cache(artista, musicas)

        return {
            "transaction_id": transaction_id,
            "data": musicas,
            "fonte": "genius"
        }