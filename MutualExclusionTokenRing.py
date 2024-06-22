import tkinter as tk
import time
import threading
import math
import random

class TokenRingSimulator:
    def __init__(self, root, num_nodes):
        self.root = root
        self.num_nodes = num_nodes
        self.canvas = tk.Canvas(root, width=800, height=600, bg='white')
        self.canvas.pack()
        self.node_radius = 20
        self.token_radius = 10
        self.center_x = 400
        self.center_y = 300
        self.radius = 200
        self.angle_step = 360 / self.num_nodes
        self.nodes = []
        self.token_node = 0
        self.create_nodes()
        self.create_critical_region()
        self.has_token = [False] * self.num_nodes
        self.has_token[0] = True
        self.running = True
        self.start_token_passing()

    def create_nodes(self):
        for i in range(self.num_nodes):
            angle = math.radians(i * self.angle_step)
            x = self.center_x + self.radius * math.cos(angle)
            y = self.center_y + self.radius * math.sin(angle)
            node = self.canvas.create_oval(x - self.node_radius, y - self.node_radius, x + self.node_radius, y + self.node_radius, fill='lightblue', outline='black', width=2)
            self.nodes.append((node, x, y))
            self.canvas.create_text(x, y, text=str(i + 1))

    def create_critical_region(self):
        self.critical_region = self.canvas.create_rectangle(self.center_x - 50, self.center_y - 50, self.center_x + 50, self.center_y + 50, outline='black', width=2)
        self.critical_region_text = self.canvas.create_text(self.center_x, self.center_y, text="Critical Region", font=('Arial', 12))

    def pass_token(self):
        while self.running:
            if self.has_token[self.token_node]:
                self.highlight_node(self.token_node)
                wants_to_enter = random.choice([True, False])
                if wants_to_enter:
                    self.enter_critical_region(self.token_node)
                    time.sleep(1)  # simulate the time in critical region
                    self.leave_critical_region(self.token_node)
                self.remove_highlight(self.token_node)
                self.has_token[self.token_node] = False
                self.token_node = (self.token_node + 1) % self.num_nodes
                self.has_token[self.token_node] = True
                time.sleep(1)  # simulate the token passing time

    def highlight_node(self, node_index):
        node, x, y = self.nodes[node_index]
        self.canvas.itemconfig(node, outline='red', width=4)
        time.sleep(1)
        self.canvas.update_idletasks()  # ensure the update is rendered

    def remove_highlight(self, node_index):
        node, x, y = self.nodes[node_index]
        self.canvas.itemconfig(node, outline='black', width=2)
        self.canvas.update_idletasks()  # ensure the update is rendered

    def enter_critical_region(self, node_index):
        node, x, y = self.nodes[node_index]
        self.canvas.itemconfig(node, fill='green')
        self.canvas.create_line(x, y, self.center_x, self.center_y, fill='green', width=2, tags='token_line')
        self.canvas.update_idletasks()  # ensure the update is rendered

    def leave_critical_region(self, node_index):
        node, x, y = self.nodes[node_index]
        self.canvas.itemconfig(node, fill='lightblue')
        self.canvas.delete('token_line')
        self.canvas.update_idletasks()  # ensure the update is rendered

    def start_token_passing(self):
        threading.Thread(target=self.pass_token, daemon=True).start()

    def stop(self):
        self.running = False

def main():
    root = tk.Tk()
    root.title("Token Ring Algorithm Simulator")
    num_nodes = int(input("Enter the number of nodes: "))
    simulator = TokenRingSimulator(root, num_nodes)
    root.protocol("WM_DELETE_WINDOW", simulator.stop)
    root.mainloop()

if __name__ == "__main__":
    main()
