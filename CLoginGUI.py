#login page
from BmainpageGUI import SecondPageGUI


import tkinter as tk
from tkinter import *
from tkinter import messagebox

BTN_IMAGE = "./Images/GUI - btn login.png"
BG_IMAGE = "./Images/booksBG2.png"
FONT = "Calibri"
FONT_BUTTON = (FONT, 14)


class CLoginGUI:

    def __init__(self, parent_wnd, callback_register, callback_signin):

        self._parent_wnd = parent_wnd
        self._this_wnd = tk.Toplevel(parent_wnd) if parent_wnd else tk.Tk()
        self._this_wnd.title("Login")

        self._canvas = None

        self._entry_login = None
        self._entry_pw = None

        self._btn_register = None
        self._btn_signin = None

        self._login = ''
        self._pw = ''
        self._id = 0

        self.callback_register = callback_register
        self.callback_signin = callback_signin

        self.create_ui()

    def get_login(self) -> str:
        return self._login

    def get_pw(self) -> str:
        return self._pw

    def get_id(self) -> int:
        return self._id

    def create_ui(self):
        self._this_wnd.state("zoomed")
        self._this_wnd.resizable(True, True)
        self._this_wnd.configure(bg="#0b0b0f")

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
            self._this_wnd,
            bg=self.BG,
            highlightthickness=0,
            bd=0
        )
        self._canvas.pack(fill="both", expand=True)

        self._entry_login = tk.Entry(
            self._canvas,
            font=("Calibri", 16),
            fg=self.TEXT,
            bg="#0e0f17",
            insertbackground=self.TEXT,
            bd=0,
            highlightthickness=0
        )

        self._entry_pw = tk.Entry(
            self._canvas,
            font=("Calibri", 16),
            fg=self.TEXT,
            bg="#0e0f17",
            insertbackground=self.TEXT,
            bd=0,
            highlightthickness=0,
            show="*"
        )

        self._btn_register = tk.Button(
            self._canvas,
            text="REGISTER",
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
            command=self.on_click_register
        )

        self._btn_signin = tk.Button(
            self._canvas,
            text="SIGN IN",
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
            command=self.on_click_signin
        )

        self._canvas.bind("<Configure>", self._redraw_layout)
        self._this_wnd.after(50, self._redraw_layout)


    def _redraw_layout(self, event=None):
        self._canvas.delete("all")

        width = self._canvas.winfo_width()
        height = self._canvas.winfo_height()

        if width <= 1 or height <= 1:
            return

        self._draw_grid()

        panel_w = 960
        panel_h = 410

        panel_x1 = (width - panel_w) // 2
        panel_y1 = (height - panel_h) // 2
        panel_x2 = panel_x1 + panel_w
        panel_y2 = panel_y1 + panel_h

        self._canvas.create_rectangle(
            panel_x1 + 6, panel_y1 + 6,
            panel_x2 + 6, panel_y2 + 6,
            fill="#07070b", outline=""
        )

        self._canvas.create_rectangle(
            panel_x1, panel_y1, panel_x2, panel_y2,
            fill=self.PANEL, outline=self.BORDER, width=2
        )

        self._canvas.create_line(
            panel_x1, panel_y1, panel_x2, panel_y1,
            fill=self.CYAN, width=3
        )

        self._canvas.create_text(
            (panel_x1 + panel_x2) // 2, panel_y1 + 35,
            text="ONLINE LIBRARY VIRLIB",
            font=("Calibri", 26, "bold"),
            fill=self.TEXT
        )
        self._canvas.create_text(
            (panel_x1 + panel_x2) // 2, panel_y1 + 70,
            text="study • practice • progress",
            font=("Calibri", 14),
            fill=self.MUTED
        )

        self._canvas.create_text(
            panel_x1 + 55, panel_y1 + 120,
            text="LOGIN",
            font=("Calibri", 14, "bold"),
            fill=self.CYAN,
            anchor="w"
        )

        self._canvas.create_text(
            panel_x1 + 55, panel_y1 + 235,
            text="PASSWORD",
            font=("Calibri", 14, "bold"),
            fill=self.PURPLE,
            anchor="w"
        )

        entry_w = 360
        entry_h = 40

        self._canvas.create_rectangle(
            panel_x1 + 55, panel_y1 + 145,
            panel_x1 + 55 + entry_w, panel_y1 + 145 + entry_h,
            outline=self.CYAN, width=2
        )

        self._canvas.create_rectangle(
            panel_x1 + 55, panel_y1 + 260,
            panel_x1 + 55 + entry_w, panel_y1 + 260 + entry_h,
            outline=self.PURPLE, width=2
        )


        self._entry_login.place(
            x=panel_x1 + 65,
            y=panel_y1 + 155,
            width=entry_w - 20,
            height=entry_h - 14
        )

        self._entry_pw.place(
            x=panel_x1 + 65,
            y=panel_y1 + 270,
            width=entry_w - 20,
            height=entry_h - 14
        )


        self._btn_signin.place(
            x=panel_x1 + 650,
            y=panel_y2 - 290,
            width=160,
            height=42
        )

        self._btn_register.place(
            x=panel_x1 + 650,
            y=panel_y2 - 220,
            width=160,
            height=42
        )

        self._canvas.create_text(
            (panel_x1 + panel_x2) // 2, panel_y2 - 25,
            text="tip: use strong password • keep your account safe",
            font=("Calibri", 11),
            fill="#7e8593"
        )

    def _draw_grid(self, event=None):
        width = self._canvas.winfo_width()
        height = self._canvas.winfo_height()
        step = 45

        for x in range(0, width, step):
            self._canvas.create_line(x, 0, x, height, fill="#2D3458", tags="grid")

        for y in range(0, height, step):
            self._canvas.create_line(0, y, width, y, fill="#424558", tags="grid")

        self._canvas.tag_lower("grid")

    def run(self):
        self._this_wnd.grab_set()
        self._this_wnd.focus_force()

    def on_click_register(self):
        self._login = (self._entry_login.get() or "").strip()
        self._pw = (self._entry_pw.get() or "").strip()
        data = {"login": self._login, "password": self._pw}

        if not callable(self.callback_register):
            messagebox.showerror("Ошибка", "Функция регистрации не передана (callback_register=None)")
            return
        self.callback_register(data)

    def on_click_signin(self):
        self._login = (self._entry_login.get() or "").strip()
        self._pw = (self._entry_pw.get() or "").strip()
        data = {"login": self._login, "password": self._pw}

        if not callable(self.callback_signin):
            messagebox.showerror("Ошибка", "Функция входа не передана (callback_signin=None)")
            return
        self.callback_signin(data)


if __name__ == "__main__":

    from Users_db import add_user
    from Users_db import get_user_id

    main_gui = None


    def register_cb(data):

        global main_gui
        print("REGISTER_CB STARTED")
        login = data["login"].strip()
        pw = data["password"].strip()



        if not login:
            messagebox.showerror("error", "login can't be empty")
            return

        try:
            add_user(login, pw)
            messagebox.showinfo("OK", f"User {login} added.")


            SecondPageGUI(main_gui._this_wnd, main_gui.get_login())
        except Exception as e:
            messagebox.showerror("error", str(e))


    def signin_cb(data):
        global main_gui
        print("REGISTER_CB STARTED")

        messagebox.showinfo("Sign in", f"trying enter as:  {data['login']}")
        SecondPageGUI(main_gui._this_wnd, main_gui.get_login(),1)


    main_gui = CLoginGUI(None, register_cb, signin_cb)
    main_gui.run()
