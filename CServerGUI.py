#ServerGUI
import tkinter as tk
from tkinter import *
from CServerBL import *


FONT = "Calibri"
FONT_BUTTON = (FONT,16)


class CServerGUI(CServerBL):

    def __init__(self, host, port):
        super().__init__(host,port)

        # Attributes
        self._server_thread = None

        self._root = None
        self._canvas = None

        self._entry_IP = None
        self._entry_Port = None
        self._entry_Received = None
        self._entry_Send = None

        self._btn_start = None
        self._btn_stop = None

        # GUI initialization
        self.create_ui()

    def create_ui(self):

        self._root = tk.Tk()
        self._root.title("Server GUI")

        self._root.state("zoomed")
        self._root.resizable(False, False)
        self._root.configure(bg="#0b0b0f")

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


        self._canvas = tk.Canvas(
            self._root,
            bg=self.BG,
            highlightthickness=0,
            bd=0
        )


        self._canvas.pack(fill='both',expand=True)


        self._btn_start = tk.Button(
            self._canvas,
            text="Start",
            font=FONT_BUTTON,
            fg=self.BTN_TEXT,
            bg=self.BTN_BG,
            activeforeground=self.BTN_TEXT,
            activebackground=self.BTN_HOVER,
            compound="center",
            relief="solid",
            highlightthickness=1,
            highlightbackground=self.BTN_BORDER,
            highlightcolor=self.BTN_BORDER,
            bd=0,
            command=self.on_click_start)


        self._btn_stop = tk.Button(
            self._canvas,
            text="Stop",
            font=FONT_BUTTON,
            fg=self.BTN_TEXT,
            bg=self.BTN_BG,
            activebackground=self.BTN_HOVER,
            compound="center",
            relief="solid",
            highlightthickness=1,
            highlightbackground=self.BTN_BORDER,
            highlightcolor=self.BTN_BORDER,
             bd=0,
            command=self.on_click_stop,
            state="disabled")






        self._entry_IP = tk.Entry(self._canvas, font=('Calibri',16), fg='#808080')
        self._entry_IP.insert(0,'127.0.0.1')


        self._entry_Port = tk.Entry(self._canvas,font=('Calibri',16),fg='#808080')
        self._entry_Port.insert(0,"8822")


        self._entry_Send = tk.Entry(self._canvas,font=('Calibri',16),fg='#808080')
        self._entry_Send.insert(0,"text message")


        self._entry_Received = tk.Entry(self._canvas,font=('Calibri',16),fg='#808080')
        self._entry_Received.insert(0,"...")

        self._canvas.bind("<Configure>", self._redraw_layout)
        self._root.after(50, self._redraw_layout)



    def _redraw_layout(self, event=None):
        self._canvas.delete("all")

        width = self._canvas.winfo_width()
        height = self._canvas.winfo_height()

        if width <= 1 or height <= 1:
            return

        self._draw_grid()


        panel_w = 1200
        panel_h = 520

        panel_x1 = (width - panel_w) // 2
        panel_y1 = (height - panel_h) // 2
        panel_x2 = panel_x1 + panel_w
        panel_y2 = panel_y1 + panel_h

        # shadow
        self._canvas.create_rectangle(
            panel_x1 + 6, panel_y1 + 6,
            panel_x2 + 6, panel_y2 + 6,
            fill="#07070b", outline=""
        )

        # panel
        self._canvas.create_rectangle(
            panel_x1, panel_y1, panel_x2, panel_y2,
            fill=self.PANEL, outline=self.BORDER, width=2
        )

        # top neon line
        self._canvas.create_line(
            panel_x1, panel_y1, panel_x2, panel_y1,
            fill=self.CYAN, width=3
        )

        self._canvas.create_text(
            (panel_x1 + panel_x2) // 2,
            panel_y1 + 40,
            text="SERVER",
            font=("Calibri", 28, "bold"),
            fill=self.TEXT
        )

        self._canvas.create_text(
            panel_x1 + 60, panel_y1 + 110,
            text="IP:",
            font=FONT_BUTTON,
            fill=self.CYAN,
            anchor="w"
        )

        self._canvas.create_text(
            panel_x1 + 60, panel_y1 + 170,
            text="PORT:",
            font=FONT_BUTTON,
            fill=self.CYAN,
            anchor="w"
        )

        self._canvas.create_text(
            panel_x1 + 60, panel_y1 + 230,
            text="SEND:",
            font=FONT_BUTTON,
            fill=self.PURPLE,
            anchor="w"
        )

        self._canvas.create_text(
            panel_x1 + 60, panel_y1 + 300,
            text="RECEIVED:",
            font=FONT_BUTTON,
            fill=self.PURPLE,
            anchor="w"
        )

        entry_h = 32

        self._entry_IP.place(
            x=panel_x1 + 180,
            y=panel_y1 + 95,
            width=260,
            height=entry_h
        )

        self._entry_Port.place(
            x=panel_x1 + 180,
            y=panel_y1 + 155,
            width=260,
            height=entry_h
        )

        self._entry_Send.place(
            x=panel_x1 + 180,
            y=panel_y1 + 215,
            width=260,
            height=entry_h
        )

        self._entry_Received.place(
            x=panel_x1 + 180,
            y=panel_y1 + 275,
            width=260,
            height=entry_h
        )

        self._btn_start.place(
            x=panel_x1 + 780,
            y=panel_y1 + 215,
            width=160,
            height=42
        )

        self._btn_stop.place(
            x=panel_x1 + 780,
            y=panel_y1 + 275,
            width=160,
            height=42
        )


    def _draw_grid(self, event=None):
        if self._canvas is None:
            return

        width = self._canvas.winfo_width()
        height = self._canvas.winfo_height()
        step = 45

        for x in range(0, width, step):
            self._canvas.create_line(x, 0, x, height, fill="#2D3458", tags="grid")

        for y in range(0, height, step):
            self._canvas.create_line(0, y, width, y, fill="#2D3458", tags="grid")

        self._canvas.tag_lower("grid")

    def run(self):
        self._root.mainloop()

    def on_click_start(self):
        self._entry_IP.config(state="disabled")
        self._entry_Port.config(state="disabled")
        self._btn_start.config(state="disabled")
        self._btn_stop.config(state="normal")

        self._server_thread = threading.Thread(target=self.start_server)
        self._server_thread.start()

    def on_click_stop(self):
        self._entry_IP.config(state="normal")
        self._entry_Port.config(state="normal")
        self._btn_start.config(state="normal")
        self._btn_stop.config(state="disabled")

        self.stop_server()


if __name__ == "__main__":
    server = CServerGUI(SERVER_HOST, PORT)
    server.run()
