#imports
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

#creates the main window
root = tk.Tk()
root.title("Smart Revision Planner")
root.geometry("1000x700")
root.configure(bg="#171A21")
root.rowconfigure(1, weight=1)
root.columnconfigure((0,1), weight=1, uniform="equal_columns")

#main heading
heading = tk.Label(
    root, 
    text="Smart Revision Planner", 
    bg="#171A21", 
    fg="#ffffff", 
    font = ("Arial", 24, "bold"), 
    padx=20, 
    pady=20
    )

heading.grid(row=0, column=0, columnspan=2, pady=5)

#creates frames
def create_frame(x, y, left_pad, right_pad):
    frame = tk.Frame(root, bg="#252A36")
    frame.grid(row=x, column=y, sticky="nsew", padx=(left_pad,right_pad))
    return frame

#frames
task_input_frame = create_frame(1,0,20,10)
task_input_frame.columnconfigure(0, weight=1)

task_output_frame = create_frame(1,1,10,20)
task_output_frame.rowconfigure(1, weight=1)
task_output_frame.columnconfigure(0, weight=1)

#creates headings
def create_heading(frame, label_text):
    heading = tk.Label(
        frame, 
        text=label_text, 
        bg="#252A36", 
        fg="#ffffff", 
        font = ("Arial", 16, "bold"), 
        padx=20, 
        pady=20
        )
    
    heading.grid(row=0, column=0, columnspan=2, sticky="nesw")
    return heading

#headings
task_input_heading = create_heading(task_input_frame, "Task Input Section")
task_output_heading = create_heading(task_output_frame, "Revision Tasks")

#creates entries and labels
def creates_entry_labels(label_text,frame,x):
    label = tk.Label(
        frame, 
        text=label_text, 
        bg="#252A36", 
        fg="#A8B0C2", 
        font = ("Arial", 11, "normal")
        )
    
    label.grid(row=x, column=0, sticky="w", padx=20)
    entry = tk.Entry(frame, bg="#171A21")
    entry.grid(row=x+1, column=0, sticky="ew", padx=20, pady=5)
    return label, entry

#validates difficulty
def validates_difficulty(entry):
    if entry.isdigit() and int(entry) >= 1 and int(entry) <= 5:
        return True
    elif entry == "":
        return True
    else:
        messagebox.showerror("showerror","Difficulty Must be an Integer Between 1 and 5")
        return False
    
#validates duration
def validates_duration(entry):
    if entry.isdigit() and int(entry) > 0:
        return True
    elif entry == "":
        return True
    else:
        messagebox.showerror("showerror","Duration Must be a Positive Integer")
        return False

#entries and labels
reg_validates_difficulty = root.register(validates_difficulty)
reg_validates_duration = root.register(validates_duration)

subject_label, subject_entry = creates_entry_labels("Subject",task_input_frame,2)
topic_label, topic_entry = creates_entry_labels("Topic",task_input_frame,4)
difficulty_label, difficulty_entry = creates_entry_labels("Difficulty (1-5)",task_input_frame,6)
deadline_label, deadline_entry = creates_entry_labels("Deadline (YYYY-MM-DD)",task_input_frame,8)
duration_label, duration_entry = creates_entry_labels("Duration (Minutes)",task_input_frame,10)

difficulty_entry.config(validate="key", validatecommand=(reg_validates_difficulty, "%P"))
duration_entry.config(validate="key", validatecommand=(reg_validates_duration, "%P"))

#clears entries
def clear_entries():
    for entry in (subject_entry, topic_entry, difficulty_entry, deadline_entry, duration_entry):
        entry.delete(0, tk.END)

tasks = []
task_row_index = 1

#add task button actions
def add_task():
    global task_row_index

    task_information = {
        "Subject": subject_entry.get(),
        "Topic": topic_entry.get(),
        "Difficulty": difficulty_entry.get(),
        "Deadline": deadline_entry.get(),
        "Duration": duration_entry.get(),
        "Completed": False
    }
    
    valid_entries = []

    for entry in task_information.values():
        if entry == "":
            valid_entries.append(False)
        else:
            valid_entries.append(True)

    #checks if deadline is in correct format
    if task_information["Deadline"] != "":
        try:
            datetime.strptime(task_information["Deadline"], "%Y-%m-%d")
        except ValueError:
            valid_entries[3] = False
            messagebox.showerror("showerror","Deadline Must be in YYYY-MM-DD format")

    #checks if all entries are filled
    if all(valid_entries):
        tasks.append(task_information)

        clear_entries()

        #updates task list
        create_task_card(task_information)
        task_row_index += 1

    else:
        messagebox.showerror("showerror","You Must Fill in All Entries to Add a Task")

#buttons
add_task_button = tk.Button(task_input_frame, text="Add Task", command=add_task)
add_task_button.grid(row=12, column=0, sticky="ew", padx=18, pady=10)

#creates task cards
def create_task_card(task_information):
    task_card = tk.Frame(revision_tasks_frame, bg="#171A21")
    task_card.grid(row=task_row_index, column=0, sticky="nesw", padx=20, pady=5)
    task_card.columnconfigure(0, weight=1)

    #creates task card labels
    def create_task_card_label(label_text, background_colour, font_colour, font_size, font_type, x, y, side, top_pad, bottom_pad, line_length):
        label = tk.Label(
            task_card, 
            text=label_text ,
            bg=background_colour, 
            fg=font_colour, 
            font = ("Arial", font_size, font_type), 
            wraplength=line_length
            )
        
        label.grid(row=x, column=y, sticky=side, padx=20, pady=(top_pad,bottom_pad))

    deadline_text = datetime.strptime(task_information["Deadline"], "%Y-%m-%d")

    create_task_card_label(task_information["Subject"], "#171A21", "#ffffff", 15, "bold", 0, 0, "w", 10, 5, 150)
    create_task_card_label(task_information["Topic"], "#171A21", "#D6DBE6", 12, "normal", 1, 0, "w", 0, 5, 200)
    create_task_card_label(deadline_text.strftime("%d %b %Y"), "#171A21", "#A8B0C2", 10, "normal", 2, 0, "w", 5, 10, 0)
    create_task_card_label("Difficulty " + str(task_information["Difficulty"]), "#303D59", "#93B4FF", 10, "bold", 0, 1, "e", 10, 5, 0)
    create_task_card_label(str(task_information["Duration"]) + " min", "#171A21", "#A8B0C2", 10, "normal", 2, 1, "e", 5, 10, 0)

#scrollable tasks
canvas = tk.Canvas(task_output_frame, bg="#252A36", highlightthickness=0)
canvas.grid(row=1, column=0, sticky="nesw")

scrollbar = ttk.Scrollbar(task_output_frame, orient="vertical", command=canvas.yview)
scrollbar.grid(row=1, column=1, sticky="ns")

canvas.configure(yscrollcommand=scrollbar.set)
revision_tasks_frame = tk.Frame(canvas, bg="#252A36")

revision_tasks_frame_id = canvas.create_window((0,0), window=revision_tasks_frame, anchor="nw")
revision_tasks_frame.columnconfigure(0, weight=1)
revision_tasks_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.bind("<Configure>", lambda event: canvas.itemconfigure(revision_tasks_frame_id, width = event.width))

#runs main loop
root.mainloop()
