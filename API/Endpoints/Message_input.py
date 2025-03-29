# messages.py
from flask import request
from .Webhook import webhook_bp
from API.outbound.Message_output import send_whatsapp_message  # Importa a função

@webhook_bp.route('/webhook', methods=['POST'])
def handle_incoming_messages():
    data = request.get_json()
    print("Mensagem recebida:", data)

    # Extraindo o número do remetente e o texto
    try:
        # Exemplo de caminhos no JSON:
        changes = data["entry"][0]["changes"]
        value = changes[0]["value"]
        messages = value["messages"]
        sender = messages[0]["from"]  # "5562999999999"
        text_body = messages[0]["text"]["body"]
        
        # Responder o usuário
        resposta = f"Você disse: {text_body}"
        send_whatsapp_message(sender, resposta)
    except KeyError:
        print("JSON em formato inesperado, não foi possível extrair dados.")

    return "Ok", 200

#Padrão sem resposta: 

# from flask import request
# from .Webhook import webhook_bp

# @webhook_bp.route('/webhook', methods=['POST'])
# def handle_incoming_messages():
#     data = request.get_json()
#     print("Mensagem recebida:", data)
#     return "Ok", 200