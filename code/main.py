#imports
import tkinter as tk

#creates the main window
root = tk.Tk()
root.title("Smart Revision Planner")
root.geometry("1000x700")
root.configure(bg="#171A21")
root.columnconfigure((0,1), weight=1, uniform="equal_columns")

heading = tk.Label(root, text="Smart Revision Planner", bg="#171A21", fg="#ffffff", font = ("Arial", 24, "bold"), padx=20, pady=20)
heading.grid(row=0, column=0, columnspan=2, pady=5)

#frames
def create_frame(x, y, left_pad, right_pad):
    frame = tk.Frame(root, bg="#252A36")
    frame.grid(row=x, column=y, sticky="nsew", padx=(left_pad,right_pad))
    return frame

task_input_frame = create_frame(1,0,20,10)
task_input_frame.columnconfigure(0, weight=1)
task_output_frame = create_frame(1,1,10,20)

#headings
def create_heading(frame, label_text, y):
    heading = tk.Label(frame, text=label_text, bg="#252A36", fg="#ffffff", font = ("Arial", 16, "bold"), padx=20, pady=20)
    heading.grid(row=1, column=y, sticky="nesw")
    return heading

task_input_heading = create_heading(task_input_frame, "Task Input Section", 0)
task_output_heading = create_heading(task_output_frame, "Revision Tasks", 1)

#entries
def creates_entry_labels(label_text,frame,x):
    label = tk.Label(frame, text=label_text, bg="#252A36", fg="#A8B0C2", font = ("Arial", 11, "normal"))
    label.grid(row=x, column=0, sticky="w", padx=20)
    entry = tk.Entry(frame, bg="#171A21")
    entry.grid(row=x+1, column=0, sticky="ew", padx=20, pady=5)
    return label, entry

subject_label, subject_entry = creates_entry_labels("Subject",task_input_frame,2)
topic_label, topic_entry = creates_entry_labels("Topic",task_input_frame,4)
difficulty_label, difficulty_entry = creates_entry_labels("Difficulty",task_input_frame,6)
deadline_label, deadline_entry = creates_entry_labels("Deadline",task_input_frame,8)
duration_label, duration_entry = creates_entry_labels("Duration",task_input_frame,10)

#buttons
def button_click():
    print(subject_entry.get())

add_task_button = tk.Button(task_input_frame, text="Add Task", command=button_click)
add_task_button.grid(row=12, column=0, sticky="ew", padx=18, pady=10)

#Run the main loop
root.mainloop()
