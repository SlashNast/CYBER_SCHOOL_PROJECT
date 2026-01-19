# video_grid_page.py
import tkinter as tk
import webbrowser


class VideoGridPage:
    def __init__(self, parent_wnd, window_title: str, title: str, subtitle: str, videos: list[tuple[str, str]]):
        self._parent_wnd = parent_wnd
        self._this_wnd = tk.Toplevel(parent_wnd) if parent_wnd else tk.Tk()

        self._this_wnd.title(window_title)
        self._title = title
        self._subtitle = subtitle
        self._videos = videos

        self._canvas = None
        self._buttons = []

    def create_ui(self):
        # ====== Window ======
        self._this_wnd.state("zoomed")
        self._this_wnd.resizable(True, True)
        self._this_wnd.configure(bg="#0b0b0f")

        # ====== Palette ======
        BG = "#0b0b0f"
        PANEL = "#11111a"
        TEXT = "#e6e6eb"
        MUTED = "#9aa0aa"
        CYAN = "#22d3ee"
        BORDER = "#1f2233"

        BTN_BG = "#2a2f3a"
        BTN_HOVER = "#343a46"
        BTN_TEXT = "#ffffff"
        BTN_BORDER = "#ffffff"

        # ====== Canvas ======
        self._canvas = tk.Canvas(self._this_wnd, bg=BG, highlightthickness=0, bd=0)
        self._canvas.pack(fill="both", expand=True)
        self._canvas.bind("<Configure>", self._draw_grid)

        # ====== Main panel ======
        panel_x1, panel_y1 = 420, 110
        panel_x2, panel_y2 = 1500, 620

        self._canvas.create_rectangle(panel_x1 + 6, panel_y1 + 6, panel_x2 + 6, panel_y2 + 6, fill="#07070b", outline="")
        self._canvas.create_rectangle(panel_x1, panel_y1, panel_x2, panel_y2, fill=PANEL, outline=BORDER, width=2)
        self._canvas.create_line(panel_x1, panel_y1, panel_x2, panel_y1, fill=CYAN, width=3)

        # ====== Title ======
        self._canvas.create_text(
            (panel_x1 + panel_x2) // 2, panel_y1 + 45,
            text="BAGRUT — VIDEO SOLUTIONS",
            font=("Calibri", 26, "bold"),
            fill=TEXT
        )
        self._canvas.create_text(
            (panel_x1 + panel_x2) // 2, panel_y1 + 75,
            text="choose a task to open YouTube",
            font=("Calibri", 14),
            fill=MUTED
        )

        # ====== Subtitle ======
        self._canvas.create_text(
            panel_x1 + 330, panel_y1 + 135,
            text=self._title,
            font=("Calibri", 15, "bold"),
            fill=TEXT,
            anchor="w"
        )
        self._canvas.create_text(
            panel_x1 + 330, panel_y1 + 160,
            text=self._subtitle,
            font=("Calibri", 12),
            fill=MUTED,
            anchor="w"
        )

        # ====== Buttons ======
        start_x = panel_x1 + 70
        start_y = panel_y1 + 200
        btn_w, btn_h = 190, 44
        gap_x, gap_y = 26, 18

        col1_x = start_x
        col2_x = start_x + btn_w + gap_x

        def make_open(url):
            return lambda: webbrowser.open(url)

        for i, (btn_title, url) in enumerate(self._videos):
            row = i % 4
            col = i // 4  # 0 или 1

            x = col1_x if col == 0 else col2_x
            y = start_y + row * (btn_h + gap_y)

            btn = tk.Button(
                self._canvas,
                text=btn_title,
                font=("Calibri", 14, "bold"),
                fg=BTN_TEXT,
                bg=BTN_BG,
                activeforeground=BTN_TEXT,
                activebackground=BTN_HOVER,
                bd=1,
                relief="solid",
                highlightthickness=1,
                highlightbackground=BTN_BORDER,
                highlightcolor=BTN_BORDER,
                command=make_open(url),
                cursor="hand2"
            )
            btn.place(x=x + 280, y=y, width=btn_w, height=btn_h)
            self._buttons.append(btn)

        # hover
        def on_enter(e): e.widget.config(bg=BTN_HOVER)
        def on_leave(e): e.widget.config(bg=BTN_BG)

        for b in self._buttons:
            b.bind("<Enter>", on_enter)
            b.bind("<Leave>", on_leave)

        # ====== Footer ======
        self._canvas.create_text(
            (panel_x1 + panel_x2) // 2, panel_y2 - 30,
            text="save links • share with classmates • practice daily",
            font=("Calibri", 11),
            fill="#7e8593"
        )

    def _draw_grid(self, event=None):
        if self._canvas is None:
            return

        self._canvas.delete("grid")
        width = self._canvas.winfo_width()
        height = self._canvas.winfo_height()
        step = 45

        for x in range(0, width, step):
            self._canvas.create_line(x, 0, x, height, fill="#2D3458", tags="grid")
        for y in range(0, height, step):
            self._canvas.create_line(0, y, width, y, fill="#2D3458", tags="grid")

        self._canvas.tag_lower("grid")

    def run(self):
        if self._parent_wnd is None:
            self._this_wnd.mainloop()
        else:
            self._this_wnd.deiconify()

    def show_modal(self):
        self._this_wnd.transient(self._parent_wnd)
        self._this_wnd.grab_set()



if __name__ == "__main__":
    gui = VideoGridPage(None)
    gui.create_ui()
    gui.run()
