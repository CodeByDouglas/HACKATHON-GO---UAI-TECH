import dotenv
import requests
import os

dotenv.load_dotenv()

WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

def send_whatsapp_message(to, message):
    """
    Envia uma mensagem de texto simples (session message)
    para o usuário 'to' via WhatsApp Cloud API.
    """
    url = f"https://graph.facebook.com/v16.0/{PHONE_NUMBER_ID}/messages"
    
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messaging_product": "whatsapp",
        "to": to,  # número do destinatário no formato E.164 (ex: '5562999999999')
        "type": "text",
        "text": {
            "body": message
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        print("✅ Mensagem enviada com sucesso.")
    else:
        print(f"❌ Erro ao enviar mensagem: {response.status_code}")
        print(response.json())

    return response
