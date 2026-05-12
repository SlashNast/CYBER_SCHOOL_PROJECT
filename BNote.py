# BNote.py
import tkinter as tk
from tkinter import messagebox
import Users_db


class Note:
    def __init__(self, parent_wnd, user_id, note_id=None, on_saved=None):
        self._parent_wnd = parent_wnd
        self.user_id = user_id
        self.note_id = note_id
        self.on_saved = on_saved

        self._this_wnd = tk.Toplevel(parent_wnd) if parent_wnd else tk.Tk()

        self.create_ui()
        self.create_menu()

        if self.note_id is not None:
            self.load_note()


    def create_ui(self):
        self._this_wnd.title("Note")
        self._this_wnd.geometry("600x400")
        self._this_wnd.resizable(True, True)

        self.BG = "#0b0b0f"
        self.PURPLE = "#DE00EE"
        self.CYAN = "#22d3ee"
        self.BLUE = "#1B1BF3"
        self.LIGHT_BLACK = "#696973"

        self._this_wnd.configure(bg=self.BG)

        self.title_var = tk.StringVar()

        self.title_entry = tk.Entry(
            self._this_wnd,
            textvariable=self.title_var,
            bg="#11111a",
            fg="white",
            insertbackground="white",
            font=("Arial", 16)
        )

        self.title_entry.pack(fill="x", padx=10, pady=10)

        self.f_text = tk.Frame(self._this_wnd, bg=self.BG)
        self.f_text.pack(fill=tk.BOTH, expand=True)

        self.text_field = tk.Text(
            self.f_text,
            bg=self.BG,
            fg="white",
            pady=20,
            padx=10,
            wrap=tk.WORD,
            insertbackground=self.CYAN,
            selectbackground=self.PURPLE,
            spacing3=10,
            width=30,
            font=("Arial", 14)
        )
        self.text_field.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        self.scroll = tk.Scrollbar(
            self.f_text,
            command=self.text_field.yview
        )
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_field.config(yscrollcommand=self.scroll.set)

    def create_menu(self):
        self.main_menu = tk.Menu(self._this_wnd)

        self.file_menu = tk.Menu(
            self.main_menu,
            tearoff=0,
            bg="black",
            fg="white",
            activebackground=self.PURPLE,
            activeforeground="white"
        )

        self.file_menu.add_command(label="SAVE", command=self.save_note)
        self.file_menu.add_command(label="DELETE", command=self.delete_note)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="EXIT", command=self.close_window)

        self.main_menu.add_cascade(label="File", menu=self.file_menu)
        self._this_wnd.config(menu=self.main_menu)


    def load_note(self):
        note = Users_db.get_note_by_id(self.note_id, self.user_id)

        if note is None:
            messagebox.showerror(
                "Error",
                "Note not found",
                parent=self._this_wnd
            )

            return

        content = note[2]
        title = note [1]

        self.title_var.set(title)

        self.text_field.delete("1.0", tk.END)
        self.text_field.insert("1.0", content)

    def save_note(self):
        content = self.text_field.get("1.0", "end-1c").strip()

        if not content:
            messagebox.showwarning(
                "Empty note",
                "Note is empty",
                parent=self._this_wnd
            )
            return

        title = self.title_var.get().strip()

        if not title:
            messagebox.showwarning(
                "Empty title",
                "Please enter title",
                 parent = self._this_wnd
            )
            return

        if self.note_id is None:
            self.note_id = Users_db.add_note(
                self.user_id,
                title,
                content
            )
        else:
            Users_db.update_note(
                self.note_id,
                self.user_id,
                title,
                content
            )

        if self.on_saved:
            self.on_saved()

        messagebox.showinfo(
            "Saved",
            "Note saved successfully",
            parent=self._this_wnd
        )

    def delete_note(self):
        if self.note_id is None:
            self.text_field.delete("1.0", tk.END)
            self._this_wnd.destroy()
            return

        ok = Users_db.delete_note(self.note_id, self.user_id)

        if ok:
            if self.on_saved:
                self.on_saved()

            messagebox.showinfo(
                "Deleted",
                "Note deleted successfully",
                parent=self._this_wnd
            )

            self._this_wnd.destroy()
        else:
            messagebox.showerror(
                "Error",
                "Could not delete note",
                parent=self._this_wnd
            )

    def close_window(self):
        self._this_wnd.destroy()


    def show_modal(self):
        self._this_wnd.grab_set()

    def run(self):
        if self._parent_wnd is None:
            self._this_wnd.mainloop()