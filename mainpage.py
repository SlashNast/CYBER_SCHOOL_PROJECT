from sampleforbagrutmath import VideoGridPage
from BagrutMathPDF import Mathpdfs
from aichat_pageGUI import AIChatPage
import tkinter as tk



class SecondPageGUI:
    def __init__(self, parent_wnd, username):
        self._parent_wnd = parent_wnd
        self._this_wnd = tk.Toplevel(parent_wnd) if parent_wnd else tk.Tk()
        self.username = username
        self._this_wnd.title(f"Hi, {self.username} 👋 !! pls  Choose learning program")


        self._canvas = None
        self._math_5points_window = None
        self._AI_chat_window = None

        # чтобы под-опции не наслаивались
        self._sub_buttons = []

        self.create_ui()

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

        # ====== Main panel ======
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
            text="ONLINE LIBRARY",
            font=("Calibri", 26, "bold"),
            fill=self.TEXT
        )


        self._canvas.create_text(
            (self.panel_x1 + self.panel_x2) // 2, self.panel_y1 + 80,
            text=f"Hi!! {self.username} choose your learning program",
            font=("Calibri", 15),
            fill=self.MUTED
        )

        # ====== Main buttons (4) ======
        btn_y = self.panel_y1 + 120
        btn_w, btn_h = 240, 52
        gap = 35

        total_w = btn_w * 3 + gap * 2
        start_x = (self.panel_x1 + self.panel_x2 - total_w) // 2

        self._btn_CHATAI = self._make_button("AI chat",  command=self.open_chat_AI_page)
        self._btn_CHATAI.place(x= start_x + 2*(btn_w + gap), y=btn_y, width=btn_w, height=btn_h)

        self._btn_bagrut = self._make_button("BAGRUT PREP", lambda: self.on_choose("bagrut"))
        self._btn_bagrut.place(x=start_x, y=btn_y, width=btn_w, height=btn_h)

        self._btn_school = self._make_button("SCHOOL HELP", lambda: self.on_choose("school"))
        self._btn_school.place(x=start_x + btn_w + gap, y=btn_y, width=btn_w, height=btn_h)



        # footer
        self._canvas.create_text(
            (self.panel_x1 + self.panel_x2) // 2, self.panel_y2 - 28,
            text="tip: pick a program → then pick a subject",
            font=("Calibri", 11),
            fill="#7e8593"
        )

    def _make_button(self, text, command):
        btn = tk.Button(
            self._canvas,
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
            width = 25
        )
        btn.bind("<Enter>", lambda e: e.widget.config(bg=self.BTN_HOVER))
        btn.bind("<Leave>", lambda e: e.widget.config(bg=self.BTN_BG))
        return btn

    def _make_sub_button(self, text, x, y, command=None, w=180, h=44):
        b = self._make_button(text, command if command else (lambda: None))
        b.place(x=x, y=y, width=w, height=h)
        self._sub_buttons.append(b)

    def _clear_sub_buttons(self):
        for b in self._sub_buttons:
            try:
                b.destroy()
            except:
                pass
        self._sub_buttons.clear()

    # ================= Logic =================
    def on_choose(self, program_type: str):
        if program_type == "school":
            self.show_school_options()
        elif program_type == "bagrut":
            self.show_bagrut_options()

    def on_choose_bagrut(self, program_type: str):
        if program_type == "bagrutmath":
            self.show_bagrut_math_options()

    # ================= Submenus =================


    def show_school_options(self):
        self._clear_sub_buttons()

        base_x = (self.panel_x1 + self.panel_x2) // 2 - 90  # центр (под school)
        base_y = self.panel_y1 + 200

        self._make_sub_button("MATH", base_x, base_y)
        self._make_sub_button("HEBREW", base_x, base_y + 55)
        self._make_sub_button("C#", base_x, base_y + 110)

    def show_bagrut_options(self):
        self._clear_sub_buttons()

        base_x = self.panel_x1 + 140  # слева (под bagrut)
        base_y = self.panel_y1 + 200

        self._make_sub_button("MATH", base_x, base_y, command=lambda: self.on_choose_bagrut("bagrutmath"))
        self._make_sub_button("HEBREW", base_x, base_y + 55)
        self._make_sub_button("C#", base_x, base_y + 110)

    def show_bagrut_math_options(self):
        self._clear_sub_buttons()

        base_x = self.panel_x1 + 140
        base_y = self.panel_y1 + 200

        self._make_sub_button("BAGRUTS PDFS", base_x, base_y, command=self.bagrutpdfs)
        self._make_sub_button("VIDEO SOLUTIONS", base_x, base_y + 55)
        self._make_sub_button("idk smthng", base_x, base_y + 110)

    def bagrutpdfs(self):
        if self._math_5points_window is not None:
            try:
                self._math_5points_window._this_wnd.lift()
                return
            except:
                self._math_5points_window = None

        self._math_5points_window = Mathpdfs(self._this_wnd)
        self._math_5points_window.create_ui()


    def open_chat_AI_page(self):
        if self._AI_chat_window is not None:
            try:
                self._AI_chat_window._this_wnd.lift()
                return
            except:
                self._AI_chat_window = None

        self._AI_chat_window = AIChatPage(self._this_wnd)
        self._AI_chat_window.create_ui()





        # НЕ запускай второй mainloop для Toplevel

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
    gui = SecondPageGUI(None)
    gui.run()
