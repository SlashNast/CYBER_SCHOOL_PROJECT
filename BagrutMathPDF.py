import tkinter as tk
import os
import webbrowser
from tkinter import messagebox



class Mathpdfs:
    def __init__(self, parent_wnd):
        self._parent_wnd = parent_wnd
        self._this_wnd = tk.Toplevel(parent_wnd) if parent_wnd else tk.Tk()
        self._this_wnd.title("Choose learning program")

        self._canvas = None
        self._sub_buttons = []

        self.create_ui()

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

        # размещаем scroll_canvas поверх твоего большого canvas
        self.scroll_canvas.place(x=list_x1, y=list_y1, width=list_w, height=list_h)
        self.scrollbar.place(x=list_x2 + 8, y=list_y1, height=list_h)

        # frame внутри canvas — сюда будем добавлять кнопки
        self.list_frame = tk.Frame(self.scroll_canvas, bg=self.PANEL)
        self.list_window_id = self.scroll_canvas.create_window((0, 0), window=self.list_frame, anchor="nw")

        # важно: обновлять scrollregion, когда меняется размер контента
        self.list_frame.bind("<Configure>", self._on_list_frame_configure)
        self.scroll_canvas.bind("<Configure>", self._on_scroll_canvas_configure)

        # колесо мыши (чтобы можно было листать)
        self.scroll_canvas.bind_all("<MouseWheel>", self._on_mousewheel)



        self.PDFMAT_DIR = os.path.join(self._get_project_root(), "pdfsBAGRUTMATH")
        self.PDFMAT_MAP = {
            "35472, H26" : "horef2026, שאלון,35472.pdf",
            "35371, H26" : "horef2026, שאלון-35371.pdf",
            "35372, H26" : "horef2026, שאלון-35372.pdf",
            "35381, H26" : "horef2026, שאלון-35381.pdf",
            "35382, H26" : "horef2026, שאלון-35382.pdf",
            "35481, H26" : "horef2026, שאלון-35481.pdf",
            "35482, H26" : "horef2026, .שאלון-35482.pdf",
            "35582, H26" : "horef2026, שאלון- 35582.pdf",
            "35581, H26" : "horef2026 , שאלון-35581.pdf",
            "35471, H26" : "horef 2026, שאלון-35471.pdf",
            "35571, H26" : "שאלון-35571,  horef2026 .pdf",
            "35572, H26" : "שאלון-35572, horef2026.pdf"
        }

    def _get_project_root(self):
        return os.path.dirname(os.path.abspath(__file__))

    def on_choose(self, key: str):
        filename = self.PDFMAT_MAP.get(key)
        if not filename:
            messagebox.showerror("Error", f"No PDF mapped for key: {key}")
            return
        pdf_path = os.path.join(self.PDFMAT_DIR, filename)
        self.open_pdf(pdf_path)

    def open_pdf(self, pdf_path: str):
        pdf_abs = os.path.abspath(pdf_path)

        if not os.path.exists(pdf_abs):
            messagebox.showerror("Error", f"PDF not found:\n{pdf_abs}")
            return

        webbrowser.open_new(r"file://" + pdf_abs)

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

        self.panel_x1, self.panel_y1 = 520, 110
        self.panel_x2, self.panel_y2 = 1480, 560

        # shadow
        self._canvas.create_rectangle(
            self.panel_x1 + 6, self.panel_y1 + 6, self.panel_x2 + 6, self.panel_y2 + 6,
            fill="#07070b", outline=""
        )
        # panel
        self._canvas.create_rectangle(
            self.panel_x1, self.panel_y1, self.panel_x2, self.panel_y2,
            fill=self.PANEL, outline=self.BORDER, width=2
        )
        # neon top line
        self._canvas.create_line(
            self.panel_x1, self.panel_y1, self.panel_x2, self.panel_y1,
            fill=self.CYAN, width=3
        )

        # ====== Title ======
        self._canvas.create_text(
            (self.panel_x1 + self.panel_x2) // 2, self.panel_y1 + 40,
            text="CHOOSE YOUR BAGRUT EXAM",
            font=("Calibri", 26, "bold"),
            fill=self.TEXT
        )
        self._canvas.create_text(
            (self.panel_x1 + self.panel_x2) // 2, self.panel_y1 + 70,
            text="choose your sheelon",
            font=("Calibri", 14),
            fill=self.MUTED
        )

        #button
        btn_y = self.panel_y1 + 120
        btn_w, btn_h = 240, 52
        gap = 35

        total_w = btn_w * 3 + gap * 2
        start_x = (self.panel_x1 + self.panel_x2 - total_w) // 2

        self._canvas.create_text(
            start_x+ 90, btn_y - 20,
            text="BAGRUTS OF 2026",
            font=("Calibri", 18, "bold"),
            fill=self.TEXT
        )


        # self._btn_35571H26 = self._make_button("35571", lambda: self.on_choose("35571, H26"))
        # self._btn_35571H26.place(x=start_x, y=btn_y, width=btn_w-15, height=btn_h)
        #
        # self._btn_35572H26 = self._make_button("35572", lambda: self.on_choose("35572, H26"))
        # self._btn_35572H26.place(x=start_x, y=btn_y+70, width=btn_w-15, height=btn_h)
        #
        # self._btn_35581H26 = self._make_button("35581", lambda: self.on_choose("35581, H26"))
        # self._btn_35581H26.place(x=start_x, y=btn_y + 140, width=btn_w - 15, height=btn_h)
        #
        # self._btn_35582H26 = self._make_button("35872", lambda: self.on_choose("35872, H26"))
        # self._btn_35582H26.place(x=start_x, y=btn_y + 210, width=btn_w - 15, height=btn_h)

        btn = self._make_list_button("BAGRUT PREP", lambda: self.on_choose("35472_H26"))
        btn.pack(fill="x", padx=10, pady=8)



        #text:
        self._canvas.create_text(
            (self.panel_x1 + self.panel_x2) // 2, self.panel_y2 - 28,
            text="tip: pick a program → then pick a subject",
            font=("Calibri", 11),
            fill="#7e8593"
        )

    # def _make_button(self, text, command):
    #     btn = tk.Button(
    #         self._canvas,
    #         text=text,
    #         font=("Calibri", 14, "bold"),
    #         fg=self.BTN_TEXT,
    #         bg=self.BTN_BG,
    #         activeforeground=self.BTN_TEXT,
    #         activebackground=self.BTN_HOVER,
    #         bd=1,
    #         relief="solid",
    #         highlightthickness=1,
    #         highlightbackground=self.BTN_BORDER,
    #         highlightcolor=self.BTN_BORDER,
    #         command=command,
    #         cursor="hand2",
    #         width=25
    #     )
    #     btn.bind("<Enter>", lambda e: e.widget.config(bg=self.BTN_HOVER))
    #     btn.bind("<Leave>", lambda e: e.widget.config(bg=self.BTN_BG))
    #     return btn

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
            cursor="hand2"
        )
        btn.bind("<Enter>", lambda e: e.widget.config(bg=self.BTN_HOVER))
        btn.bind("<Leave>", lambda e: e.widget.config(bg=self.BTN_BG))
        return btn

    def _on_list_frame_configure(self, event):
            # пересчитываем область прокрутки под размер содержимого
            self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all"))

    def _on_scroll_canvas_configure(self, event):
            # чтобы внутренний frame растягивался по ширине scroll_canvas
            self.scroll_canvas.itemconfig(self.list_window_id, width=event.width)

    def _on_mousewheel(self, event):
            # Windows: event.delta обычно кратен 120
            self.scroll_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        # ================= Grid =================

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

        # ================= Window helpers =================

    def show_modal(self):
        self._this_wnd.grab_set()

    def run(self):
        # запускать mainloop только если это корневое окно
        if self._parent_wnd is None:
            self._this_wnd.mainloop()

if __name__ == "__main__":
    gui = Mathpdfs(None)
    gui.run()


