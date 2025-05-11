import tkinter as tk
from tkinter import messagebox
import json
import os

def check_password():
    try:
        if os.path.exists("password.json"):
            with open("password.json", "r") as f:
                data = json.load(f)
                recorded_password = data.get("password", "No password recorded")
                output_text.delete(1.0, tk.END)
                output_text.insert(tk.END, f"Password found: {recorded_password}")
        else:
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, "Error: password.json not found")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read file: {e}")

def refresh_file():
    try:
        if os.path.exists("password.json"):
            with open("password.json", "r") as f:
                json.load(f)  # Try to parse JSON
            # Show success popup
            popup = tk.Toplevel(root)
            popup.title("Refresh Status")
            popup.geometry("300x100")
            tk.Label(popup, text="✅ Successfully read password.json!", fg="green").pack(pady=20)
        else:
            # Show fail popup
            popup = tk.Toplevel(root)
            popup.title("Refresh Status")
            popup.geometry("300x100")
            tk.Label(popup, text="❌ Error: password.json not found!", fg="red").pack(pady=20)
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Invalid JSON format in password.json!")
    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error: {e}")

# Create the main window
root = tk.Tk()
root.title("Password Checker")
root.geometry("400x250")

# Output Textbox
output_label = tk.Label(root, text="Password Status:")
output_label.pack(pady=5)

output_text = tk.Text(root, height=5, width=50, wrap=tk.WORD)
output_text.pack(pady=5)
output_text.config(state="normal")

# Button Frame (for better layout)
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# Check Button
check_button = tk.Button(
    button_frame,
    text="Check Password",
    command=check_password,
    bg="#4CAF50",
    fg="white",
    font=("Arial", 10)
)
check_button.pack(side=tk.LEFT, padx=5)

# Refresh Button
refresh_button = tk.Button(
    button_frame,
    text="Refresh",
    command=refresh_file,
    bg="#2196F3",
    fg="white",
    font=("Arial", 10)
)
refresh_button.pack(side=tk.LEFT, padx=5)

# Run the application
root.mainloop()
