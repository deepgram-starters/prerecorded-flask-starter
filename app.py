import json
from flask import Flask, jsonify, request, abort, make_response
from deepgram import Deepgram
import os
from dotenv import load_dotenv
from flask_cors import CORS

# Загрузка переменных окружения
load_dotenv()

# Создание Flask-приложения
app = Flask(__name__, static_folder="./static", static_url_path="/")

# Добавляем middleware для поддержки обратного прокси
class ReverseProxied:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        scheme = environ.get('HTTP_X_FORWARDED_PROTO', 'http')
        if scheme:
            environ['wsgi.url_scheme'] = scheme

        host = environ.get('HTTP_X_FORWARDED_HOST', '')
        if host:
            environ['HTTP_HOST'] = host

        return self.app(environ, start_response)

app.wsgi_app = ReverseProxied(app.wsgi_app)

# Устанавливаем SERVER_NAME из переменной окружения
if os.getenv('SERVER_NAME'):
    app.config['SERVER_NAME'] = os.getenv('SERVER_NAME')

# Инициализация Deepgram
deepgram = Deepgram(os.environ.get("DEEPGRAM_API_KEY"))

# Настройка CORS
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# Маршрут для главной страницы
@app.route("/", methods=["GET"])
def index():
    return app.send_static_file("index.html")

# Маршрут для транскрибации
@app.route("/api", methods=["POST"])
async def transcribe():
    form = request.form
    files = request.files
    url = form.get("url")
    features = form.get("features")
    model = form.get("model")
    version = form.get("version")
    tier = form.get("tier")

    dgFeatures = json.loads(features)
    dgRequest = None

    try:
        if url and url.startswith("https://res.cloudinary.com/deepgram"):
            dgRequest = {"url": url}

        if "file" in files:
            file = files.get("file")
            dgRequest = {"mimetype": file.mimetype, "buffer": file.stream.read()}

        dgFeatures["model"] = model

        if version:
            dgFeatures["version"] = version

        if model == "whisper":
            dgFeatures["tier"] = tier

        if not dgRequest:
            raise Exception(
                "Error: You need to choose a file to transcribe your own audio."
            )

        transcription = await deepgram.transcription.prerecorded(dgRequest, dgFeatures)

        return jsonify(
            {
                "model": model,
                "version": version,
                "tier": tier,
                "dgFeatures": dgFeatures,
                "transcription": transcription,
            }
        )
    except Exception as error:
        return json_abort(error)

# Обработка ошибок
def json_abort(message):
    print(message)
    return abort(make_response(jsonify(err=str(message)), 500))

# Запуск приложения
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
