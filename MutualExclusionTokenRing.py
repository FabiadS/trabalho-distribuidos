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
        self.canvas.pack(padx=20, pady=20)
        self.node_radius = 20
        self.token_radius = 10
        self.center_x = 400
        self.center_y = 300
        self.radius = 200
        self.angle_step = 360 / self.num_nodes
        self.nodes = []
        self.token_node = 0
        self.critical_region_value = None
        self.create_nodes()
        self.create_critical_region()
        self.create_info_box()
        self.has_token = [False] * self.num_nodes
        self.has_token[0] = True
        self.running = True
        self.start_token_passing()

    def create_nodes(self):
        for i in range(self.num_nodes):
            angle = math.radians(i * self.angle_step)
            x = self.center_x + self.radius * math.cos(angle)
            y = self.center_y + self.radius * math.sin(angle)
            node = self.canvas.create_oval(x - self.node_radius, y - self.node_radius, x + self.node_radius, y + self.node_radius, fill='#87CEEB', outline='#4682B4', width=3)
            self.nodes.append((node, x, y))
            self.canvas.create_text(x, y, text=str(i + 1), font=('Arial', 10, 'bold'))

    def create_critical_region(self):
        self.critical_region = self.canvas.create_rectangle(self.center_x - 50, self.center_y - 50, self.center_x + 50, self.center_y + 50, outline='#4682B4', width=3)
        self.critical_region_text = self.canvas.create_text(self.center_x, self.center_y - 10, text="Critical \n Region", font=('Arial', 12, 'bold'))
        self.critical_region_value_text = self.canvas.create_text(self.center_x, self.center_y + 20, text="", font=('Arial', 12, 'bold'))

    def create_info_box(self):
        self.info_box = self.canvas.create_rectangle(600, 40, 770, 140, outline='#4682B4', width=3)
        self.info_box_title = self.canvas.create_text(690, 55, text="Node turn Info", font=('Arial', 12, 'bold', 'underline'))
        self.info_texts = {
            'token_node': self.canvas.create_text(610, 80, text="Node with token: ", font=('Arial', 10, 'bold'), anchor='w'),
            'wants_to_enter': self.canvas.create_text(610, 100, text="Wants to enter: ", font=('Arial', 10, 'bold'), anchor='w'),
            'critical_value': self.canvas.create_text(610, 120, text="Critical region value: ", font=('Arial', 10, 'bold'), anchor='w')
        }

    def update_info_box(self, token_node, wants_to_enter):
        self.canvas.itemconfig(self.info_texts['token_node'], text=f"Node with token: {token_node + 1}")
        self.canvas.itemconfig(self.info_texts['wants_to_enter'], text=f"Wants to enter: {wants_to_enter}")
        critical_value_text = str(self.critical_region_value) if self.critical_region_value is not None else " "
        self.canvas.itemconfig(self.info_texts['critical_value'], text=f"Critical region value: {critical_value_text}")

    def pass_token(self):
        while self.running:
            if self.has_token[self.token_node]:
                self.update_info_box(self.token_node, ' ')
                self.highlight_node(self.token_node)
                wants_to_enter = random.choice([True, False])
                self.update_info_box(self.token_node, wants_to_enter)
                if wants_to_enter:
                    self.enter_critical_region(self.token_node)
                    self.update_info_box(self.token_node, wants_to_enter)
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

    def remove_highlight(self, node_index):
        node, x, y = self.nodes[node_index]
        self.canvas.itemconfig(node, outline='#4682B4', width=3)

    def enter_critical_region(self, node_index):
        node, x, y = self.nodes[node_index]
        self.canvas.itemconfig(node, fill='#32CD32')
        self.canvas.create_line(x, y, self.center_x, self.center_y, fill='#32CD32', width=3, tags='token_line')
        self.critical_region_value = node_index + 1
        self.canvas.itemconfig(self.critical_region_value_text, text=str(self.critical_region_value))

    def leave_critical_region(self, node_index):
        node, x, y = self.nodes[node_index]
        self.canvas.itemconfig(node, fill='#87CEEB')
        self.canvas.delete('token_line')

    def start_token_passing(self):
        threading.Thread(target=self.pass_token, daemon=True).start()

    def stop(self):
        global root
        self.running = False
        root.destroy()


root = tk.Tk()

def main():
    root.title("Token Ring Algorithm Simulator")
    num_nodes = int(input("Enter the number of nodes: "))
    simulator = TokenRingSimulator(root, num_nodes)
    root.protocol("WM_DELETE_WINDOW", simulator.stop)
    root.mainloop()

if __name__ == "__main__":
    main()
