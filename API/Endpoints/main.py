from flask import request
from .Webhook import webhook_bp
from API.Utility.Mensagens import (
    Menu_inicial,
    Pedir_cep_coleta_organica,
    Pedir_cep_coleta_seletiva,
    Menu_descarte_de_residuos,
    Menu_denuncia,
    Cep_invalido,
    Sucesso_coleta_oraganica,
    Sucesso_ecoponto,
    Sucesso_descarte_empresa_parceira,
    Descarte_irregular_de_lixo,
    Sucesso_denuncia,
    Menu_programas_da_prefeitura,
    Confirmacao_Catatreco,
    Confirmacao_sukatech,
    Sucesso_cata_treco,
    Sucesso_sukatech,
    Pedir_cep_ecoponto,
    Pedir_cep_empresa_parceira,
    Menssagem_de_encerramento,
    Sucesso_coleta_seletiva, 
    Menu_material_de_descarte,
    Inicio_coleta_cep, 
    continuidade
)
from API.Utility.Envio_mensagem import send_whatsapp_message
from API.Utility.Sessao import iniciar_sessao, obter_sessao, fechar_sessao, atualizar_etapa, atualizar_cep, obter_cep
from API.Utility.Validar_Cep import cep_valido
from API.Utility.Buscar_Cep import consultar_coleta_organica, consultar_coleta_seletiva


@webhook_bp.route('/webhook', methods=['POST'])
def fluxo_de_conversa():
    # Recebe o JSON do webhook
    corpo = request.get_json()
    change_value = corpo["entry"][0]["changes"][0]["value"]

    # Se não houver "messages", trata eventos de status ou JSON inesperado e retorna
    if "messages" not in change_value:
        if "statuses" in change_value:
            status_info = change_value["statuses"][0]
            print("Recebi um evento de status:", status_info)
        else:
            print("JSON em formato inesperado:", change_value)
        return "Ok", 200

    # Extração dos dados da mensagem
    user_number = change_value["messages"][0]["from"]
    mensagem_texto = change_value["messages"][0]["text"]["body"].strip().lower()

    # Verifica se já existe uma sessão para o usuário
    sessao = obter_sessao(user_number)
    if sessao is None:
        iniciar_sessao(user_number)
        send_whatsapp_message(user_number, Inicio_coleta_cep)
        return "Ok", 200

    # Processa o fluxo com base na etapa da sessão
    match sessao:
        case "incerir_cep":
            if cep_valido(mensagem_texto):
                send_whatsapp_message(user_number, Menu_inicial)
                atualizar_etapa(user_number, "seleção inicial")
                atualizar_cep(user_number, mensagem_texto)
            elif mensagem_texto == "1": 
                send_whatsapp_message(user_number,  Menssagem_de_encerramento)
                fechar_sessao(user_number)
            else:
                send_whatsapp_message(user_number, Cep_invalido)
        
        case "seleção inicial":
            if mensagem_texto == "1":
                send_whatsapp_message(user_number, consultar_coleta_organica(obter_cep(user_number)))
                send_whatsapp_message(user_number, continuidade)
                atualizar_etapa(user_number, "continua")
            elif mensagem_texto == "2":
                send_whatsapp_message(user_number, consultar_coleta_seletiva(obter_cep(user_number)))
                send_whatsapp_message(user_number, continuidade)
                atualizar_etapa(user_number, "continua")
            elif mensagem_texto == "3":
                send_whatsapp_message(user_number, Menu_descarte_de_residuos)
                atualizar_etapa(user_number, "Aguardando Descarte")
            elif mensagem_texto == "4":
                send_whatsapp_message(user_number, Menu_denuncia)
                atualizar_etapa(user_number, "Selecionar topico denuncia")

        case "continua":
            if mensagem_texto == "1":
                send_whatsapp_message(user_number, Menu_inicial)
                atualizar_etapa(user_number, "seleção inicial")
            elif mensagem_texto == "2":
                send_whatsapp_message(user_number, Menssagem_de_encerramento)
                fechar_sessao(user_number)
        
        case "Aguardando Descarte":
            if mensagem_texto == "1":
                send_whatsapp_message(user_number, Pedir_cep_ecoponto)
                atualizar_etapa(user_number, "Aguardando cep ecoponto")
            elif mensagem_texto == "2":
                send_whatsapp_message(user_number, Menu_material_de_descarte)
                atualizar_etapa(user_number, "selecionando material")
            elif mensagem_texto == "3":
                send_whatsapp_message(user_number, Menu_programas_da_prefeitura)
                atualizar_etapa(user_number, "Aguardando programa da prefeitura")

        case "Aguardando cep ecoponto":
            if mensagem_texto == "999":
                send_whatsapp_message(user_number, Sucesso_ecoponto)
                fechar_sessao(user_number)
            elif mensagem_texto == "1":
                send_whatsapp_message(user_number, Menssagem_de_encerramento)
                fechar_sessao(user_number)
            else:
                send_whatsapp_message(user_number, Cep_invalido)

        case "selecionando material":
            if mensagem_texto == "1":
                send_whatsapp_message(user_number, Pedir_cep_empresa_parceira)
                atualizar_etapa(user_number, "Aguardando cep metal")
            elif mensagem_texto == "2":
                send_whatsapp_message(user_number, Pedir_cep_empresa_parceira)
                atualizar_etapa(user_number, "Aguardando cep vidro")
            elif mensagem_texto == "3":
                send_whatsapp_message(user_number, Pedir_cep_empresa_parceira)
                atualizar_etapa(user_number, "Aguardando cep papel")
            elif mensagem_texto == "4":
                send_whatsapp_message(user_number, Pedir_cep_empresa_parceira)
                atualizar_etapa(user_number, "Aguardando cep plastico")

        case "Aguardando cep metal":
            if mensagem_texto == "555":
                send_whatsapp_message(user_number, Sucesso_descarte_empresa_parceira)
                fechar_sessao(user_number)
            elif mensagem_texto == "1":
                send_whatsapp_message(user_number, Menssagem_de_encerramento)
                fechar_sessao(user_number)
            else:
                send_whatsapp_message(user_number, Cep_invalido)

        case "Aguardando cep vidro":
            if mensagem_texto == "555":
                send_whatsapp_message(user_number, Sucesso_descarte_empresa_parceira)
                fechar_sessao(user_number)
            elif mensagem_texto == "1":
                send_whatsapp_message(user_number, Menssagem_de_encerramento)
                fechar_sessao(user_number)
            else:
                send_whatsapp_message(user_number, Cep_invalido)

        case "Aguardando cep papel":
            if mensagem_texto == "555":
                send_whatsapp_message(user_number, Sucesso_descarte_empresa_parceira)
                fechar_sessao(user_number)
            elif mensagem_texto == "1":
                send_whatsapp_message(user_number, Menssagem_de_encerramento)
                fechar_sessao(user_number)
            else:
                send_whatsapp_message(user_number, Cep_invalido)

        case "Aguardando cep plastico":
            if mensagem_texto == "555":
                send_whatsapp_message(user_number, Sucesso_descarte_empresa_parceira)
                fechar_sessao(user_number)
            elif mensagem_texto == "1":
                send_whatsapp_message(user_number, Menssagem_de_encerramento)
                fechar_sessao(user_number)
            else:
                send_whatsapp_message(user_number, Cep_invalido)

        case "Selecionar topico denuncia":
            if mensagem_texto == "1":
                send_whatsapp_message(user_number, Descarte_irregular_de_lixo)
                atualizar_etapa(user_number, "Aguardando a Denuncia")

        case "Aguardando a Denuncia":
            send_whatsapp_message(user_number, Sucesso_denuncia)
            fechar_sessao(user_number)

        case "Aguardando programa da prefeitura":
            if mensagem_texto == "1":
                send_whatsapp_message(user_number, Confirmacao_Catatreco)
                atualizar_etapa(user_number, "Confirmar catatreco")
            elif mensagem_texto == "2":
                send_whatsapp_message(user_number, Confirmacao_sukatech)
                atualizar_etapa(user_number, "Confirmar sukatech")

        case "Confirmar catatreco":
            if mensagem_texto == "endereço":
                send_whatsapp_message(user_number, Sucesso_cata_treco)
                fechar_sessao(user_number)

        case "Confirmar sukatech":
            if mensagem_texto == "endereço":
                send_whatsapp_message(user_number, Sucesso_sukatech)
                fechar_sessao(user_number)

    return "Ok", 200
