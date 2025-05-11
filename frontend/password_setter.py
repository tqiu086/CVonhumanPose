import tkinter as tk
from tkinter import messagebox
import json
import os

class PasswordSetter:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Setter")
        self.root.geometry("300x300")
        
        self.password = []
        
        # Instructions Label
        self.label = tk.Label(
            root,
            text="Enter 4 digits (1-4 only):",
            font=("Arial", 12)
        )
        self.label.pack(pady=10)
        
        # Password Display (shows * for entered digits)
        self.display = tk.Label(
            root,
            text="____",
            font=("Courier", 24),
            fg="blue"
        )
        self.display.pack(pady=10)
        # Action Hints
        self.hint_label = tk.Label(
            root,
            text="1: Raise Left Hand   2: Raise Right Hand\n3: Raise Both Hands   4: Arms Outstretched",
            font=("Arial", 10),
            fg="gray"
        )
        self.hint_label.pack()
        # Keypad Frame
        self.keypad_frame = tk.Frame(root)
        self.keypad_frame.pack()
        
        # Create buttons 1-4
        for i in range(1, 5):
            button = tk.Button(
                self.keypad_frame,
                text=str(i),
                width=3,
                font=("Arial", 14),
                command=lambda x=i: self.add_digit(x)
            )
            button.grid(row=0, column=i-1, padx=5)

        # Backspace Button
        self.backspace_button = tk.Button(
            root,
            text="Backspace",
            width=10,
            command=self.backspace,
            bg="#9E9E9E",
            fg="white"
        )
        self.backspace_button.pack(pady=5)
        # Clear Button
        self.clear_button = tk.Button(
            root,
            text="Clear",
            width=10,
            command=self.clear_password,
            bg="#f44336",
            fg="white"
        )
        self.clear_button.pack(pady=10)
        
        # Submit Button (initially disabled)
        self.submit_button = tk.Button(
            root,
            text="Submit",
            width=10,
            state=tk.DISABLED,
            command=self.submit_password,
            bg="#4CAF50",
            fg="white"
        )
        self.submit_button.pack()
    
    def add_digit(self, digit):
        if len(self.password) < 4:
            self.password.append(str(digit))
            self.update_display()
            
            # Enable submit if 4 digits entered
            if len(self.password) == 4:
                self.submit_button.config(state=tk.NORMAL)
    
    def clear_password(self):
        self.password = []
        self.update_display()
        self.submit_button.config(state=tk.DISABLED)
    def backspace(self):
        if self.password:
            self.password.pop()
            self.update_display()
            self.submit_button.config(state=tk.DISABLED)
    def update_display(self):
        display_text = ""
        for i in range(4):
            if i < len(self.password):
                display_text += "*"
            else:
                display_text += "_"
        self.display.config(text=display_text)
    
    def submit_password(self):
        final_password = "".join(self.password)
        messagebox.showinfo(
            "Password Set",
            f"Password submitted: {final_password}"
        )
        # Optional: Save to file
        with open("password.json", "w") as f:
            json.dump({"password": final_password}, f)
        self.clear_password()

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordSetter(root)
    root.mainloop()