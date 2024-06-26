# Algoritmo de Comunicação em Grupo Baseado em Privilégio

Este código implementa um sistema de comunicação em grupo baseado em privilégio. Tem como objetivo simular a comunicação entre processos emissores e receptores, utilizando a linguagem Python com a biblioteca Tkinter para a interface gráfica. O sistema permite que múltiplos processos enviem e recebam mensagens, sendo que apenas o processo emissor de posse do token pode realizar o envio de mensagens ao grupo.

### Requisitos Funcionais

- Interface gráfica para visualizar emissores e receptores.
- Emissor com o token envia mensagens para todos os receptores.
- Receptores enviam confirmações de recebimento de mensagens.
- Gerenciamento de token para controlar qual emissor pode enviar mensagens.
- Tabela de manutenção do estado do sistema (quem tem o token, mensagens enviadas e recebidas).

### Identificação dos Processos
- Cada emissor e receptor possui um ID único.
- O processo atual com o token é identificado e permite o envio de mensagens.

### Comunicação entre Receptor e Emissor

#### Descrição da Comunicação
A comunicação segue o padrão de privilégio:
1. O emissor com o token envia mensagens para todos os receptores.
2. Cada receptor envia uma confirmação de recebimento ao emissor.
3. O token é passado para o próximo emissor na sequência.

### Código de Demonstração

#### Envio de Mensagem

```python
def send_message(self, emissor_id):
    emissor = self.emissores[emissor_id]
    for receptor_id in range(self.num_processes):
        message_label = f"m{emissor_id}{receptor_id}"
        self.gui.update_receptor_color(receptor_id, emissor.color)
        self.gui.draw_message_line(emissor_id, receptor_id, emissor.color, message_label)
    print(f"Emissor {emissor_id} enviou uma mensagem para todos os receptores")
```

#### Confirmação de Recebimento

```python
def send_acknowledgment(self, receptor_id, emissor_id):
    acknowledgment_label = f"r{receptor_id}{emissor_id}"
    self.gui.draw_response_line(receptor_id, emissor_id, "orange", acknowledgment_label)
    print(f"Receptor {receptor_id} enviou uma confirmação para Emissor {emissor_id}")
```

### Conclusão

A implementação do sistema de comunicação baseado em privilégio demonstrou com sucesso o envio e recebimento eficiente e sincronizado de mensagens entre processos emissores e receptores. Utilizando a linguagem Python e a biblioteca Tkinter, foi possível criar uma interface gráfica intuitiva que facilita a visualização e o entendimento do fluxo de comunicação. 

# Algoritmo de Exclusão Mútua por Token Ring

## Descrição Geral

Este projeto é um simulador de algoritmo de exclusão mútua baseado no token ring, desenvolvido em Python utilizando a biblioteca Tkinter para a interface gráfica. O simulador ilustra como os nós em um anel de token podem solicitar acesso a uma região crítica, passar o token entre si e garantir que apenas um nó acesse a região crítica de cada vez.

### Funcionalidades

- Interface gráfica para exibir os nós, o token e a região crítica.
- Inicia a simulação com um número configurável de nós.
- Gerencia a passagem do token entre os nós.
- Simula a entrada e saída de nós na região crítica.

### Requisitos

- Python 3.x
- Biblioteca Tkinter (geralmente incluída na instalação padrão do Python)

### Como Usar

1. Clone este repositório.
2. Execute o script principal `MutualExclusionTokenRing.py`.
3. Insira o número de nós quando solicitado.
4. A simulação iniciará automaticamente, mostrando os nós, o token e a região crítica.

### Funcionamento

1. A simulação começa com um número especificado de nós.
2. Um nó possui o token inicialmente.
3. O nó que possui o token é circulado em vermelho.
4. O nó com o token decide aleatoriamente se deseja entrar na região crítica.
5. Se o nó decidir entrar, ele muda de cor para verde e ocupa a região crítica por um tempo definido.
6. Após sair da região crítica, o token é passado para o próximo nó no anel.
7. O processo se repete até que a simulação seja parada.

## Identificação dos Processos

- Região Crítica: Representada por um retângulo no canvas, indicando qual nó está atualmente na região crítica.
- Nós: Cada nó é representado por um círculo e possui um ID único. Os nós decidem aleatoriamente se entrarão ou não na região crítica ao receber o token.
- Token: O token é passado de nó para nó, permitindo que o nó que o possui tome decisões sobre acessar a região crítica.
Caixa de Informações: Exibe informações sobre o nó atual com o token, sua decisão e o estado da região crítica.

### Classes e Funções princiáis
**1. CriticalRegion:** Representa a região crítica no canvas. Possui métodos para atualizar e limpar a região crítica com base no nó que a está utilizando.

**2. Node:** Representa um nó no canvas. Possui métodos para destacar, entrar e sair da região crítica, passar e receber o token, e tomar decisões aleatórias.

**3. InfoBox:** Exibe informações sobre o estado atual do nó com o token, incluindo a decisão tomada e o valor atual da região crítica.

**4. simulate_token_passing:** Função que simula a passagem do token entre os nós e o acesso à região crítica.

**5. create_nodes:** Função que cria os nós no canvas em posições calculadas ao redor de um círculo.

**6. main:** Função principal que inicializa a interface gráfica e inicia a simulação.

## Conclusão

Este simulador de algoritmo de token ring fornece uma representação visual e interativa de como o token pode ser passado entre nós em um anel para garantir a exclusão mútua. Ele permite que os usuários entendam e visualizem como os nós interagem para acessar uma região crítica, utilizando conceitos básicos de algoritmos distribuídos.
