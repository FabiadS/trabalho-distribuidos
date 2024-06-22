import tkinter as tk
from tkinter import messagebox
import threading
import time
import random

class Emissor:
    def __init__(self, id, token=False):
        self.id = id
        self.token = token
        self.color = f"#{random.randint(0, 0xFFFFFF):06x}"

class Receptor:
    def __init__(self, id):
        self.id = id
        self.color = "#FFFFFF"

class TokenRing:
    def __init__(self, num_processes):
        self.num_processes = num_processes
        self.emissores = [Emissor(i, token=(i==0)) for i in range(num_processes)]
        self.receptores = [Receptor(i) for i in range(num_processes)]
        self.token_position = 0
        self.stop = False
        self.lock = threading.Lock()
        self.gui = None

    def start_communication(self):
        while not self.stop:
            with self.lock:
                if self.emissores[self.token_position].token:
                    self.send_message(self.token_position)
                    for receptor_id in range(self.num_processes):
                        # Schedule acknowledgment after 1 second
                        self.gui.after(1000, self.send_acknowledgment, receptor_id, self.token_position)
                    self.token_position = (self.token_position + 1) % self.num_processes
                    for emissor in self.emissores:
                        emissor.token = False
                    self.emissores[self.token_position].token = True
            time.sleep(2)

    def send_message(self, emissor_id):
        emissor = self.emissores[emissor_id]
        for receptor_id in range(self.num_processes):
            message_label = f"m{emissor_id}{receptor_id}"
            self.gui.update_receptor_color(receptor_id, emissor.color)
            self.gui.draw_message_line(emissor_id, receptor_id, emissor.color, message_label)
        print(f"Emissor {emissor_id} enviou uma mensagem para todos os receptores")

    def send_acknowledgment(self, receptor_id, emissor_id):
        acknowledgment_label = f"r{receptor_id}{emissor_id}"
        self.gui.draw_response_line(receptor_id, emissor_id, "orange", acknowledgment_label)
        print(f"Receptor {receptor_id} enviou uma confirmação para Emissor {emissor_id}")

    def stop_communication(self):
        self.stop = True

    def set_gui(self, gui):
        self.gui = gui

class GUI(tk.Tk):
    def __init__(self, token_ring):
        super().__init__()
        self.token_ring = token_ring
        self.title("Token Ring Communication")
        self.canvas = tk.Canvas(self, width=600, height=400)
        self.canvas.pack()
        self.draw_emissores()
        self.draw_receptores()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def draw_emissores(self):
        self.emissor_circles = []
        for emissor in self.token_ring.emissores:
            x, y = 100 + emissor.id * 50, 100
            circle = self.canvas.create_oval(x, y, x + 40, y + 40, fill=emissor.color, outline="black")
            self.emissor_circles.append(circle)

    def draw_receptores(self):
        self.receptor_circles = []
        for receptor in self.token_ring.receptores:
            x, y = 100 + receptor.id * 50, 300
            circle = self.canvas.create_oval(x, y, x + 40, y + 40, fill=receptor.color, outline="black")
            self.receptor_circles.append(circle)

    def update_receptor_color(self, receptor_id, color):
        self.canvas.itemconfig(self.receptor_circles[receptor_id], fill=color)

    def draw_message_line(self, emissor_id, receptor_id, color, label):
        emissor_coords = self.canvas.coords(self.emissor_circles[emissor_id])
        receptor_coords = self.canvas.coords(self.receptor_circles[receptor_id])
        emissor_center = (emissor_coords[0] + 20, emissor_coords[1] + 20)
        receptor_center = (receptor_coords[0] + 20, receptor_coords[1] + 20)
        line = self.canvas.create_line(emissor_center, receptor_center, fill=color, width=2)
        text = self.canvas.create_text((emissor_center[0] + receptor_center[0]) / 2,
                                       (emissor_center[1] + receptor_center[1]) / 2, 
                                       text=label, fill=color)
        self.after(1000, lambda: self.canvas.delete(line))  # Remove the line after 1 second
        self.after(1000, lambda: self.canvas.delete(text))  # Remove the text after 1 second

    def draw_response_line(self, receptor_id, emissor_id, color, label):
        receptor_coords = self.canvas.coords(self.receptor_circles[receptor_id])
        emissor_coords = self.canvas.coords(self.emissor_circles[emissor_id])
        receptor_center = (receptor_coords[0] + 20, receptor_coords[1] + 20)
        emissor_center = (emissor_coords[0] + 20, emissor_coords[1] + 20)
        line = self.canvas.create_line(receptor_center, emissor_center, fill=color, dash=(4, 2), width=2)
        text = self.canvas.create_text((receptor_center[0] + emissor_center[0]) / 2,
                                       (receptor_center[1] + emissor_center[1]) / 2, 
                                       text=label, fill=color)
        self.after(1000, lambda: self.canvas.delete(line))  # Remove the line after 1 second
        self.after(1000, lambda: self.canvas.delete(text))  # Remove the text after 1 second

    def on_closing(self):
        self.token_ring.stop_communication()
        self.destroy()

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
