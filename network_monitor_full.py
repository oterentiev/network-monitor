import tkinter as tk
from tkinter import ttk
import random
import threading
import time

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class NetworkMonitorSystem:

    def __init__(self, root):

        self.root = root
        self.root.title("Інформаційна система діагностики локальної мережі")
        self.root.geometry("1200x700")

        self.running = False
        self.traffic_data = []

        self.create_ui()

    def create_ui(self):

        style = ttk.Style()
        style.theme_use("vista")

        top = ttk.Frame(self.root)
        top.pack(fill=tk.X, padx=10, pady=10)

        ttk.Button(top, text="Запуск", command=self.start_monitoring).pack(side=tk.LEFT, padx=5)
        ttk.Button(top, text="Зупинка", command=self.stop_monitoring).pack(side=tk.LEFT, padx=5)

        center = ttk.Frame(self.root)
        center.pack(fill=tk.BOTH, expand=True)

        left = ttk.LabelFrame(center, text="Графік трафіку")
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        right = ttk.LabelFrame(center, text="Параметри")
        right.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.figure, master=left)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        columns = ("Параметр", "Значення")

        self.table = ttk.Treeview(
            right,
            columns=columns,
            show="headings",
            height=12
        )

        self.table.heading("Параметр", text="Параметр")
        self.table.heading("Значення", text="Значення")

        self.table.pack(fill=tk.BOTH, expand=True)

        self.log = tk.Text(self.root, height=8)
        self.log.pack(fill=tk.X, padx=10, pady=10)

    def write_log(self, text):
        self.log.insert(tk.END, text + "\\n")
        self.log.see(tk.END)

    def start_monitoring(self):

        if not self.running:
            self.running = True

            self.write_log("Моніторинг мережі запущено")

            thread = threading.Thread(target=self.monitor)
            thread.daemon = True
            thread.start()

    def stop_monitoring(self):

        self.running = False
        self.write_log("Моніторинг зупинено")

    def monitor(self):

        while self.running:

            traffic = random.randint(10, 100)

            self.traffic_data.append(traffic)

            if len(self.traffic_data) > 25:
                self.traffic_data.pop(0)

            self.update_chart()
            self.update_table(traffic)

            time.sleep(1)

    def moving_average(self, data, window=5):

        if len(data) < window:
            return sum(data) / len(data)

        return sum(data[-window:]) / window

    def update_chart(self):

        self.ax.clear()

        self.ax.plot(self.traffic_data, label="Трафік")

        forecast = self.moving_average(self.traffic_data)

        self.ax.axhline(
            y=forecast,
            linestyle="--",
            label="Прогноз"
        )

        self.ax.set_title("Аналіз часових рядів")
        self.ax.legend()

        self.canvas.draw()

    def update_table(self, traffic):

        for item in self.table.get_children():
            self.table.delete(item)

        self.table.insert("", tk.END, values=("Ethernet", "Активний"))
        self.table.insert("", tk.END, values=("Wi‑Fi", "Активний"))
        self.table.insert("", tk.END, values=("LTE/5G", "Резерв"))
        self.table.insert("", tk.END, values=("Трафік", f"{traffic} Mbps"))
        self.table.insert("", tk.END, values=("QoS", "Нормальний"))


if __name__ == "__main__":

    root = tk.Tk()

    app = NetworkMonitorSystem(root)

    root.mainloop()
