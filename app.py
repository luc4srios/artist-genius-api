from flask import Flask
from flask_restx import Api
from src.routes.music_routes import api_ns

app = Flask(__name__)
api = Api(app, version='1.0', 
          title='API Genius', 
          description='API para buscar as 10 músicas mais populares de um artista usando Genius',
          doc='/docs/')

api.add_namespace(api_ns, path='/musicas')

if __name__ == "__main__":
    app.run(debug=True)