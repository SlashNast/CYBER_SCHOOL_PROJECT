#MathVideos.py


import tkinter as tk
import webbrowser
from tkinter import messagebox

from math_bagrut_videos import videos_2025
import Users_db


class MathVideos:
    def __init__(self, parent_wnd, user_id):
        self._parent_wnd = parent_wnd
        self.user_id = user_id
        self._this_wnd = tk.Toplevel(parent_wnd) if parent_wnd else tk.Tk()

        self._this_wnd.title("Choose video solution")

        self._canvas = None
        self._sub_buttons = []

        # список видео из конфигурации
        self.VIDEOS = videos_2025.VIDEOS_5_POINTS_571_SUMMER_MOEDALEF_2025

        self.create_ui()

    # ================= Logic =================

    def on_choose(self, url: str):
        if not url:
            messagebox.showerror("Error", "Video link not found",  parent=self._this_wnd)
            return

        webbrowser.open(url)

    def on_save(self, material_id: int, title: str):

        ok = Users_db.add_to_favorites(self.user_id, material_id )
        if ok:
            messagebox.showinfo("SAVE", f"Saved:\n{title}",  parent=self._this_wnd)
        else:
            messagebox.showerror("SAVE", f"This material is already in favorites",  parent=self._this_wnd)

    def go_back(self):
        self._this_wnd.destroy()



    # ================= UI =================

    def create_ui(self):

        # ====== Window ======
        self._this_wnd.state("zoomed")
        self._this_wnd.resizable(True, True)
        self._this_wnd.configure(bg="#0b0b0f")

        # ====== Cyberpunk palette ======
        self.BG = "#0b0b0f"
        self.PANEL = "#11111a"
        self.TEXT = "#e6e6eb"
        self.MUTED = "#9aa0aa"
        self.CYAN = "#22d3ee"
        self.PURPLE = "#a855f7"
        self.BORDER = "#1f2233"

        self.BTN_BG = "#2a2f3a"
        self.BTN_HOVER = "#343a46"
        self.BTN_TEXT = "#ffffff"
        self.BTN_BORDER = "#ffffff"

        # ====== Canvas ======
        self._canvas = tk.Canvas(
            self._this_wnd,
            bg=self.BG,
            highlightthickness=0,
            bd=0
        )
        self._canvas.pack(fill="both", expand=True)
        self._canvas.bind("<Configure>", self._draw_grid)

        self.panel_x1, self.panel_y1 = 420, 100
        self.panel_x2, self.panel_y2 = 1580, 620

        # shadow
        self._canvas.create_rectangle(
            self.panel_x1 + 6, self.panel_y1 + 6,
            self.panel_x2 + 6, self.panel_y2 + 6,
            fill="#07070b", outline=""
        )

        # panel
        self._canvas.create_rectangle(
            self.panel_x1, self.panel_y1,
            self.panel_x2, self.panel_y2,
            fill=self.PANEL, outline=self.BORDER, width=2
        )

        # neon line
        self._canvas.create_line(
            self.panel_x1, self.panel_y1,
            self.panel_x2, self.panel_y1,
            fill=self.CYAN, width=3
        )

        # ====== Title ======
        self._canvas.create_text(
            (self.panel_x1 + self.panel_x2) // 2,
            self.panel_y1 + 40,
            text="VIDEO SOLUTIONS",
            font=("Calibri", 26, "bold"),
            fill=self.TEXT
        )

        self._canvas.create_text(
            (self.panel_x1 + self.panel_x2) // 2,
            self.panel_y1 + 70,
            text="choose a task",
            font=("Calibri", 14),
            fill=self.MUTED
        )

        # ===== Scroll area =====

        self.scroll_canvas = tk.Canvas(
            self._canvas,
            bg=self.PANEL,
            highlightthickness=0,
            bd=0
        )

        self.scrollbar = tk.Scrollbar(
            self._this_wnd,
            orient="vertical",
            command=self.scroll_canvas.yview
        )

        self.scroll_canvas.configure(yscrollcommand=self.scrollbar.set)

        list_x1 = self.panel_x1 + 40
        list_y1 = self.panel_y1 + 110
        list_x2 = self.panel_x2 - 40
        list_y2 = self.panel_y2 - 60

        list_w = list_x2 - list_x1
        list_h = list_y2 - list_y1

        self.scroll_canvas.place(x=list_x1, y=list_y1, width=list_w, height=list_h)
        self.scrollbar.place(x=list_x2 + 8, y=list_y1, height=list_h)

        self.list_frame = tk.Frame(self.scroll_canvas, bg=self.PANEL)

        self.list_window_id = self.scroll_canvas.create_window(
            (0, 0),
            window=self.list_frame,
            anchor="nw"
        )

        self.list_frame.bind("<Configure>", self._on_list_frame_configure)
        self.scroll_canvas.bind("<Configure>", self._on_scroll_canvas_configure)

        self.scroll_canvas.bind_all("<MouseWheel>", self._on_mousewheel)





        # ===== Buttons =====

        self.list_frame.grid_columnconfigure(0, weight=1)
        self.list_frame.grid_columnconfigure(1, weight=0)

        for row, (material_id, title, material_type, path_or_link) in enumerate(self.VIDEOS):

            big_btn = self._make_list_button(title, lambda u=path_or_link: self.on_choose(u))

            big_btn.grid(
                row=row,
                column=0,
                padx=(10, 8),
                pady=6
            )
            save_btn = self._make_list_saved("SAVE", lambda m_id=material_id, t=title, u=path_or_link: self.on_save(m_id, t))

            save_btn.grid(
                row=row,
                column=1,
                padx=(0, 10),
                pady=6
            )

        # footer
        self._canvas.create_text(
            (self.panel_x1 + self.panel_x2) // 2,
            self.panel_y2 - 28,
            text="tip: pick a task → watch solution",
            font=("Calibri", 11),
            fill="#7e8593"
        )

        self._btn_back = tk.Button(
            self._canvas,
            text="BACK",
            font=("Calibri", 12, "bold"),
            fg=self.BTN_TEXT,
            bg=self.BTN_BG,
            activeforeground=self.BTN_TEXT,
            activebackground=self.BTN_HOVER,
            bd=1,
            relief="solid",
            highlightthickness=1,
            highlightbackground=self.BTN_BORDER,
            highlightcolor=self.BTN_BORDER,
            command=self.go_back,
            cursor="hand2"
        )
        self._btn_back.place(x=20, y=20, width=100, height=40)

        self._btn_back.bind("<Enter>", lambda e: e.widget.config(bg=self.BTN_HOVER))
        self._btn_back.bind("<Leave>", lambda e: e.widget.config(bg=self.BTN_BG))

    # ================= Buttons =================

    def _make_list_button(self, text, command):
        btn = tk.Button(
            self.list_frame,
            text=text,
            font=("Calibri", 14, "bold"),
            fg=self.BTN_TEXT,
            bg=self.BTN_BG,
            activeforeground=self.BTN_TEXT,
            activebackground=self.BTN_HOVER,
            bd=1,
            relief="solid",
            highlightthickness=1,
            highlightbackground=self.BTN_BORDER,
            highlightcolor=self.BTN_BORDER,
            command=command,
            cursor="hand2",
            anchor="w",
            padx=12,
            width = 55
        )

        btn.bind("<Enter>", lambda e: e.widget.config(bg=self.BTN_HOVER))
        btn.bind("<Leave>", lambda e: e.widget.config(bg=self.BTN_BG))

        return btn


    def _make_list_saved(self, text, command):
        btn = tk.Button(
            self.list_frame,
            text=text,
            font=("Calibri", 14, "bold"),
            fg=self.BTN_TEXT,
            bg=self.BTN_BG,
            activeforeground=self.BTN_TEXT,
            activebackground=self.BTN_HOVER,
            bd=1,
            relief="solid",
            highlightthickness=1,
            highlightbackground=self.BTN_BORDER,
            highlightcolor=self.BTN_BORDER,
            command=command,
            cursor="hand2",
            width=8
        )

        btn.bind("<Enter>", lambda e: e.widget.config(bg=self.BTN_HOVER))
        btn.bind("<Leave>", lambda e: e.widget.config(bg=self.BTN_BG))

        return btn





    # ================= Scroll =================

    def _on_list_frame_configure(self, event):
        self.scroll_canvas.configure(
            scrollregion=self.scroll_canvas.bbox("all")
        )

    def _on_scroll_canvas_configure(self, event):
        self.scroll_canvas.itemconfig(
            self.list_window_id,
            width=event.width
        )

    def _on_mousewheel(self, event):
        self.scroll_canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    # ================= Grid =================

    def _draw_grid(self, event=None):
        if self._canvas is None:
            return

        self._canvas.delete("grid")

        width = self._canvas.winfo_width()
        height = self._canvas.winfo_height()

        step = 45

        for x in range(0, width, step):
            self._canvas.create_line(
                x, 0, x, height,
                fill="#2D3458",
                tags="grid"
            )

        for y in range(0, height, step):
            self._canvas.create_line(
                0, y, width, y,
                fill="#2D3458",
                tags="grid"
            )

        self._canvas.tag_lower("grid")

    # ================= Window helpers =================

    def show_modal(self):
        self._this_wnd.grab_set()

    def run(self):
        if self._parent_wnd is None:
            self._this_wnd.mainloop()


if __name__ == "__main__":
    from Users_db import add_to_favorites

    def add_saved(data1, data2):
        user_id =  data1["user_id"].strip()
        material = data2["material"].strip()

        try:
            add_to_favorites(user_id, material)
            messagebox.showinfo("OK", f"Your {material} added.")

        except Exception as e:
            messagebox.showerror("Ошибка добавления", str(e))


    gui = MathVideos(None,1)
    gui.run()