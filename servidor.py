from flask import Flask
from API.Endpoints.Webhook import webhook_bp
import API.Endpoints.Message_input

app = Flask(__name__)

app.register_blueprint(webhook_bp)

@app.route('/')
def home():
    return "Olá, mundo! Esse é o Zeco Lógico"

if __name__ == "__main__":
    app.run(debug=True)
