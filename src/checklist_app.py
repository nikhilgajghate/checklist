import json
import os
import tkinter as tk
from datetime import datetime
from tkinter import messagebox
from typing import Any, Dict, List

import customtkinter as ctk  # type: ignore

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class ChecklistApp:
    def __init__(self) -> None:
        self.root = ctk.CTk()
        self.root.title("Daily Checklist")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)

        # Data storage
        self.tasks: List[Dict[str, Any]] = []
        self.data_file = "checklist_data.json"

        # Load existing data
        self.load_data()

        # Create UI
        self.create_widgets()

    def create_widgets(self) -> None:
        # Main container
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Header
        header_frame = ctk.CTkFrame(main_frame)
        header_frame.pack(fill="x", padx=10, pady=(10, 20))

        title_label = ctk.CTkLabel(
            header_frame,
            text="📋 Daily Checklist",
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        title_label.pack(pady=10)

        date_label = ctk.CTkLabel(
            header_frame,
            text=datetime.now().strftime("%B %d, %Y"),
            font=ctk.CTkFont(size=14),
        )
        date_label.pack(pady=(0, 10))

        # Input section
        input_frame = ctk.CTkFrame(main_frame)
        input_frame.pack(fill="x", padx=10, pady=(0, 20))

        # Task input
        task_label = ctk.CTkLabel(
            input_frame, text="Add new task:", font=ctk.CTkFont(size=14, weight="bold")
        )
        task_label.pack(anchor="w", padx=10, pady=(10, 5))

        self.task_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Enter your task here...",
            height=35,
            font=ctk.CTkFont(size=14),
        )
        self.task_entry.pack(fill="x", padx=10, pady=(0, 10))

        # Add button
        add_button = ctk.CTkButton(
            input_frame,
            text="Add Task",
            command=self.add_task,
            height=35,
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        add_button.pack(pady=(0, 10))

        # Tasks section
        tasks_frame = ctk.CTkFrame(main_frame)
        tasks_frame.pack(fill="both", expand=True, padx=10)

        tasks_label = ctk.CTkLabel(
            tasks_frame, text="Your Tasks:", font=ctk.CTkFont(size=16, weight="bold")
        )
        tasks_label.pack(anchor="w", padx=10, pady=10)

        # Scrollable frame for tasks
        self.tasks_container = ctk.CTkScrollableFrame(tasks_frame)
        self.tasks_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Bottom buttons
        bottom_frame = ctk.CTkFrame(main_frame)
        bottom_frame.pack(fill="x", padx=10, pady=(10, 0))

        clear_completed_btn = ctk.CTkButton(
            bottom_frame,
            text="Clear Completed",
            command=self.clear_completed,
            height=35,
            font=ctk.CTkFont(size=12),
        )
        clear_completed_btn.pack(side="left", padx=(0, 10))

        clear_all_btn = ctk.CTkButton(
            bottom_frame,
            text="Clear All",
            command=self.clear_all,
            height=35,
            font=ctk.CTkFont(size=12),
        )
        clear_all_btn.pack(side="left")

        # Progress indicator
        self.progress_label = ctk.CTkLabel(
            bottom_frame, text="0/0 tasks completed", font=ctk.CTkFont(size=12)
        )
        self.progress_label.pack(side="right", padx=10)

        # Bind Enter key to add task
        self.task_entry.bind("<Return>", lambda event: self.add_task())

        # Update display
        self.update_tasks_display()

    def add_task(self) -> None:
        task_text = self.task_entry.get().strip()
        if task_text:
            task = {
                "id": len(self.tasks) + 1,
                "text": task_text,
                "completed": False,
                "created_at": datetime.now().isoformat(),
            }
            self.tasks.append(task)
            self.task_entry.delete(0, tk.END)
            self.update_tasks_display()
            self.save_data()
        else:
            messagebox.showwarning("Warning", "Please enter a task!")

    def toggle_task(self, task_id: int) -> None:
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = not task["completed"]
                break
        self.update_tasks_display()
        self.save_data()

    def delete_task(self, task_id: int) -> None:
        self.tasks = [task for task in self.tasks if task["id"] != task_id]
        self.update_tasks_display()
        self.save_data()

    def clear_completed(self) -> None:
        self.tasks = [task for task in self.tasks if not task["completed"]]
        self.update_tasks_display()
        self.save_data()

    def clear_all(self) -> None:
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all tasks?"):
            self.tasks = []
            self.update_tasks_display()
            self.save_data()

    def update_tasks_display(self) -> None:
        # Clear existing widgets
        for widget in self.tasks_container.winfo_children():
            widget.destroy()

        # Add task widgets
        for task in self.tasks:
            task_frame = ctk.CTkFrame(self.tasks_container)
            task_frame.pack(fill="x", padx=5, pady=2)

            # Checkbox
            checkbox = ctk.CTkCheckBox(
                task_frame,
                text="",
                command=lambda t=task["id"]: self.toggle_task(t),
                width=20,
            )
            checkbox.pack(side="left", padx=(10, 5))
            checkbox.select() if task["completed"] else checkbox.deselect()

            # Task text
            task_text = task["text"]
            if task["completed"]:
                task_text = f"~~{task_text}~~"

            task_label = ctk.CTkLabel(
                task_frame, text=task_text, font=ctk.CTkFont(size=14), wraplength=500
            )
            task_label.pack(side="left", fill="x", expand=True, padx=5)

            if task["completed"]:
                task_label.configure(text_color="gray")

            # Delete button
            delete_btn = ctk.CTkButton(
                task_frame,
                text="🗑️",
                width=30,
                height=25,
                command=lambda t=task["id"]: self.delete_task(t),
                font=ctk.CTkFont(size=12),
            )
            delete_btn.pack(side="right", padx=5)

        # Update progress
        completed = sum(1 for task in self.tasks if task["completed"])
        total = len(self.tasks)
        self.progress_label.configure(text=f"{completed}/{total} tasks completed")

    def save_data(self) -> None:
        try:
            with open(self.data_file, "w") as f:
                json.dump(self.tasks, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {e}")

    def load_data(self) -> None:
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, "r") as f:
                    self.tasks = json.load(f)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {e}")
            self.tasks = []

    def run(self) -> None:
        self.root.mainloop()


if __name__ == "__main__":
    app = ChecklistApp()
    app.run()
