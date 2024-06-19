import subprocess
import json

# Função para carregar a configuração das partições a partir de um arquivo JSON
def carregar_configuracao_particoes():
    # Abre o arquivo 'configuracoes/configuracao_particoes.json' no modo de leitura
    with open('configuracoes/configuracao_particoes.json', 'r') as f:
        # Lê o arquivo JSON e o converte em um dicionário Python
        return json.load(f)

# Função para iniciar todos os nós de partição
def iniciar_nodos_particoes():
    # Carrega a configuração das partições usando a função definida acima
    particoes = carregar_configuracao_particoes()
    # Lista para manter a referência dos processos iniciados
    processos = []

    # Itera sobre cada entrada na configuração das partições
    for nodo_id, config in particoes.items():
        intervalo = config['intervalo']  # Obtém o intervalo de letras da partição
        ip = config['ip']  # Obtém o IP da partição
        porta = config['porta']  # Define a porta inicial para o intervalo

        # Itera sobre o intervalo de letras da partição
        for letra in range(ord(intervalo[0]), ord(intervalo[1]) + 1):
            letra_particao = chr(letra)  # Converte o código ASCII de volta para a letra
            # Cria o comando para iniciar o nó de partição
            comando = f"python3 dns_particionado.py particao {letra_particao} {porta}"
            # Imprime uma mensagem indicando qual partição está sendo iniciada
            print(f"Iniciando nodo de partição para {letra_particao} no IP {ip} e porta {porta}")
            # Inicia o processo usando subprocess.Popen e armazena a referência na lista processos
            processo = subprocess.Popen(comando, shell=True)
            processos.append(processo)  # Adiciona o processo à lista
            
            porta += 1  # Incrementa a porta para o próximo nodo

    # Retorna a lista de processos iniciados
    return processos

# Ponto de entrada do script
if __name__ == "__main__":
    # Inicia todos os nós de partição e armazena os processos iniciados
    processos = iniciar_nodos_particoes()
    print("Todos os nós de partição foram iniciados.")
    
    try:
        # Aguarda que todos os processos terminem
        for processo in processos:
            processo.wait()
    except KeyboardInterrupt:
        # Trata a interrupção do teclado (Ctrl+C) para encerrar os processos de forma limpa
        print("Encerrando todos os processos de nós de partição...")
        for processo in processos:
            processo.terminate()
