#imports
import tkinter as tk

#creates the main window
root = tk.Tk() #initialises main window
root.title("Smart Revision Planner")
root.geometry("1000x700") #sets window size
root.configure(bg="#121212")

#adds window heading
heading = tk.Label(root, text="Smart Revision Planner", bg="#121212", fg="#ffffff", font = ("Arial", 20, "bold"), pady=50)
heading.pack() #adds item to window

#adds subject heading
subject_heading = tk.Label(root, text="Subjects", bg="#121212", fg="#ffffff", font = ("Arial", 20, "bold"), pady=50)
subject_heading.pack()

#Run the main loop
root.mainloop() #keeps window running until it's closed
