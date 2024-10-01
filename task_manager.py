import tkinter as tk
from tkinter import messagebox
import time
import threading

# Global list to store tasks
tasks = []

def update_task_status(task, task_label, time_rem_label, edit_button):
    amber_popup_shown = False

    while task['remaining_time'] > 0 and not task['done']:
        mins, secs = divmod(task['remaining_time'], 60)
        time_rem_label.config(text=f"{int(mins)} min {int(secs)} sec")

        if task['remaining_time'] <= 120 and not task['done']:
            task_label.config(bg="orange")  # Amber color
            if not amber_popup_shown:
                show_notification(f"Reminder [AMBER TASK]: {task['text']} - 2 minutes left!")
                amber_popup_shown = True
        else:
            task_label.config(bg="lightgray")  # Gray color

        time.sleep(1)
        task['remaining_time'] -= 1

    if not task['done']:
        task_label.config(bg="red")
        edit_button.config(state=tk.DISABLED)  # Disable edit button
        task['time_up'] = True
        show_notification(f"Reminder: {task['text']} - Time's Up!")

def show_notification(reminder_text):
    messagebox.showinfo("Reminder", f"Reminder: {reminder_text}")

def mark_done(task_label, task, time_rem_label):
    task['done'] = True
    task_label.config(bg="green")
    time_rem_label.config(text="Completed")  # Stop the countdown
    # No further updates to this task since it's done

def edit_task(task, task_label, time_rem_label, edit_button):
    if task.get('time_up'):
        messagebox.showinfo("Cannot Edit", "Please create a new task.")
        return

    edit_window = tk.Toplevel(root)
    edit_window.title("Edit Task")

    tk.Label(edit_window, text="New Task Name:").pack(pady=5)
    task_entry = tk.Entry(edit_window, width=30)
    task_entry.insert(0, task['text'])
    task_entry.pack(pady=5)

    tk.Label(edit_window, text="New Time (in minutes):").pack(pady=5)
    time_entry = tk.Entry(edit_window, width=10)
    time_entry.insert(0, str(task['remaining_time'] / 60))
    time_entry.pack(pady=5)

    def save_task():
        new_text = task_entry.get()
        try:
            new_time = float(time_entry.get()) * 60
            if new_text and new_time > 0:
                task['text'] = new_text
                task['remaining_time'] = new_time
                task_label.config(text=new_text)
                time_rem_label.config(text=f"{int(new_time // 60)} min")
                edit_window.destroy()
            else:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid task name and time.")

    tk.Button(edit_window, text="Save", command=save_task).pack(pady=10)

def delete_task(task_frame, task):
    task['done'] = True
    task_frame.destroy()
    tasks.remove(task)

def check_duplicate_task(task_name):
    for task in tasks:
        if task_name == task['text'] and not task['done']:
            return True
    return False

def start_timer():
    try:
        minutes = float(time_input.get())
        reminder_text = reminder_input.get()

        if minutes <= 0 or not reminder_text:
            raise ValueError

        if check_duplicate_task(reminder_text):
            show_notification(f"Task already exists: {reminder_text}")
            return

        total_seconds = minutes * 60

        task = {
            'text': reminder_text,
            'remaining_time': total_seconds,
            'done': False,
            'time_up': False
        }
        tasks.append(task)

        task_frame_row = tk.Frame(task_list_frame, bg="white")
        task_frame_row.pack(fill="x", pady=2)

        serial_no = len(tasks)
        serial_label = tk.Label(task_frame_row, text=str(serial_no), width=5, font=("Helvetica", 12), bg="lightgray", relief=tk.GROOVE)
        serial_label.pack(side="left", fill="x")

        task_label = tk.Label(task_frame_row, text=reminder_text, width=20, font=("Helvetica", 12), bg="lightgray", relief=tk.GROOVE, wraplength=150, justify="left")
        task_label.pack(side="left", fill="x", padx=5)

        time_rem_label = tk.Label(task_frame_row, text=f"{int(minutes)} min", width=20, font=("Helvetica", 12), bg="lightgray", relief=tk.GROOVE)
        time_rem_label.pack(side="left", fill="x", padx=5)

        done_button = tk.Button(task_frame_row, text="Done", command=lambda: mark_done(task_label, task, time_rem_label))
        done_button.pack(side="left", padx=5)

        edit_button = tk.Button(task_frame_row, text="Edit", command=lambda: edit_task(task, task_label, time_rem_label, edit_button))
        edit_button.pack(side="left", padx=5)

        delete_button = tk.Button(task_frame_row, text="Delete", command=lambda: delete_task(task_frame_row, task))
        delete_button.pack(side="left", padx=5)

        threading.Thread(target=update_task_status, args=(task, task_label, time_rem_label, edit_button)).start()

    except ValueError:
        messagebox.showerror("Error", "Please enter a valid time and message.")

def start_thread():
    t = threading.Thread(target=start_timer)
    t.start()

# Initialize the tkinter window
root = tk.Tk()
root.title("Alarm Reminder with Task List")
root.geometry("800x400")
root.config(bg="#f0f8ff")

header = tk.Label(root, text="Set Your Alarm Reminder", font=("Helvetica", 16), bg="#4682B4", fg="white", padx=20, pady=10)
header.pack(fill="x")

reminder_label = tk.Label(root, text="Reminder Message", font=("Helvetica", 12), bg="#f0f8ff")
reminder_label.pack(pady=10)
reminder_input = tk.Entry(root, font=("Helvetica", 12), width=30)
reminder_input.pack(pady=5)

time_label = tk.Label(root, text="Set Time (in minutes)", font=("Helvetica", 12), bg="#f0f8ff")
time_label.pack(pady=10)
time_input = tk.Entry(root, font=("Helvetica", 12), width=10)
time_input.pack(pady=5)

submit_button = tk.Button(root, text="Start Alarm", font=("Helvetica", 12), bg="#4682B4", fg="white", command=start_thread)
submit_button.pack(pady=20)

# Task List Header
task_list_header = tk.Frame(root, bg="#f0f8ff")
task_list_header.pack(fill="x", padx=20)

serial_no_header = tk.Label(task_list_header, text="No.", font=("Helvetica", 12, "bold"), bg="#f0f8ff")
serial_no_header.pack(side="left", fill="x", padx=5)

task_header = tk.Label(task_list_header, text="Task Description", font=("Helvetica", 12, "bold"), bg="#f0f8ff")
task_header.pack(side="left", fill="x", padx=5)

time_rem_header = tk.Label(task_list_header, text="Time Remaining", font=("Helvetica", 12, "bold"), bg="#f0f8ff")
time_rem_header.pack(side="left", fill="x", padx=5)

# Frame for the task list
task_list_frame = tk.Frame(root, bg="#f0f8ff", relief=tk.SUNKEN, bd=2)
task_list_frame.pack(fill="both", expand=True, padx=20, pady=20)

root.mainloop()
