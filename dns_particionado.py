import socket
import threading
import json
import time
import random

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

# ------------------- Funções do Roteador -------------------

def lidar_com_cliente(socket_cliente, particoes):
    try:
        requisicao = socket_cliente.recv(1024).decode('utf-8')
        nome_dominio = requisicao.strip()
        primeira_letra = nome_dominio[0].upper()

        if primeira_letra in particoes:
            endereco_particao = particoes[primeira_letra]
            socket_particao = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_particao.connect((endereco_particao['ip'], endereco_particao['porta']))
            print(f"Roteador redirecionando {nome_dominio} para partição {primeira_letra}")
            socket_particao.sendall(nome_dominio.encode('utf-8'))

            resposta = socket_particao.recv(1024)
            socket_cliente.sendall(resposta)

            socket_particao.close()
        else:
            socket_cliente.sendall('Nenhuma partição disponível para esta requisição.'.encode('utf-8'))
    except Exception as e:
        print(f"Erro ao lidar com cliente: {e}")
    finally:
        socket_cliente.close()

def iniciar_roteador(ip_roteador, porta_roteador):
    particoes = carregar_configuracao_particoes()
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((ip_roteador, porta_roteador))
    servidor.listen(5)
    print(f"Roteador ouvindo em {ip_roteador}:{porta_roteador}")

    while True:
        socket_cliente, addr = servidor.accept()
        print(f"Conexão aceita de {addr}")
        manipulador_cliente = threading.Thread(target=lidar_com_cliente, args=(socket_cliente, particoes))
        manipulador_cliente.start()

# ------------------- Funções do Nodo de Partição -------------------

def lidar_com_requisicao(socket_cliente, dados_dns):
    try:
        nome_dominio = socket_cliente.recv(1024).decode('utf-8').strip()
        endereco_ip = dados_dns.get(nome_dominio, 'Domínio não encontrado')
        print(f"Partição respondendo: {nome_dominio} -> {endereco_ip}")
        socket_cliente.sendall(endereco_ip.encode('utf-8'))
    except Exception as e:
        print(f"Erro ao lidar com requisição: {e}")
    finally:
        socket_cliente.close()

def iniciar_nodo_particao(letra_particao, ip, porta):
    dados_dns = carregar_dados_dns(letra_particao)
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((ip, porta))
    servidor.listen(5)
    print(f"Nó de partição {letra_particao} ouvindo em {ip}:{porta}")

    while True:
        socket_cliente, addr = servidor.accept()
        print(f"Conexão aceita de {addr}")
        manipulador_cliente = threading.Thread(target=lidar_com_requisicao, args=(socket_cliente, dados_dns))
        manipulador_cliente.start()

# ------------------- Funções do Cliente -------------------

def enviar_requisicoes(ip_roteador, porta_roteador, requisicoes):
    for requisicao in requisicoes:
        try:
            socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_cliente.connect((ip_roteador, porta_roteador))
            print(f"Cliente enviando requisição: {requisicao}")
            socket_cliente.sendall(requisicao.encode('utf-8'))

            resposta = socket_cliente.recv(1024).decode('utf-8')
            print(f"Resposta para {requisicao}: {resposta}")

            socket_cliente.close()
            time.sleep(random.uniform(1, 2))
        except Exception as e:
            print(f"Erro ao enviar requisição: {e}")

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
