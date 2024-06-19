import threading
import time
import random
import socket
import json
import sys

class TesteDNSParticionado:
    def __init__(self, config_cliente, num_clientes):
        self.config_cliente = config_cliente
        self.num_clientes = num_clientes

    def enviar_requisicao(self, cliente_id):
        token = "secreto"
        ip_roteador = self.config_cliente['ip_roteador']
        porta_roteador = self.config_cliente['porta_roteador']
        requisicoes = self.config_cliente['requisicoes']

        for requisicao in requisicoes:
            try:
                socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                mensagem = f"{token},{requisicao}"
                print(f"Cliente {cliente_id} enviando requisição: {requisicao}")
                socket_cliente.sendto(mensagem.encode('utf-8'), (ip_roteador, porta_roteador))

                resposta, _ = socket_cliente.recvfrom(1024)
                resposta_decodificada = resposta.decode('utf-8')
                print(f"Cliente {cliente_id} recebeu resposta para {requisicao}: {resposta_decodificada}")

                time.sleep(random.uniform(1, 2))
            except Exception as e:
                print(f"Erro ao enviar requisição pelo cliente {cliente_id}: {e}")

    def iniciar_testes(self):
        threads = []
        for i in range(self.num_clientes):
            t = threading.Thread(target=self.enviar_requisicao, args=(i,))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

if __name__ == "__main__":
    with open('configuracoes/configuracao_cliente.json', 'r') as f:
        config_cliente = json.load(f)

    if len(sys.argv) != 2:
        print("Uso: python3 teste_dns_particionado.py <num_clientes>")
        sys.exit(1)

    num_clientes = int(sys.argv[1])  # Recebe o número de clientes via linha de comando

    teste_dns = TesteDNSParticionado(config_cliente, num_clientes)
    teste_dns.iniciar_testes()
