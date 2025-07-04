import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime

FILENAME = "tasks.json"


def load_tasks():
    if not os.path.exists(FILENAME):
        return[]
    with open(FILENAME, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_tasks(tasks):
    with open(FILENAME, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)


def generate_id(tasks):
    if not tasks:
        return 1
    return max(task['id'] for task in tasks) + 1


class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Задачи")
        self.tasks = load_tasks()

        self.listbox = tk.Listbox(root, width=100, height=40)
        self.listbox.pack(pady=10)

        self.refresh_task_list()

        button_frame = tk.Frame(root)
        button_frame.pack()

        tk.Button(button_frame, text="Добавить задачу", command=self.add_task).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Удалить", command=self.delete_task).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Сменить статус", command=self.toggle_status).grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="Сохранить", command=self.save).grid(row=0, column=3, padx=5)

    def refresh_task_list(self):
        self.listbox.delete(0, tk.END)
        for task in self.tasks:
            status = "✅" if task['completed'] else "❌"
            text = f"[{status}] {task['title']} — {task['due_date']}"
            self.listbox.insert(tk.END, text)

    def add_task(self):
        title = simpledialog.askstring("Новая задача", "Введите заголовок:")
        if not title:
            return
        description = simpledialog.askstring("Описание", "Введите описание:")
        due_date = simpledialog.askstring("Дата", "Введите дату (ГГГГ-ММ-ДД):")
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except Exception:
            messagebox.showerror("Ошибка", "Неверный формат даты")
            return

        new_task = {
            "id": generate_id(self.tasks),
            "title": title,
            "description": description,
            "due_date": due_date,
            "completed": False
        }
        self.tasks.append(new_task)
        self.refresh_task_list()

    def delete_task(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showinfo("Инфо", "Выберите задачу для удаления.")
            return
        index = selection[0]
        self.tasks.pop(index)
        self.refresh_task_list()

    def toggle_status(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showinfo("Инфо", "Выберите задачу для изменения статуса.")
            return
        index = selection[0]
        self.tasks[index]["completed"] = not self.tasks[index]["completed"]
        self.refresh_task_list()

    def save(self):
        save_tasks(self.tasks)
        messagebox.showinfo("Сохранение", "Задачи сохранены!")


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()