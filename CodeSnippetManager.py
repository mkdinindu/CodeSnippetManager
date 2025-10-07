import tkinter as tk
from tkinter import messagebox, scrolledtext
from collections import deque
import json
import pyperclip
import os

DATA_FILE = "snippets.json"
MAX_SNIPPETS = 50

# Load existing snippets
def load_snippets():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            return deque(data, maxlen=MAX_SNIPPETS)
    return deque(maxlen=MAX_SNIPPETS)

# Save snippets
def save_snippets():
    with open(DATA_FILE, "w") as f:
        json.dump(list(snippets), f, indent=4)

# Add new snippet
def add_snippet():
    title = title_entry.get().strip()
    code = code_text.get("1.0", tk.END).strip()

    if not title or not code:
        messagebox.showwarning("Warning", "Please enter both title and code!")
        return

    snippets.appendleft({"title": title, "code": code})
    update_listbox()
    save_snippets()
    title_entry.delete(0, tk.END)
    code_text.delete("1.0", tk.END)

# Update list display
def update_listbox():
    listbox.delete(0, tk.END)
    for snip in snippets:
        listbox.insert(tk.END, snip["title"])

# Show selected snippet
def show_snippet(event=None):
    selected = listbox.curselection()
    if not selected:
        return
    index = selected[0]
    snippet = snippets[index]
    code_text.delete("1.0", tk.END)
    code_text.insert(tk.END, snippet["code"])

# Copy snippet
def copy_snippet():
    selected = listbox.curselection()
    if not selected:
        messagebox.showinfo("Info", "No snippet selected.")
        return
    index = selected[0]
    pyperclip.copy(snippets[index]["code"])
    messagebox.showinfo("Copied", f"Snippet '{snippets[index]['title']}' copied!")

# Delete snippet
def delete_snippet():
    selected = listbox.curselection()
    if not selected:
        messagebox.showinfo("Info", "No snippet selected.")
        return
    index = selected[0]
    del snippets[index]
    update_listbox()
    save_snippets()

# Initialize app
root = tk.Tk()
root.title("Code Snippet Saver")
root.geometry("600x600")
root.resizable(False, False)

snippets = load_snippets()

# UI Components
tk.Label(root, text="Snippet Title:").pack(anchor="w", padx=10, pady=(10, 0))
title_entry = tk.Entry(root, width=50)
title_entry.pack(padx=10, pady=5)

tk.Label(root, text="Code:").pack(anchor="w", padx=10)
code_text = scrolledtext.ScrolledText(root, height=10, width=70)
code_text.pack(padx=10, pady=5)

tk.Button(root, text="Save Snippet", command=add_snippet).pack(pady=5)

# Snippet list
tk.Label(root, text="Recent Snippets:").pack(anchor="w", padx=10, pady=(10, 0))
listbox = tk.Listbox(root, height=8, width=60)
listbox.pack(padx=10, pady=5)
listbox.bind("<<ListboxSelect>>", show_snippet)

# Action buttons
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)
tk.Button(btn_frame, text="Copy", command=copy_snippet).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Delete", command=delete_snippet).grid(row=0, column=1, padx=5)

update_listbox()

root.mainloop()
save_snippets()
