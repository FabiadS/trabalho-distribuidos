import tkinter as tk
import time
import threading
import random
from math import cos, sin, pi

# Classe que representa a região crítica no canvas. Cria um retângulo e um texto para indicar a região crítica.
class CriticalRegion:
    def __init__(self, canvas, x, y, size):
        self.canvas = canvas
        self.rect = canvas.create_rectangle(x, y, x + size, y + size, outline='black', fill='white')
        self.text = canvas.create_text(x + size // 2, y + size // 2, text='Critical \n Region', font=('Arial', 12))
        self.value = None

    # Atualiza a região crítica com o ID do nó que a está utilizando.
    def update(self, node_id):
        self.value = node_id
        self.canvas.itemconfig(self.rect, fill='yellow')
        self.canvas.itemconfig(self.text, text=f'Node {node_id}')
        self.canvas.update()

    # Limpa a região crítica, removendo o ID do nó.
    def clear(self):
        self.value = None
        self.canvas.itemconfig(self.rect, fill='white')
        self.canvas.itemconfig(self.text, text='CR')
        self.canvas.update()

# Classe que representa um nó no canvas. Inicializa o nó com suas propriedades e desenha um círculo com um texto no canvas.
class Node:
    def __init__(self, canvas, x, y, size, node_id):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.size = size
        self.node_id = node_id
        self.has_token = False
        self.decision = None
        self.rect = canvas.create_oval(x, y, x + size, y + size, outline='black', fill='white')
        self.text = canvas.create_text(x + size // 2, y + size // 2, text=f'{node_id}', font=('Arial', 12))

    # Destaca o nó, alterando a cor de contorno.
    def highlight(self):
        self.canvas.itemconfig(self.rect, outline='red', width=3)
        self.canvas.update()
        time.sleep(1)

    # Remove o destaque do nó, revertendo a cor de contorno.
    def unhighlight(self):
        self.canvas.itemconfig(self.rect, outline='black', width=1)
        self.canvas.update()

    # Indica que o nó entrou na região crítica, alterando a cor de preenchimento.
    def enter_CR(self):
        self.canvas.itemconfig(self.rect, fill='yellow')

    # Indica que o nó saiu da região crítica, revertendo a cor de preenchimento.
    def leave_CR(self):
        self.canvas.itemconfig(self.rect, fill='white')

    # Passa o token para o próximo nó.
    def pass_token(self, next_node):
        self.unhighlight()
        next_node.receive_token()
        self.has_token = False

    # Recebe o token, marcando o nó como possuidor do token.
    def receive_token(self):
        self.has_token = True

    # Faz uma decisão aleatória (True ou False) sobre entrar na região crítica.
    def make_decision(self):
        self.decision = random.choice([True, False])
        return self.decision

# Função que simula a passagem do token entre os nós e o acesso à região crítica.
def simulate_token_passing(nodes, critical_region, info_box):
    while True:
        for node in nodes:
            if node.has_token:
                node.make_decision()
                info_box.update_info(node.node_id, node.decision, critical_region.value)
                node.highlight()
                if node.decision:
                    critical_region.update(node.node_id)
                    node.enter_CR()
                    info_box.update_info(node.node_id, node.decision, critical_region.value)
                    time.sleep(1)
                    critical_region.clear()
                else:
                    time.sleep(1)
                next_node = nodes[(node.node_id + 1) % len(nodes)]
                node.pass_token(next_node)
                node.leave_CR()
                break

# Classe que representa uma caixa de informações no canvas. Exibe informações sobre o estado atual do nó com o token.
class InfoBox:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.box = canvas.create_rectangle(x, y, x + 150, y + 100, outline='black', fill='white')
        self.node_text = canvas.create_text(x + 75, y + 20, text='Node with Token: ', font=('Arial', 12))
        self.choice_text = canvas.create_text(x + 75, y + 50, text='Choice: ', font=('Arial', 12))
        self.cr_value_text = canvas.create_text(x + 75, y + 80, text='Is in CR: ', font=('Arial', 12))

    # Atualiza a caixa de informações com o ID do nó, a decisão tomada e o valor atual da região crítica.
    def update_info(self, node_id, choice, cr_value):
        self.canvas.itemconfig(self.node_text, text=f'Node with Token: {node_id}')
        choice_str = choice if choice is not None else ' '
        self.canvas.itemconfig(self.choice_text, text=f'Choice: {choice_str}')
        node_str = 'node ' + str(cr_value) if cr_value is not None else ' '
        self.canvas.itemconfig(self.cr_value_text, text=f'Is in CR: {node_str}')
        self.canvas.update()

# Função que cria os nós no canvas em posições calculadas ao redor de um círculo.
def create_nodes(canvas, num_nodes):
    nodes = []
    angle_step = 2 * pi / num_nodes
    radius = 200
    center_x, center_y = 300, 300
    size = 40

    for i in range(num_nodes):
        angle = i * angle_step
        x = center_x + radius * cos(angle) - size // 2
        y = center_y + radius * sin(angle) - size // 2
        node = Node(canvas, x, y, size, i)
        nodes.append(node)

    nodes[0].receive_token()   # O primeiro nó inicia com o token
    return nodes

# Função principal que inicializa a interface gráfica e inicia a simulação.
def main():
    num_nodes = int(input("Enter the number of nodes: "))

    root = tk.Tk()
    root.title("Token Ring Mutual Exclusion Simulation")
    canvas = tk.Canvas(root, width=600, height=600)
    canvas.pack()

    critical_region = CriticalRegion(canvas, 250, 250, 100)
    nodes = create_nodes(canvas, num_nodes)
    info_box = InfoBox(canvas, 450, 20)

    simulation_thread = threading.Thread(target=simulate_token_passing, args=(nodes, critical_region, info_box))
    simulation_thread.daemon = True
    simulation_thread.start()

    root.mainloop()

if __name__ == "__main__":
    main()
