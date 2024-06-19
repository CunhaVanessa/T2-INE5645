# T2-INE5645

Este projeto implementa o trabalho T2 da disciplina INE5645 - Programação Paralela e Distribuída da UFSC, onde trabalhamos um serviço de DNS particionado usando Python com a biblioteca Sockets. Nos baseamos principalmente no padrão de projeto Sharding, exposto em sala de aula para seguir com o desenvolvimento do mesmo para atender os seguintes requisitos:

Um Domain Name System (DNS) faz associação entre nomes de domínios e entidades participantes. A sua utilização mais convencional associa nomes de domínios mais facilmente memorizáveis a endereços IP, necessários à localização e identificação de serviços e dispositivos, processo esse denominado resolução de nomes. Um sistema como esse pode receber uma grande quantidade de requisições de resolução, e isso pode
fazer com que seja muito caro encarregar um único servidor de armazenar todos os dados. Em vista disso, podemos particionar o serviço, adicionando mais servidores e distribuindo uma porção dos dados para cada um.

Para o trabalho você deve implementar um serviço de DNS particionado, composto por um nó roteador, e nós de partição. Cada cliente envia requisições ao nó roteador, que redireciona a um dos nós de partição, que por sua vez responde o cliente. O número de partições é fixo, sendo 26 partições, uma para cada letra do alfabeto. A primeira partição armazena os nomes iniciados por “A”, a segunda partição os nomes iniciados por “B”, e assim sucessivamente. A relação de nomes e endereços IP deve ser armazenada em arquivo.

Outros requisitos:
- A comunicação deve ser implementada utilizando sockets ou MPI. Se optar por usar
MPI, não poderá ser utilizado recursos de comunicação coletiva ou implementações
do MPI de padrões como scatter/gather e map/reduce;
- Cada comunicação realizada deve ser exibida na tela (print);
- Para testes e simulação, devem ser criados arquivos de configuração:
    - Para cada partição, o arquivo de configuração tem seu endereço e uma relação de nomes para endereços IP;
    - O roteador tem o próprio endereço e os endereços das partições;  
    - Os clientes precisam do endereço do roteador e uma lista de requisições que serão feitas durante a simulação. Requisições com nomes existentes e inexistentes.
    - Requisições devem ser feitas em intervalos aleatórios de 1 a 2 segundos.

## Dependências

- Python 3.x

## Como Executar

### Passo 0: Gerar partições

Antes de mais nada é preciso gerar as partições onde estarão mapeadas de A-Z os sites e seus respectivos IPs fictícios:

`python3 gerar_particoes.py`

### Passo 1: Iniciar os Nós de Partição

Para conectar os nós as respectivas partições utilize o comando:

`python3 iniciar_particoes.py`

### Passo 2: Iniciar o Roteador

Em um novo terminal, execute:

`python3 dns_particionado.py roteador`

### Passo 3: Enviar Requisições do Cliente

Em um novo terminal, execute:

`python3 dns_particionado.py cliente`

### Passo 4: Realizar testes

`python3 teste_dns_particionado.py <num_clientes>`

### Configurações

- configuracao_particoes.json: Configurações dos nós de partição.
- particao_<LETRA>.json: Dados de DNS para cada partição.
- configuracao_cliente.json: Configuração do cliente, incluindo o IP do roteador, porta e lista de requisições.

Certifique-se de que todos os arquivos de configuração estejam devidamente configurados antes de executar os scripts.

## Decisões de Padrão de Projeto

1. Uso de Sockets: Optamos por utilizar sockets para comunicação entre clientes, roteadores e nós de partição devido à sua simplicidade e eficiência em implementar comunicações de rede em Python.

2. Multithreading: O uso de threads permite que o servidor (roteador e nós de partição) lide com múltiplas conexões simultaneamente, melhorando a capacidade de resposta e escalabilidade do sistema.

3. Configuração Baseada em Arquivos JSON: Arquivos JSON são utilizados para armazenar a configuração dos nós de partição, clientes e dados de DNS. Isso facilita a manutenção e alteração das configurações sem a necessidade de modificar o código.

4. Particionamento por Letra Inicial: A escolha de particionar os dados de DNS com base na letra inicial do nome de domínio simplifica a lógica de roteamento e armazenamento, distribuindo de forma relativamente uniforme as requisições entre os nós de partição.