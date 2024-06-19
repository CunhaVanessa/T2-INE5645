import socket
import threading
import json
import time
import random
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ------------------- Funções de Configuração -------------------

def carregar_configuracao_particoes():
    with open('configuracoes/configuracao_particoes.json', 'r') as f:
        return json.load(f)

def carregar_configuracao_cliente():
    with open('configuracoes/configuracao_cliente.json', 'r') as f:
        return json.load(f)

def carregar_dados_dns(letra_particao):
    with open(f'particoes/particao_{letra_particao}.json', 'r') as f:
        return json.load(f)

# ------------------- Funções do Roteador (API Gateway) -------------------

def autenticar(token):
    token_correto = "secreto"
    return token == token_correto

def determinar_particao(nome_dominio, particoes):
    primeira_letra = nome_dominio[0].upper()
    for particao, config in particoes.items():
        if config['intervalo'][0] <= primeira_letra <= config['intervalo'][1]:
            return config
    return None

def lidar_com_cliente(socket_cliente, particoes):
    try:
        requisicao, addr = socket_cliente.recvfrom(1024)
        requisicao_decodificada = requisicao.decode('utf-8').strip().split(',')

        if len(requisicao_decodificada) != 2:
            resposta = 'Formato de requisição inválido.'
            socket_cliente.sendto(resposta.encode('utf-8'), addr)
            logging.warning('Formato de requisição inválido: %s', requisicao)
            return

        token, nome_dominio = requisicao_decodificada

        if not autenticar(token):
            resposta = 'Autenticação falhou.'
            socket_cliente.sendto(resposta.encode('utf-8'), addr)
            logging.warning('Autenticação falhou para token: %s', token)
            return

        logging.info('Requisição recebida: %s', nome_dominio)

        particao = determinar_particao(nome_dominio, particoes)
        if particao:
            ip_particao = particao['ip']
            porta_particao = particao['porta']

            socket_particao = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            mensagem = f"{nome_dominio},{addr[0]},{addr[1]}"
            socket_particao.sendto(mensagem.encode('utf-8'), (ip_particao, porta_particao))

            logging.info('Requisição encaminhada para %s: %s', nome_dominio, particao)
        else:
            resposta = 'Nenhuma partição disponível para esta requisição.'
            socket_cliente.sendto(resposta.encode('utf-8'), addr)
            logging.warning('Nenhuma partição disponível para %s', nome_dominio)
    except Exception as e:
        logging.error('Erro ao lidar com cliente: %s', e)

def iniciar_roteador(ip_roteador, porta_roteador):
    particoes = carregar_configuracao_particoes()
    servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    servidor.bind((ip_roteador, porta_roteador))
    logging.info(f"Roteador ouvindo em {ip_roteador}:{porta_roteador}")

    while True:
        lidar_com_cliente(servidor, particoes)

# ------------------- Funções do Nodo de Partição -------------------

def lidar_com_requisicao(socket_cliente, dados_dns):
    try:
        requisicao, addr = socket_cliente.recvfrom(1024)
        requisicao_decodificada = requisicao.decode('utf-8').strip().split(',')

        if len(requisicao_decodificada) != 3:
            logging.warning('Formato de requisição inválido: %s', requisicao)
            return

        nome_dominio, ip_cliente, porta_cliente = requisicao_decodificada
        endereco_ip = dados_dns.get(nome_dominio, 'Domínio não encontrado')
        logging.info(f"Partição respondendo: {nome_dominio} -> {endereco_ip}")
        socket_cliente.sendto(endereco_ip.encode('utf-8'), (ip_cliente, int(porta_cliente)))
    except Exception as e:
        logging.error(f"Erro ao lidar com requisição: %s", e)

def iniciar_nodo_particao(letra_particao, ip, porta):
    dados_dns = carregar_dados_dns(letra_particao)
    servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    servidor.bind((ip, porta))
    logging.info(f"Nó de partição {letra_particao} ouvindo em {ip}:{porta}")

    while True:
        lidar_com_requisicao(servidor, dados_dns)

# ------------------- Funções do Cliente -------------------

def enviar_requisicoes(ip_roteador, porta_roteador, requisicoes):
    token = "secreto"
    for requisicao in requisicoes:
        try:
            socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            mensagem = f"{token},{requisicao}"
            print(f"Cliente enviando requisição: {requisicao}")
            socket_cliente.sendto(mensagem.encode('utf-8'), (ip_roteador, porta_roteador))

            resposta, _ = socket_cliente.recvfrom(1024)
            resposta_decodificada = resposta.decode('utf-8')
            print(f"Resposta para {requisicao}: {resposta_decodificada}")

            time.sleep(random.uniform(1, 2))
        except Exception as e:
            logging.error('Erro ao enviar requisição: %s', e)

# ------------------- Execução Principal -------------------

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Uso: python3 dns_particionado.py [roteador|particao|cliente]")
        sys.exit(1)

    modo = sys.argv[1]

    if modo == "roteador":
        ip_roteador = '127.0.0.1'
        porta_roteador = 9000
        iniciar_roteador(ip_roteador, porta_roteador)
    elif modo == "particao":
        if len(sys.argv) < 4:
            print("Uso: python3 dns_particionado.py particao <letra_particao> <porta>")
            sys.exit(1)
        letra_particao = sys.argv[2]
        ip = '127.0.0.1'
        porta = int(sys.argv[3])
        iniciar_nodo_particao(letra_particao, ip, porta)
    elif modo == "cliente":
        configuracao = carregar_configuracao_cliente()
        ip_roteador = configuracao['ip_roteador']
        porta_roteador = configuracao['porta_roteador']
        requisicoes = configuracao['requisicoes']
        enviar_requisicoes(ip_roteador, porta_roteador, requisicoes)
    else:
        print("Modo desconhecido. Use: roteador, particao ou cliente.")
        sys.exit(1)
