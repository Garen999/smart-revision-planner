#imports
import json
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

#images
bin_icon = tk.PhotoImage(file="images/bin_icon.png")
bin_icon = bin_icon.subsample(24,24)

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
def create_frame(x, y, sides, left_pad, right_pad):
    frame = tk.Frame(root, bg="#252A36")
    frame.grid(row=x, column=y, sticky=sides, padx=(left_pad,right_pad))
    return frame

#frames
task_input_frame = create_frame(1,0,"new",20,10)
task_input_frame.columnconfigure(0, weight=1)

task_output_frame = create_frame(1,1,"nesw",10,20)
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
deadline_label, deadline_entry = creates_entry_labels("Deadline (DD-MM-YYYY)",task_input_frame,8)
duration_label, duration_entry = creates_entry_labels("Duration (Minutes)",task_input_frame,10)

difficulty_entry.config(validate="key", validatecommand=(reg_validates_difficulty, "%P"))
duration_entry.config(validate="key", validatecommand=(reg_validates_duration, "%P"))

#clears entries
def clear_entries():
    for entry in (subject_entry, topic_entry, difficulty_entry, deadline_entry, duration_entry):
        entry.delete(0, tk.END)

tasks = []

#add task button actions
def add_task():
    global task_row_index

    task_information = {
        "Subject": subject_entry.get(),
        "Topic": topic_entry.get(),
        "Difficulty": difficulty_entry.get(),
        "Deadline": deadline_entry.get(),
        "Duration": duration_entry.get(),
        "Completed": False,
        "Priority": 0,
        "Widget": None
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
            datetime.strptime(task_information["Deadline"], "%d-%m-%Y")
        except ValueError:
            valid_entries[3] = False
            messagebox.showerror("showerror","Deadline Must be in DD-MM-YYYY format")

    #checks if all entries are filled
    if all(valid_entries):
        tasks.append(task_information)

        clear_entries()

        #updates task list
        task_information["Widget"] = create_task_card(task_information)
        ranks_tasks()
        saves_data()

    else:
        messagebox.showerror("showerror","You Must Fill in All Entries to Add a Task")

#buttons
add_task_button = tk.Button(task_input_frame, text="Add Task", command=add_task)
add_task_button.grid(row=12, column=0, sticky="ew", padx=18, pady=10)

#creates task cards
def create_task_card(task_information):
    task_card = tk.Frame(revision_tasks_frame, bg="#171A21")
    task_card.grid(row=tasks.index(task_information) + 1, column=0, sticky="nesw", padx=20, pady=5)
    task_card.columnconfigure(1, weight=1)

    #delete task button
    def delete_task():
        task_card.destroy()
        tasks.remove(task_information)
        ranks_tasks()
        saves_data()

    delete_button = tk.Label(task_card, image=bin_icon, bg="#171A21", cursor="hand2")
    delete_button.grid(row=1, column=2, sticky="e", padx=10)
    delete_button.bind("<Button-1>", lambda event:delete_task())

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
        
        label.grid(row=x, column=y, sticky=side, padx=10, pady=(top_pad,bottom_pad))
        return label
    
    deadline_text = datetime.strptime(task_information["Deadline"], "%d-%m-%Y")
    days = abs((deadline_text - datetime.now()).days)

    days_text = " (Overdue)" if deadline_text < datetime.now() else " (" + str(days)+ " days away)"

    task_card_subject_label = create_task_card_label(task_information["Subject"], "#171A21", "#ffffff", 15, "bold", 0, 1, "w", 10, 5, 250)

    create_task_card_label(task_information["Topic"], "#171A21", "#D6DBE6", 12, "normal", 1, 1, "w", 0, 5, 200)

    create_task_card_label(
        deadline_text.strftime("%d %b %Y") + days_text + " · " + str(task_information["Duration"]) + " min", 
        "#171A21", 
        "#A8B0C2", 
        10, 
        "normal", 
        2, 1, "w", 5, 10, 0
        )
    
    create_task_card_label("Difficulty " + str(task_information["Difficulty"]), "#303D59", "#93B4FF", 10, "bold", 0, 2, "e", 10, 5, 0)

    #complete task button
    def complete_task():
        if complete_button_state.get():
            task_information["Completed"] = True
            task_card_subject_label.configure(fg="#00FF00")
        else:
            task_information["Completed"] = False
            task_card_subject_label.configure(fg="#FFFFFF")
        ranks_tasks()
        saves_data()

    complete_button_state = tk.BooleanVar(value=task_information["Completed"])

    complete_button = tk.Checkbutton(
        task_card, 
        bg="#171A21", 
        variable=complete_button_state, 
        command=complete_task
        )
    
    complete_button.grid(row=0, column=0, sticky="w", padx=10, pady=(10,5))

    return task_card

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

# #determines task priority
def ranks_tasks():
    global tasks

    for task in tasks:
        days = (datetime.strptime(task["Deadline"], "%d-%m-%Y") - datetime.now()).days

        if task["Completed"]: 
            score = 0
        elif days <=0:
            score = 0
        else:
            score = int(task["Difficulty"])*int(task["Duration"])/days

        task["Priority"] = score

    tasks = sorted(tasks, key=lambda x: x["Priority"], reverse=True)

    for i, task in enumerate(tasks):
        task["Widget"].grid(row=i+ 1, column=0, sticky="nesw", padx=20, pady=5)

#saves task data
def saves_data():
    saved_tasks = [
        {key: value for key, value in task.items() if key!="Widget"}
        for task in tasks
    ]

    with open("data/task_data.json","w") as task_data_file:
        json.dump(saved_tasks, task_data_file, indent=4)

#loads task data
def loads_data():
    global tasks

    with open("data/task_data.json","r") as task_data_file:
        try:
            tasks = json.load(task_data_file)
        except json.JSONDecodeError as e:
            print("Invalid JSON syntax:", e)

    for task in tasks:
        task.update({"Widget": create_task_card(task)})

    ranks_tasks()

loads_data()

#runs main loop
root.mainloop()