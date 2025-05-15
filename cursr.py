
# import tkinter as tk
# from tkinter import ttk
# import threading
# import time
# import mouse
# import math

# class CursrApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Cursr - Cursor Personality Predictor")
#         self.root.geometry("400x300")
#         self.root.configure(bg="#2c3e50")

#         self.label = tk.Label(root, text="Welcome to Cursr!", font=("Arial", 18), bg="#2c3e50", fg="white")
#         self.label.pack(pady=20)

#         self.status_label = tk.Label(root, text="", font=("Arial", 14), bg="#2c3e50", fg="lightgreen")
#         self.status_label.pack(pady=10)

#         self.countdown_label = tk.Label(root, text="", font=("Arial", 24), bg="#2c3e50", fg="white")
#         self.countdown_label.pack(pady=10)

#         self.start_button = ttk.Button(root, text="Start Tracking", command=self.start_tracking)
#         self.start_button.pack(pady=20)

#         self.tracking_time = 20  # seconds

#         # For counting clicks
#         self.click_count = 0
#         self.click_lock = threading.Lock()

#     def start_tracking(self):
#         self.start_button.config(state='disabled')
#         self.status_label.config(text="Tracking started...")
#         self.click_count = 0
#         # Start mouse click listener
#         mouse.on_click(lambda: self.on_click)
#         # Start tracking in a separate thread
#         threading.Thread(target=self.track_mouse).start()

#     def on_click(self):
#         with self.click_lock:
#             self.click_count += 1

#     def track_mouse(self):
#         start_time = time.time()
#         end_time = start_time + self.tracking_time

#         movements = []

#         while time.time() < end_time:
#             pos = mouse.get_position()
#             movements.append(pos)
#             remaining = int(end_time - time.time())
#             self.update_countdown(remaining)
#             time.sleep(0.05)

#         self.update_countdown(0)
#         mouse.unhook_all()  # Stop click listener
#         self.status_label.config(text="Tracking complete!")
#         self.start_button.config(state='normal')

#         personality = self.analyze_movements(movements, self.click_count)
#         self.status_label.config(text=f"Personality: {personality}")

#     def update_countdown(self, seconds):
#         self.root.after(0, lambda: self.countdown_label.config(text=f"Time left: {seconds} s"))

#     def analyze_movements(self, data, clicks):
#         if len(data) < 2:
#             return "Calm and Focused"

#         total_distance = 0
#         idle_count = 0
#         threshold_idle = 5  # pixels, small movement = idle

#         for i in range(1, len(data)):
#             x1, y1 = data[i-1]
#             x2, y2 = data[i]
#             dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
#             total_distance += dist
#             if dist < threshold_idle:
#                 idle_count += 1

#         avg_speed = total_distance / len(data)
#         idle_ratio = idle_count / len(data)
#         click_rate = clicks / self.tracking_time

#         # Personality rules combining features

#         if avg_speed > 20 and click_rate > 2:
#             return "Impulsive"
#         elif avg_speed < 5 and idle_ratio > 0.6 and click_rate < 1:
#             return "Calm and Focused"
#         elif idle_ratio > 0.4 and click_rate < 0.5:
#             return "Overthinker"
#         elif avg_speed > 10 and idle_ratio > 0.3 and click_rate > 1:
#             return "Distracted"
#         elif avg_speed < 10 and click_rate > 3:
#             return "Energetic"
#         else:
#             return "Balanced"

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = CursrApp(root)
#     root.mainloop()


import tkinter as tk
from tkinter import ttk
import threading
import time
import mouse
import math

class CursrApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cursr - Cursor Personality Predictor")
        self.root.geometry("500x400")
        self.root.configure(bg="#1e1e2f")

        # Title
        self.title_label = tk.Label(root, text="Cursr", font=("Helvetica", 28, "bold"), bg="#1e1e2f", fg="#00ffcc")
        self.title_label.pack(pady=10)

        # Instructions
        self.instructions = tk.Label(root, text="Click Start and move your mouse around!\nWe’ll analyze your style in 20 seconds.",
                                     font=("Helvetica", 12), bg="#1e1e2f", fg="white")
        self.instructions.pack()

        # Status
        self.status_label = tk.Label(root, text="", font=("Helvetica", 14), bg="#1e1e2f", fg="#ffffff")
        self.status_label.pack(pady=10)

        # Countdown
        self.countdown_label = tk.Label(root, text="", font=("Helvetica", 20), bg="#1e1e2f", fg="#ffcc00")
        self.countdown_label.pack()

        # Start Button
        self.start_button = ttk.Button(root, text="Start Tracking", command=self.start_tracking)
        self.start_button.pack(pady=20)

        # Output
        self.output_text = tk.Text(root, height=8, width=58, wrap='word', bg="#111", fg="white", font=("Courier", 10))
        self.output_text.pack(pady=10)
        self.output_text.config(state='disabled')

        # Variables
        self.tracking_time = 20
        self.click_count = 0
        self.click_lock = threading.Lock()

    def start_tracking(self):
        self.start_button.config(state='disabled')
        self.output_text.config(state='normal')
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state='disabled')
        self.status_label.config(text="Tracking started...")
        self.click_count = 0
        mouse.on_click(self.on_click)
        threading.Thread(target=self.track_mouse).start()

    def on_click(self):
        with self.click_lock:
            self.click_count += 1

    def track_mouse(self):
        start_time = time.time()
        end_time = start_time + self.tracking_time
        movements = []

        while time.time() < end_time:
            pos = mouse.get_position()
            movements.append(pos)
            remaining = int(end_time - time.time())
            self.update_countdown(remaining)
            time.sleep(0.05)

        mouse.unhook_all()
        self.update_countdown(0)
        self.status_label.config(text="Tracking complete!")
        self.start_button.config(state='normal')

        personality, analysis = self.analyze_movements(movements, self.click_count)
        self.show_results(personality, analysis)

    def update_countdown(self, seconds):
        self.root.after(0, lambda: self.countdown_label.config(text=f"Time left: {seconds}s"))

    def analyze_movements(self, data, clicks):
        if len(data) < 2:
            return "Calm and Focused", "Insufficient data collected."

        total_distance = 0
        idle_count = 0
        threshold_idle = 5

        for i in range(1, len(data)):
            x1, y1 = data[i-1]
            x2, y2 = data[i]
            dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            total_distance += dist
            if dist < threshold_idle:
                idle_count += 1

        avg_speed = total_distance / len(data)
        idle_ratio = idle_count / len(data)
        click_rate = clicks / self.tracking_time

        if avg_speed > 20 and click_rate > 2:
            personality = "Impulsive"
        elif avg_speed < 5 and idle_ratio > 0.6 and click_rate < 1:
            personality = "Calm and Focused"
        elif idle_ratio > 0.4 and click_rate < 0.5:
            personality = "Overthinker"
        elif avg_speed > 10 and idle_ratio > 0.3 and click_rate > 1:
            personality = "Distracted"
        elif avg_speed < 10 and click_rate > 3:
            personality = "Energetic"
        else:
            personality = "Balanced"

        analysis = (
            f"Total Movement Distance: {total_distance:.2f} pixels\n"
            f"Average Speed: {avg_speed:.2f} pixels/frame\n"
            f"Idle Time Ratio: {idle_ratio*100:.1f}%\n"
            f"Click Rate: {click_rate:.2f} clicks/sec\n"
        )

        return personality, analysis

    def show_results(self, personality, analysis):
        self.output_text.config(state='normal')
        self.output_text.insert(tk.END, f"🧠 Personality Type: {personality}\n\n")
        self.output_text.insert(tk.END, f"📊 Analysis:\n{analysis}")
        self.output_text.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = CursrApp(root)
    root.mainloop()
