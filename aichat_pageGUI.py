# aichat_page.py
import tkinter as tk
from tkinter import scrolledtext
from ai_client_openAI import ask_ai, SYSTEM_PROMPT
import threading


class AIChatPage:
    def __init__(self, parent_wnd):
        self._parent_wnd = parent_wnd
        self._this_wnd = tk.Toplevel(parent_wnd) if parent_wnd else tk.Tk()
        self._this_wnd.title("AI Chat")


        self.BG = "#0b0b0f"
        self.PANEL = "#11111a"
        self.TEXT = "#e6e6eb"
        self.MUTED = "#9aa0aa"
        self.CYAN = "#22d3ee"
        self.BORDER = "#1f2233"

        self.BTN_BG = "#2a2f3a"
        self.BTN_HOVER = "#343a46"
        self.BTN_TEXT = "#ffffff"
        self.BTN_BORDER = "#ffffff"

        self._canvas = None
        self._chat_box = None
        self._entry = None
        self._btn_send = None


        self.create_ui()
        self._history = []

    def go_back(self):
        self._this_wnd.destroy()


    def create_ui(self):
        # ====== window ======
        self._this_wnd.state("zoomed")
        self._this_wnd.resizable(True, True)
        self._this_wnd.configure(bg=self.BG)

        # ====== canvas ======
        self._canvas = tk.Canvas(self._this_wnd, bg=self.BG, highlightthickness=0, bd=0)
        self._canvas.pack(fill="both", expand=True)
        self._canvas.bind("<Configure>", self._draw_grid)

        # ====== main panel ======
        panel_x1, panel_y1 = 420, 90
        panel_x2, panel_y2 = 1500, 760

        # shadow
        self._canvas.create_rectangle(
            panel_x1 + 6, panel_y1 + 6, panel_x2 + 6, panel_y2 + 6,
            fill="#07070b", outline=""
        )
        # panel
        self._canvas.create_rectangle(
            panel_x1, panel_y1, panel_x2, panel_y2,
            fill=self.PANEL, outline=self.BORDER, width=2
        )
        # neon top line
        self._canvas.create_line(panel_x1, panel_y1, panel_x2, panel_y1, fill=self.CYAN, width=3)

        # ====== title ======
        self._canvas.create_text(
            (panel_x1 + panel_x2) // 2, panel_y1 + 40,
            text="AI CHAT",
            font=("Calibri", 26, "bold"),
            fill=self.TEXT
        )
        self._canvas.create_text(
            (panel_x1 + panel_x2) // 2, panel_y1 + 70,
            text="ask anything • get instant help",
            font=("Calibri", 14),
            fill=self.MUTED
        )

        # ====== chat area (scrolled text) ======
        chat_x = panel_x1 + 60
        chat_y = panel_y1 + 110
        chat_w = (panel_x2 - panel_x1) - 120
        chat_h = 470

        self._chat_box = scrolledtext.ScrolledText(
            self._this_wnd,
            wrap="word",
            font=("Calibri", 13),
            fg=self.TEXT,
            bg="#0f1017",
            insertbackground=self.CYAN,
            bd=1,
            relief="solid",
            highlightthickness=1,
            highlightbackground=self.BORDER,
            highlightcolor=self.CYAN
        )
        self._chat_box.place(x=chat_x, y=chat_y, width=chat_w, height=chat_h)
        self._chat_box.configure(state="disabled")

        # ====== input row ======
        input_y = chat_y + chat_h + 22
        entry_w = chat_w - 170

        self._entry = tk.Entry(
            self._this_wnd,
            font=("Calibri", 14),
            fg=self.TEXT,
            bg="#0f1017",
            insertbackground=self.CYAN,
            bd=1,
            relief="solid",
            highlightthickness=1,
            highlightbackground=self.BORDER,
            highlightcolor=self.CYAN
        )
        self._entry.place(x=chat_x, y=input_y, width=entry_w, height=46)
        self._entry.bind("<Return>", lambda e: self._on_send())

        self._btn_send = tk.Button(
            self._this_wnd,
            text="SEND",
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
            command=self._on_send,
            cursor="hand2"
        )
        self._btn_send.place(x=chat_x + entry_w + 18, y=input_y, width=152, height=46)
        self._btn_send.bind("<Enter>", lambda e: e.widget.config(bg=self.BTN_HOVER))
        self._btn_send.bind("<Leave>", lambda e: e.widget.config(bg=self.BTN_BG))

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

        # ====== footer ======
        self._canvas.create_text(
            (panel_x1 + panel_x2) // 2, panel_y2 - 26,
            text="tip: press Enter to send • keep questions short and specific",
            font=("Calibri", 11),
            fill="#7e8593"
        )

        # greeting
        self._append("AI", "Hi! Write your question below and press SEND 🙂")

    def _append(self, who: str, msg: str):
        self._chat_box.configure(state="normal")
        self._chat_box.insert("end", f"{who}: {msg}\n\n")
        self._chat_box.see("end")
        self._chat_box.configure(state="disabled")



    def _on_send(self):
        text = self._entry.get().strip()
        if not text:
            return
        self._entry.delete(0, "end")

        # user message
        self._append("YOU", text)

        self._history.append({"role": "user", "content": text})
        self._append("AI", "Thinking...")
        threading.Thread(target=self._ask_in_background, daemon=True).start()

    def _ask_in_background(self):
        try:
            answer = ask_ai(self._history)
            print(answer)
        except Exception as e:
            answer = f"Ошибка: {e}"

        def apply():
            self._append("AI", answer)
            self._history.append({"role": "assistant", "content": answer})

        self._this_wnd.after(0, apply)





    def _draw_grid(self, event=None):
        if self._canvas is None:
            return
        self._canvas.delete("grid")
        w, h = self._canvas.winfo_width(), self._canvas.winfo_height()
        step = 45
        for x in range(0, w, step):
            self._canvas.create_line(x, 0, x, h, fill="#2D3458", tags="grid")
        for y in range(0, h, step):
            self._canvas.create_line(0, y, w, y, fill="#2D3458", tags="grid")
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
    gui = AIChatPage(None)
    gui.run()
