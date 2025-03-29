from flask import request
from .Webhook import webhook_bp
from API.Utility.Mensagens import Menu_inicial, Pedir_cep_coleta_organica, Pedir_cep_coleta_seletiva
from API.Utility.Message_output import send_whatsapp_message
from Sessao import iniciar_sessao, obter_sessao, fechar_sessao, atualizar_etapa # Renomeie para 'Sessao' sem acentos

@webhook_bp.route('/webhook', methods=['POST'])
def Fluxo_de_Conversa():
    Corpo_da_mensagem = request.get_json()
    change_value = Corpo_da_mensagem["entry"][0]["changes"][0]["value"]
    
    user_number = None  # Inicializa a variável para garantir que ela seja definida
    
    if "messages" in change_value:
        # Extrai o número do usuário quando o evento é uma mensagem
        user_number = change_value["messages"][0]["from"]
        
    elif "statuses" in change_value:
        # Se for um evento de status, registra o evento
        status_info = change_value["statuses"][0]
        print("Recebi um evento de status:", status_info)
        # Se possível, tenta extrair o número do destinatário do status
        if "recipient_id" in status_info:
            user_number = status_info["recipient_id"]
        else:
            return "Ok", 200
    else:
        print("JSON em formato inesperado:", change_value)
        return "Ok", 200

    # Verifica se o usuário já possui uma sessão ativa
    if obter_sessao(user_number) is None:
        iniciar_sessao(user_number)
        send_whatsapp_message(user_number, Menu_inicial)
    else:
        etapa = obter_sessao(user_number)
        # A sintaxe match-case requer Python 3.10 ou superior
        match etapa:
            case "seleção inicial":
                # Extrai o texto da mensagem para processar a resposta
                mensagem = Corpo_da_mensagem["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
                if mensagem == "1":
                    send_whatsapp_message(user_number, Pedir_cep_coleta_organica)
                    
                    atualizar_etapa(user_number, "aguardandocepcoletaorganica")
                elif mensagem == "2":
                    send_whatsapp_message(user_number, Pedir_cep_coleta_seletiva)
                    
                    atualizar_etapa(user_number, "aguardandocepcoletaseletiva")
                  
           
            case "aguardandocepcoletaorganica": 
                mensagem = Corpo_da_mensagem["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
                if mensagem == "777":
                    send_whatsapp_message(user_number, "sua coleta é tal dia")
                    fechar_sessao(user_number)
            
            case "aguardandocepcoletaseletiva": 
                mensagem = Corpo_da_mensagem["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
                if mensagem == "888":
                    send_whatsapp_message(user_number, "sua coleta seletiva é tal dia")
                    fechar_sessao(user_number)

                
    
    return "Ok", 200