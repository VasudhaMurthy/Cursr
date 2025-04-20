import time
import math
import random
import threading
import tkinter as tk
from tkinter import messagebox
from mouse import get_position, on_click

positions = []
clicks = 0
recording = False
duration = 20

def euclidean(p1, p2):
    return math.sqrt((p1[1] - p2[1])**2 + (p1[2] - p2[2])**2)

def count_clicks():
    def on_mouse_click(*args):
        global clicks
        clicks += 1
    on_click(on_mouse_click)

def record_mouse():
    global recording, positions
    positions = []
    start_time = time.time()
    recording = True
    while recording:
        x, y = get_position()
        positions.append((time.time(), x, y))
        time.sleep(0.05)
        if time.time() - start_time > duration:
            recording = False
    analyze_data()

def analyze_data():
    total_distance = 0
    pause_count = 0
    speeds = []

    for i in range(1, len(positions)):
        dist = euclidean(positions[i-1], positions[i])
        time_diff = positions[i][0] - positions[i-1][0]
        if time_diff > 0:
            speed = dist / time_diff
            speeds.append(speed)
        total_distance += dist
        if dist < 1:
            pause_count += 1

    avg_speed = sum(speeds) / len(speeds) if speeds else 0

    if avg_speed > 300 and total_distance > 8000 and pause_count < 20:
        prediction = "🚀 Decisive & Fast Thinker"
    elif pause_count > 35 or avg_speed < 100:
        prediction = "🤔 Overthinker"
    elif total_distance > 15000:
        prediction = "🔍 Explorative Personality"
    elif clicks > 25:
        prediction = "🧠 Impulsive Clicker"
    elif 10000 > total_distance > 5000 and 100 < avg_speed < 300:
        prediction = "😌 Calm & Cautious"
    else:
        prediction = random.choice([
            "🧠 Creative Thinker",
            "🦉 Observant Explorer",
            "⚡ Speedy Navigator"
        ])

    messagebox.showinfo("Prediction Result", f"✨ Personality: {prediction}\n\n"
                        f"🖱️ Clicks: {clicks}\n"
                        f"📏 Distance: {total_distance:.2f} px\n"
                        f"⚡ Speed: {avg_speed:.2f} px/s\n"
                        f"⏸️ Pauses: {pause_count}")

def update_timer_label():
    for i in range(duration, 0, -1):
        timer_label.config(text=f"⏳ Tracking... {i} seconds left")
        time.sleep(1)
    timer_label.config(text="✅ Done! Analyzing...")

def start_tracking():
    global clicks
    clicks = 0
    instruction_label.config(text="🎯 Move your mouse and click around!")
    start_button.config(state="disabled", bg="#aaa")
    threading.Thread(target=count_clicks, daemon=True).start()
    threading.Thread(target=record_mouse, daemon=True).start()
    threading.Thread(target=update_timer_label, daemon=True).start()

# GUI
root = tk.Tk()
root.title("✨ Cursor Personality Predictor ✨")
root.geometry("500x400")
root.configure(bg="#f4f4fb")

title_label = tk.Label(root, text="🧠 Cursor Personality Predictor", font=("Helvetica", 18, "bold"), fg="#4b0082", bg="#f4f4fb")
title_label.pack(pady=20)

instruction_label = tk.Label(root, text="Click 'Start' and move your mouse freely for 20 seconds!", font=("Helvetica", 12), fg="#333", bg="#f4f4fb")
instruction_label.pack(pady=10)

start_button = tk.Button(root, text="▶️ Start", font=("Helvetica", 14), bg="#6c63ff", fg="white", width=15, height=2, command=start_tracking)
start_button.pack(pady=20)

timer_label = tk.Label(root, text="", font=("Helvetica", 14, "italic"), fg="#ff4500", bg="#f4f4fb")
timer_label.pack(pady=10)

credit = tk.Label(root, text="Made with ❤️ by MoVa", font=("Helvetica", 10), bg="#f4f4fb", fg="#888")
credit.pack(side="bottom", pady=10)

root.mainloop()
