import tkinter as tk
from tkinter import messagebox, ttk
import threading
import time
import random

# Classe Emissor representa cada processo emissor no anel de token
class Emissor:
    def __init__(self, id, token=False):
        self.id = id  # Identificador único do emissor
        self.token = token  # Indica se o emissor possui o token
        self.color = f"#{random.randint(0, 0xFFFFFF):06x}"  # Cor aleatória para o emissor

# Classe Receptor representa cada processo receptor no anel de token
class Receptor:
    def __init__(self, id):
        self.id = id  # Identificador único do receptor
        self.color = "#FFFFFF"  # Cor inicial do receptor (branca)

# Classe TokenRing gerencia a lógica de comunicação entre emissores e receptores
class TokenRing:
    def __init__(self, num_processes):
        self.num_processes = num_processes  # Número de processos no anel
        self.emissores = [Emissor(i, token=(i==0)) for i in range(num_processes)]  # Lista de emissores
        self.receptores = [Receptor(i) for i in range(num_processes)]  # Lista de receptores
        self.token_position = 0  # Posição inicial do token
        self.stop = False  # Indicador para parar a comunicação
        self.lock = threading.Lock()  # Lock para controlar acesso à comunicação
        self.gui = None  # Referência à interface gráfica

    # Função que inicia a comunicação no anel
    def start_communication(self):
        while not self.stop:
            with self.lock:
                if self.emissores[self.token_position].token:
                    self.gui.update_table_sender(self.token_position)  # Atualiza a tabela com o emissor atual
                    self.send_message(self.token_position)  # Envia mensagem do emissor atual
                    for receptor_id in range(self.num_processes):
                        # Agendar confirmação após 2 segundos
                        self.gui.after(2000, self.send_acknowledgment, receptor_id, self.token_position)
                    self.token_position = (self.token_position + 1) % self.num_processes  # Muda para o próximo emissor
                    for emissor in self.emissores:
                        emissor.token = False  # Remove o token de todos os emissores
                    self.emissores[self.token_position].token = True  # Concede o token ao próximo emissor
            time.sleep(4)  # Espera 4 segundos antes da próxima iteração

    # Função que envia mensagem do emissor para todos os receptores
    def send_message(self, emissor_id):
        emissor = self.emissores[emissor_id]
        messages = []
        for receptor_id in range(self.num_processes):
            message_label = f"m{emissor_id}{receptor_id}"  # Formata a mensagem
            messages.append(message_label)
            self.gui.update_receptor_color(receptor_id, emissor.color)  # Atualiza a cor do receptor
            self.gui.draw_message_line(emissor_id, receptor_id, emissor.color, message_label)  # Desenha a linha de mensagem
        self.gui.update_table_message(messages)  # Atualiza a tabela com as mensagens enviadas
        print(f"Emissor {emissor_id} enviou uma mensagem para todos os receptores")

    # Função que envia confirmação do receptor para o emissor
    def send_acknowledgment(self, receptor_id, emissor_id):
        acknowledgment_label = f"r{receptor_id}{emissor_id}"  # Formata a mensagem de confirmação
        self.gui.draw_response_line(receptor_id, emissor_id, "orange", acknowledgment_label)  # Desenha a linha de confirmação
        self.gui.update_table_acknowledgment(acknowledgment_label)  # Atualiza a tabela com a confirmação
        print(f"Receptor {receptor_id} enviou uma confirmação para Emissor {emissor_id}")

    # Função para parar a comunicação
    def stop_communication(self):
        self.stop = True

    # Função para definir a interface gráfica
    def set_gui(self, gui):
        self.gui = gui

# Classe GUI gerencia a interface gráfica da aplicação
class GUI(tk.Tk):
    def __init__(self, token_ring):
        super().__init__()
        self.token_ring = token_ring
        self.title("Privilege Based Communication")
        self.geometry("800x500")

        # Canvas para desenhar os emissores e receptores
        self.canvas = tk.Canvas(self, width=600, height=400)
        self.canvas.pack(side=tk.LEFT)
        
        # Frame para a tabela
        self.table_frame = tk.Frame(self, width=200)
        self.table_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)

        # Tabela para mostrar o emissor atual, mensagens e confirmações
        self.tree = ttk.Treeview(self.table_frame, columns=("emissor", "mensagem", "confirmacao"), show='headings', height=3)
        self.tree.heading("emissor", text="Emissor")
        self.tree.heading("mensagem", text="Mensagem")
        self.tree.heading("confirmacao", text="Confirmação")
        self.tree.column("emissor", width=50)
        self.tree.column("mensagem", width=300)
        self.tree.column("confirmacao", width=300)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.draw_emissores()  # Desenha os emissores no canvas
        self.draw_receptores()  # Desenha os receptores no canvas
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # Define a ação ao fechar a janela

    # Função para desenhar os emissores
    def draw_emissores(self):
        self.emissor_circles = []
        for emissor in self.token_ring.emissores:
            x, y = 100 + emissor.id * 50, 100
            circle = self.canvas.create_oval(x, y, x + 40, y + 40, fill=emissor.color, outline="black")
            self.emissor_circles.append(circle)

    # Função para desenhar os receptores
    def draw_receptores(self):
        self.receptor_circles = []
        for receptor in self.token_ring.receptores:
            x, y = 100 + receptor.id * 50, 300
            circle = self.canvas.create_oval(x, y, x + 40, y + 40, fill=receptor.color, outline="black")
            self.receptor_circles.append(circle)

    # Função para atualizar a cor do receptor
    def update_receptor_color(self, receptor_id, color):
        self.canvas.itemconfig(self.receptor_circles[receptor_id], fill=color)

    # Função para desenhar a linha de mensagem do emissor para o receptor
    def draw_message_line(self, emissor_id, receptor_id, color, label):
        emissor_coords = self.canvas.coords(self.emissor_circles[emissor_id])
        receptor_coords = self.canvas.coords(self.receptor_circles[receptor_id])
        emissor_center = (emissor_coords[0] + 20, emissor_coords[1] + 20)
        receptor_center = (receptor_coords[0] + 20, receptor_coords[1] + 20)
        line = self.canvas.create_line(emissor_center, receptor_center, fill=color, width=2)
        text = self.canvas.create_text((emissor_center[0] + receptor_center[0]) / 2,
                                       (emissor_center[1] + receptor_center[1]) / 2, 
                                       text=label, fill=color)
        self.after(1000, lambda: self.canvas.delete(line))  # Remove a linha após 1 segundo
        self.after(1000, lambda: self.canvas.delete(text))  # Remove o texto após 1 segundo

    # Função para desenhar a linha de confirmação do receptor para o emissor
    def draw_response_line(self, receptor_id, emissor_id, color, label):
        receptor_coords = self.canvas.coords(self.receptor_circles[receptor_id])
        emissor_coords = self.canvas.coords(self.emissor_circles[emissor_id])
        receptor_center = (receptor_coords[0] + 20, receptor_coords[1] + 20)
        emissor_center = (emissor_coords[0] + 20, emissor_coords[1] + 20)
        line = self.canvas.create_line(receptor_center, emissor_center, fill=color, dash=(4, 2), width=2)
        text = self.canvas.create_text((receptor_center[0] + emissor_center[0]) / 2,
                                       (receptor_center[1] + emissor_center[1]) / 2, 
                                       text=label, fill=color)
        self.after(1000, lambda: self.canvas.delete(line))  # Remove a linha após 1 segundo
        self.after(1000, lambda: self.canvas.delete(text))  # Remove o texto após 1 segundo

    # Função para atualizar a tabela com o emissor atual
    def update_table_sender(self, emissor_id):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.tree.insert("", "end", values=(f"{emissor_id}", "", ""))

    # Função para atualizar a tabela com as mensagens enviadas
    def update_table_message(self, messages):
        for item in self.tree.get_children():
            current_values = self.tree.item(item, "values")
            self.tree.item(item, values=(current_values[0], ", ".join(messages), ""))

    # Função para atualizar a tabela com as confirmações recebidas
    def update_table_acknowledgment(self, acknowledgment_label):
        for item in self.tree.get_children():
            current_values = self.tree.item(item, "values")
            current_acknowledgments = current_values[2].split(", ") if current_values[2] else []
            current_acknowledgments.append(acknowledgment_label)
            self.tree.item(item, values=(current_values[0], current_values[1], ", ".join(current_acknowledgments)))

    # Função para fechar a janela e parar a comunicação
    def on_closing(self):
        self.token_ring.stop_communication()
        self.destroy()

# Função principal que inicia a aplicação
def main():
    num_processes = int(input("Digite o número de processos (1-10): "))
    if num_processes < 1 or num_processes > 10:
        messagebox.showerror("Erro", "O número de processos deve estar entre 1 e 10")
        return

    token_ring = TokenRing(num_processes)
    gui = GUI(token_ring)
    token_ring.set_gui(gui)
    
    threading.Thread(target=token_ring.start_communication, daemon=True).start()
    gui.mainloop()

if __name__ == "__main__":
    main()
