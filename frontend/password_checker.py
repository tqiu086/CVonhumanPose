import tkinter as tk
from tkinter import messagebox
import json
import os

original_password = None  # 全局变量保存 password.json 的密码
check_password_value = None  # 保存 checkpassword.json 的密码

# 初始化时读取 password.json
def load_original_password():
    global original_password
    try:
        if os.path.exists("password.json"):
            with open("password.json", "r") as f:
                data = json.load(f)
                original_password = data.get("password", None)
                output_text.delete(1.0, tk.END)
                output_text.insert(tk.END, f"Original password loaded: {original_password}")
        else:
            output_text.insert(tk.END, "Error: password.json not found")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read password.json: {e}")

# 点击 Refresh：读取 checkpassword.json 并显示密码
def refresh_file():
    global check_password_value
    try:
        if os.path.exists("checkpassword.json"):
            with open("checkpassword.json", "r") as f:
                data = json.load(f)
                check_password_value = data.get("password", None)

            popup = tk.Toplevel(root)
            popup.title("Refresh Status")
            popup.geometry("300x100")
            tk.Label(popup, text=f"✅ checkpassword: {check_password_value}", fg="green").pack(pady=20)

            # 更新文本框显示
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, f"Check password loaded: {check_password_value}")
        else:
            popup = tk.Toplevel(root)
            popup.title("Refresh Status")
            popup.geometry("300x100")
            tk.Label(popup, text="❌ Error: checkpassword.json not found!", fg="red").pack(pady=20)
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Invalid JSON format in checkpassword.json!")
    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error: {e}")

# 点击 Check：比较两个 password 是否一致
def check_password():
    if original_password is None:
        messagebox.showwarning("Warning", "Original password not loaded!")
        return
    if check_password_value is None:
        messagebox.showwarning("Warning", "Check password not loaded!")
        return

    if original_password == check_password_value:
        messagebox.showinfo("Match Result", "✅ Passwords match!")
    else:
        messagebox.showerror("Match Result", "❌ Passwords do NOT match!")

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

# Button Frame
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

# 加载初始密码
load_original_password()

# Run the application
root.mainloop()
