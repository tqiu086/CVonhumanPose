import tkinter as tk
from tkinter import messagebox
import json
import os

def check_password():
    try:
        # Check if 'password.json' exists
        if os.path.exists("password.json"):
            with open("password.json", "r") as f:
                data = json.load(f)
                recorded_password = data.get("password", "No password recorded")
                output_text.delete(1.0, tk.END)  # Clear previous text
                output_text.insert(tk.END, f"Password found: {recorded_password}")
        else:
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, "Error: password.json not found")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Create the main window
root = tk.Tk()
root.title("Password Checker")
root.geometry("400x200")

# Output Textbox (Read-only)
output_label = tk.Label(root, text="Password Status:")
output_label.pack(pady=5)

output_text = tk.Text(root, height=5, width=50, wrap=tk.WORD)
output_text.pack(pady=5)
output_text.config(state="normal")  # Allow writing (but user can't edit)

# Check Button
check_button = tk.Button(
    root,
    text="Check Password File",
    command=check_password,
    bg="#4CAF50",
    fg="white",
    font=("Arial", 10)
)
check_button.pack(pady=10)

# Run the application
root.mainloop()
