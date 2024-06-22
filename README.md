# Algoritmo de Exclusão Mútua por Token Ring

## Descrição

Este projeto é um simulador do algoritmo de exclusão mútua baseado no token ring, desenvolvido em Python utilizando a biblioteca Tkinter para a interface gráfica. O simulador mostra como os nós em um anel de token podem solicitar acesso a uma região crítica, passar o token entre si e garantir que apenas um nó acesse a região crítica de cada vez.

## Funcionalidades

- Interface gráfica para exibir os nós, o token e a região crítica.
- Inicia a simulação com um número configurável de nós.
- Gerencia a passagem do token entre os nós.
- Simula a entrada e saída de nós na região crítica.

## Requisitos

- Python 3.x
- Biblioteca Tkinter (geralmente incluída na instalação padrão do Python)

## Como Usar

1. Clone este repositório.
2. Execute o script principal `MutualExclusionTokenRing.py`.
3. Insira o número de nós quando solicitado.
4. A simulação iniciará automaticamente, mostrando os nós, o token e a região crítica.

## Funcionamento

1. A simulação começa com um número especificado de nós.
2. Um nó possui o token inicialmente.
3. O nó que possui o token é circulado em vermelho.
4. O nó com o token decide aleatoriamente se deseja entrar na região crítica.
5. Se o nó decidir entrar, ele muda de cor para verde e ocupa a região crítica por um tempo definido.
6. Após sair da região crítica, o token é passado para o próximo nó no anel.
7. O processo se repete até que a simulação seja parada.

### Código para Recepção e Envio de Mensagens, Definição de Números de Processos e Forma de Comunicação

#### Passagem do Token

```python
def pass_token(self):
    while self.running:
        if self.has_token[self.token_node]:
            self.highlight_node(self.token_node)
            wants_to_enter = random.choice([True, False])
            if wants_to_enter:
                self.enter_critical_region(self.token_node)
                time.sleep(1)  # simula o tempo na região crítica
                self.leave_critical_region(self.token_node)
            self.remove_highlight(self.token_node)
            self.has_token[self.token_node] = False
            self.token_node = (self.token_node + 1) % self.num_nodes
            self.has_token[self.token_node] = True
            time.sleep(1)  # simula o tempo de passagem do token
```

#### Comunicação e Região Crítica

```python
def enter_critical_region(self, node_index):
    node, x, y = self.nodes[node_index]
    self.canvas.itemconfig(node, fill='green')
    self.canvas.create_line(x, y, self.center_x, self.center_y, fill='green', width=2, tags='token_line')
    self.canvas.update_idletasks()  # garante que a atualização seja renderizada

def leave_critical_region(self, node_index):
    node, x, y = self.nodes[node_index]
    self.canvas.itemconfig(node, fill='lightblue')
    self.canvas.delete('token_line')
    self.canvas.update_idletasks()  # garante que a atualização seja renderizada
```

## Conclusão

Este simulador de algoritmo de token ring fornece uma representação visual e interativa de como o token pode ser passado entre nós em um anel para garantir a exclusão mútua. Ele permite que os usuários entendam e visualizem como os nós interagem para acessar uma região crítica, utilizando conceitos básicos de algoritmos distribuídos.
