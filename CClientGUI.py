#clientgui
import tkinter as tk
from tkinter import *
from BmainpageGUI import  SecondPageGUI

from CClientBL import *
from CLoginGUI import *
import json
from tkinter import messagebox


BTN_IMAGE = "./Images/GUI - button.png"
BG_IMAGE = "./Images/GUI - BG.png"
FONT = "Calibri"
FONT_BUTTON = (FONT,16)


class CClientGUI(CClientBL):

    def __init__(self, host, port):

        super().__init__(host, port)

        self._root = tk.Tk()
        self._canvas = None
        self._img_bg = None
        self._img_btn = None

        self._entry_IP = None
        self._entry_Port = None
        self._entry_Send = None
        self._entry_Args = None
        self._text_Received = None

        self._btn_connect = None
        self._btn_disconnect = None
        self._btn_send = None
        self._btn_login = None

        self._login_wnd = None

        self.create_ui()

    def create_ui(self):
            self._root.title("Client GUI")
            self._root.state("zoomed")
            self._root.resizable(True, True)
            self._root.configure(bg="#0b0b0f")

            # ====== Palette ======
            self.BG = "#0b0b0f"
            self.PANEL = "#11111a"
            self.TEXT = "#e6e6eb"
            self.MUTED = "#9aa0aa"
            self.CYAN = "#22d3ee"
            self.PURPLE = "#a855f7"
            self.BORDER = "#1f2233"

            # ====== Canvas ======
            self._canvas = tk.Canvas(
                self._root,
                bg=self.BG,
                highlightthickness=0,
                bd=0
            )
            self._canvas.pack(fill="both", expand=True)

            # button image
            self._img_btn = PhotoImage(file=BTN_IMAGE)

            # ====== Buttons ======
            self._btn_connect = tk.Button(
                self._canvas,
                text="Connect",
                font=FONT_BUTTON,
                fg="#c0c0c0",
                compound="center",
                image=self._img_btn,
                bd=0,
                command=self.on_click_connect
            )

            self._btn_disconnect = tk.Button(
                self._canvas,
                text="Disconnect",
                font=FONT_BUTTON,
                fg="#c0c0c0",
                compound="center",
                image=self._img_btn,
                bd=0,
                command=self.on_click_disconnect,
                state="disabled"
            )

            self._btn_send = tk.Button(
                self._canvas,
                text="Send Request",
                font=FONT_BUTTON,
                fg="#c0c0c0",
                compound="center",
                image=self._img_btn,
                bd=0,
                command=self.on_click_send,
                state="disabled"
            )

            self._btn_login = tk.Button(
                self._canvas,
                text="Login",
                font=FONT_BUTTON,
                fg="#c0c0c0",
                compound="center",
                image=self._img_btn,
                bd=0,
                command=self.on_click_login
            )

            # ====== Entries ======
            self._entry_IP = tk.Entry(self._canvas, font=('Calibri', 16), fg='#808080')
            self._entry_IP.insert(0, '127.0.0.1')

            self._entry_Port = tk.Entry(self._canvas, font=('Calibri', 16), fg='#808080')
            self._entry_Port.insert(0, "8822")

            self._entry_Send = tk.Entry(self._canvas, font=('Calibri', 16), fg='#808080')
            self._entry_Send.insert(0, "CMD")

            self._entry_Args = tk.Entry(self._canvas, font=('Calibri', 16), fg='#808080')
            self._entry_Args.insert(0, "...")

            self._text_Received = tk.Text(self._canvas, font=('Calibri', 16), fg='#808080')

            self._canvas.bind("<Configure>", self._redraw_layout)
            self._root.after(50, self._redraw_layout)


    def _redraw_layout(self, event=None):
        self._canvas.delete("all")

        width = self._canvas.winfo_width()
        height = self._canvas.winfo_height()

        if width <= 1 or height <= 1:
            return

        self._draw_grid()

        # ====== Main panel ======
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

        # title
        self._canvas.create_text(
            (panel_x1 + panel_x2) // 2,
            panel_y1 + 40,
            text="CLIENT",
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

        # entry sizes
        entry_h = 32

        # entries
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

        self._entry_Args.place(
            x=panel_x1 + 470,
            y=panel_y1 + 215,
            width=340,
            height=entry_h
        )

        self._text_Received.place(
            x=panel_x1 + 180,
            y=panel_y1 + 285,
            width=630,
            height=120
        )

        # buttons
        self._btn_connect.place(
            x=panel_x2 - 290,
            y=panel_y1 + 85
        )

        self._btn_disconnect.place(
            x=panel_x2 - 290,
            y=panel_y1 + 165
        )

        self._btn_send.place(
            x=panel_x2 - 290,
            y=panel_y1 + 245
        )

        self._btn_login.place(
            x=panel_x2 - 290,
            y=panel_y1 + 325
        )


    def _draw_grid(self, event=None):
        self._canvas.delete("grid")

        width = self._canvas.winfo_width()
        height = self._canvas.winfo_height()
        step = 45

        for x in range(0, width, step):
            self._canvas.create_line(x, 0, x, height, fill="#2D3458", tags="grid")

        for y in range(0, height, step):
            self._canvas.create_line(0, y, width, y, fill="#424558", tags="grid")

    def run(self):
        self._root.mainloop()

    def on_click_connect(self):
        self._client_socket = self.connect()
        if self._client_socket:
            self._entry_IP.config(state="disabled")
            self._entry_Port.config(state="disabled")
            self._btn_connect.config(state="disabled")
            self._btn_disconnect.config(state="normal")
            self._btn_send.config(state="normal")

    def on_click_disconnect(self):
        bres = self.disconnect()
        if bres:
            self._entry_IP.config(state="normal")
            self._entry_Port.config(state="normal")
            self._btn_connect.config(state="normal")
            self._btn_disconnect.config(state="disabled")
            self._btn_send.config(state="disabled")

    def on_click_send(self):
        cmd = self._entry_Send.get()
        args = self._entry_Args.get()
        if cmd:
            self.send_data(cmd, args)
            # Use "after" to update the GUI after a short delay
            self._root.after(100,self.update_received_entry)

    loc_wnd = None

    def on_click_login(self):

        loc_wnd = None

        def callback_register(data: dict):
            if self._client_socket is None:
                self._client_socket = self.connect()
                if not self._client_socket:
                    messagebox.showerror("Error", "Can't connect to server")
                    return

            self.send_data("REG", json.dumps(data))
            resp = self.receive_data()

            try:
                obj = json.loads(resp)
            except:
                messagebox.showerror("Error", resp)
                return

            if obj.get("success"):
                messagebox.showinfo("OK", obj.get("msg", "Registered"))

                username = data.get("login", "").strip()
                user_id = obj.get("user_id")

                print("REGISTER USER_ID =", user_id)

                loc_wnd._this_wnd.destroy()
                SecondPageGUI(self._root, username, user_id)

            else:
                messagebox.showerror("Error", obj.get("error", "Registration failed"))

        def callback_signin(data: dict):

            if self._client_socket is None:
                self._client_socket = self.connect()
                if not self._client_socket:
                    messagebox.showerror("Error", "Can't connect to server")
                    return

            self.send_data("SIGNIN", json.dumps(data))
            resp = self.receive_data()

            try:
                obj = json.loads(resp)
            except:
                messagebox.showerror("Error", resp)
                return

            if obj.get("success"):
                messagebox.showinfo("OK", obj.get("msg", "Signed in"))

                username = data.get("login", "").strip()
                user_id = obj.get("user_id")

                print("REGISTER USER_ID =", user_id)

                loc_wnd._this_wnd.destroy()
                SecondPageGUI(self._root, username, user_id)

            else:
                messagebox.showerror("Error", obj.get("error", "Sign in failed"))

        loc_wnd = CLoginGUI(self._root, callback_register, callback_signin)
        loc_wnd.run()

    def update_received_entry(self):
        return
        #message = self.receive_data()
        # self._text_Received.delete(0, tk.END)
        #self._text_Received.insert(tk.END, message + "\n")



if __name__ == "__main__":
    client = CClientGUI(CLIENT_HOST,PORT)
    client.run()
