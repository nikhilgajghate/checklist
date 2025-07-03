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

    def edit_task(self, task_id: int) -> None:
        """Open edit dialog for a task"""
        # Find the task
        task = None
        for t in self.tasks:
            if t["id"] == task_id:
                task = t
                break
        
        if not task:
            return
        
        # Create edit dialog
        edit_window = ctk.CTkToplevel(self.root)
        edit_window.title("Edit Task")
        edit_window.geometry("500x150")
        edit_window.resizable(False, False)
        edit_window.transient(self.root)  # Make it modal
        edit_window.grab_set()  # Make it modal
        
        # Center the dialog
        edit_window.update_idletasks()
        x = (edit_window.winfo_screenwidth() // 2) - (500 // 2)
        y = (edit_window.winfo_screenheight() // 2) - (150 // 2)
        edit_window.geometry(f"500x150+{x}+{y}")
        
        # Create dialog content
        dialog_frame = ctk.CTkFrame(edit_window)
        dialog_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Label
        label = ctk.CTkLabel(
            dialog_frame,
            text="Edit task:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        label.pack(anchor="w", padx=10, pady=(10, 5))
        
        # Entry field
        entry = ctk.CTkEntry(
            dialog_frame,
            height=35,
            font=ctk.CTkFont(size=14)
        )
        entry.pack(fill="x", padx=10, pady=(0, 15))
        entry.insert(0, task["text"])
        entry.select_range(0, tk.END)  # Select all text
        entry.focus()
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(dialog_frame)
        buttons_frame.pack(fill="x", padx=10)
        
        # Save button
        save_btn = ctk.CTkButton(
            buttons_frame,
            text="Save",
            command=lambda: self.save_edit(task_id, entry.get().strip(), edit_window),
            height=30,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        save_btn.pack(side="right", padx=(5, 0))
        
        # Cancel button
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Cancel",
            command=edit_window.destroy,
            height=30,
            font=ctk.CTkFont(size=12)
        )
        cancel_btn.pack(side="right")
        
        # Bind Enter key to save
        entry.bind("<Return>", lambda event: self.save_edit(task_id, entry.get().strip(), edit_window))
        # Bind Escape key to cancel
        entry.bind("<Escape>", lambda event: edit_window.destroy())
    
    def save_edit(self, task_id: int, new_text: str, window) -> None:
        """Save the edited task text"""
        if not new_text.strip():
            messagebox.showwarning("Warning", "Task text cannot be empty!")
            return
        
        # Update the task
        for task in self.tasks:
            if task["id"] == task_id:
                task["text"] = new_text.strip()
                break
        
        # Close the dialog and update display
        window.destroy()
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
            
            # Bind double-click to edit task
            task_label.bind("<Double-Button-1>", lambda event, t=task["id"]: self.edit_task(t))

            if task["completed"]:
                task_label.configure(text_color="gray")

            # Edit button
            edit_btn = ctk.CTkButton(
                task_frame,
                text="✏️",
                width=30,
                height=25,
                command=lambda t=task["id"]: self.edit_task(t),
                font=ctk.CTkFont(size=12),
            )
            edit_btn.pack(side="right", padx=2)

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
