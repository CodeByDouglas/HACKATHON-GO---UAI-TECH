from flask import request
from .Webhook import webhook_bp
from API.Utility.Mensagens import *
from API.Utility.Message_output import send_whatsapp_message
from API.Utility.Sessao import iniciar_sessao, obter_sessao, fechar_sessao, atualizar_etapa 
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
       
        match etapa:
            case "seleção inicial":
                # Extrai o texto da mensagem para processar a resposta
                mensagem = Corpo_da_mensagem["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
                if mensagem == "1":
                    send_whatsapp_message(user_number, Pedir_cep_coleta_organica)
                    
                    atualizar_etapa(user_number, "Aguardando cep coleta organica")
                elif mensagem == "2":
                    send_whatsapp_message(user_number, Pedir_cep_coleta_seletiva)
                    
                    atualizar_etapa(user_number, "Aguardando cep coleta seletiva")
                  
                elif mensagem == "3":
                    send_whatsapp_message(user_number, Menu_descarte_de_residuos)
                    
                    atualizar_etapa(user_number, "Aguardando Descarte")
                  
                elif mensagem == "4":
                    send_whatsapp_message(user_number, Menu_denuncia)
                    
                    atualizar_etapa(user_number, "Selecionar topico denuncia")
                  
           
            case "Aguardando cep coleta organica": 
                mensagem = Corpo_da_mensagem["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
                if mensagem == "777":
                    send_whatsapp_message(user_number, Sucesso_coleta_oraganica)
                    fechar_sessao(user_number)
                elif mensagem == "1": 
                    send_whatsapp_message(user_number, Menssagem_de_encerramento )
                    fechar_sessao(user_number)
                else: 
                    send_whatsapp_message(user_number, Cep_invalido)
            
            case "Aguardando cep coleta seletiva": 
                mensagem = Corpo_da_mensagem["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
                if mensagem == "888":
                    send_whatsapp_message(user_number, Sucesso_colete_seletiva)
                    fechar_sessao(user_number)
                elif mensagem == "1": 
                    send_whatsapp_message(user_number, Menssagem_de_encerramento )
                    fechar_sessao(user_number)
                else: 
                    send_whatsapp_message(user_number, Cep_invalido)
            
            case "Aguardando Descarte": 
                mensagem = Corpo_da_mensagem["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
                if mensagem == "1":
                    send_whatsapp_message(user_number, Pedir_cep_ecoponto)
                    atualizar_etapa(user_number, "Aguardando cep ecoponto")

                elif mensagem == "2":
                    send_whatsapp_message(user_number, Menu_material_de_descarte)
                    atualizar_etapa(user_number, "selecionando material")
                
                elif mensagem == "3":
                    send_whatsapp_message(user_number, Menu_programas_da_prefeitura)
                    atualizar_etapa(user_number, "Aguardando programa da prefeitura")

            case "Aguardando cep ecoponto": 
                mensagem = Corpo_da_mensagem["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
                if mensagem == "999":
                    send_whatsapp_message(user_number, Sucesso_ecoponto)
                    fechar_sessao(user_number)
                elif mensagem == "1": 
                    send_whatsapp_message(user_number, Menssagem_de_encerramento )
                    fechar_sessao(user_number)
                else: 
                    send_whatsapp_message(user_number, Cep_invalido)




            case "selecionando material":
                mensagem = Corpo_da_mensagem["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
                if mensagem == "1": 
                    send_whatsapp_message(user_number, Pedir_cep_empresa_parceira)
                    atualizar_etapa(user_number, "Aguardando cep metal")
                elif mensagem == "2": 
                    send_whatsapp_message(user_number, Pedir_cep_empresa_parceira)
                    atualizar_etapa(user_number, "Aguardando cep vidro")
                elif mensagem == "3": 
                    send_whatsapp_message(user_number, Pedir_cep_empresa_parceira)
                    atualizar_etapa(user_number, "Aguardando cep papel")
                elif mensagem == "4": 
                    send_whatsapp_message(user_number, Pedir_cep_empresa_parceira)
                    atualizar_etapa(user_number, "Aguardando cep plastico")

            case "Aguardando cep metal":
                mensagem = Corpo_da_mensagem["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
                if mensagem == "555":
                    send_whatsapp_message(user_number, Sucesso_descarte_empresa_parceira)
                    fechar_sessao(user_number)
                elif mensagem == "1": 
                    send_whatsapp_message(user_number, Menssagem_de_encerramento )
                    fechar_sessao(user_number)
                else: 
                    send_whatsapp_message(user_number, Cep_invalido)
           
            case "Aguardando cep vidro":
                mensagem = Corpo_da_mensagem["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
                if mensagem == "555":
                    send_whatsapp_message(user_number, Sucesso_descarte_empresa_parceira)
                    fechar_sessao(user_number)
                elif mensagem == "1": 
                    send_whatsapp_message(user_number, Menssagem_de_encerramento )
                    fechar_sessao(user_number)
                else: 
                    send_whatsapp_message(user_number, Cep_invalido)
           
            case "Aguardando cep papel":
                mensagem = Corpo_da_mensagem["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
                if mensagem == "555":
                    send_whatsapp_message(user_number, Sucesso_descarte_empresa_parceira)
                    fechar_sessao(user_number)
                elif mensagem == "1": 
                    send_whatsapp_message(user_number, Menssagem_de_encerramento )
                    fechar_sessao(user_number)
                else: 
                    send_whatsapp_message(user_number, Cep_invalido)
            
            case "Aguardando cep plastico":
                mensagem = Corpo_da_mensagem["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
                if mensagem == "555":
                    send_whatsapp_message(user_number, Sucesso_descarte_empresa_parceira)
                    fechar_sessao(user_number)
                elif mensagem == "1": 
                    send_whatsapp_message(user_number, Menssagem_de_encerramento )
                    fechar_sessao(user_number)
                else: 
                    send_whatsapp_message(user_number, Cep_invalido)
           
            case "Selecionar topico denuncia": 
                mensagem = Corpo_da_mensagem["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
                if mensagem == "1":
                    send_whatsapp_message(user_number, Descarte_irregular_de_lixo)
                    atualizar_etapa(user_number, "Aguardando a Denuncia")

            case "Aguardando a Denuncia":
                mensagem = Corpo_da_mensagem["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
                send_whatsapp_message(user_number,Sucesso_denuncia)
                fechar_sessao(user_number)

            case "Aguardando programa da prefeitura":
                mensagem = Corpo_da_mensagem["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
                if mensagem == "1": 
                    send_whatsapp_message(user_number, Confirmacao_Catatreco)
                    atualizar_etapa(user_number, "Confirmar catatreco")
                if mensagem == "2": 
                    send_whatsapp_message(user_number, Confirmacao_sukatech)
                    atualizar_etapa(user_number, "Confirmar sukatech")
            
            case "Confirmar catatreco": 
                mensagem = Corpo_da_mensagem["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
                if mensagem == "endereço":
                    send_whatsapp_message(user_number, Sucesso_cata_treco)
                    fechar_sessao(user_number)
            
            case "Confirmar sukatech": 
                mensagem = Corpo_da_mensagem["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
                if mensagem == "endereço":
                    send_whatsapp_message(user_number, Sucesso_sukatech)
                    fechar_sessao(user_number)

            


                
    
    return "Ok", 200