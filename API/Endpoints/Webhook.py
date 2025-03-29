from flask import Blueprint, request
import os
import dotenv
#Validando Webhook
dotenv.load_dotenv()
webhook_bp = Blueprint('webhook', __name__)



VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

@webhook_bp.route('/webhook', methods=['GET'])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    
    if mode and token:
        if mode == "subscribe" and token == VERIFY_TOKEN:
            print("Webhook verificado com sucesso!")
            return challenge, 200
        else:
            return "Token de verificação inválido", 403
    return "Requisição inválida", 400
