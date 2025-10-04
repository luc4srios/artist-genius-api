from flask import Flask
from src.routes.music_routes import music_bp

app = Flask(__name__)
app.register_blueprint(music_bp)

if __name__ == "__main__":
    app.run(debug=True)