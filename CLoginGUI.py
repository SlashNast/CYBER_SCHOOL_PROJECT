from secondpagec import SecondPageGUI


import tkinter as tk
from tkinter import *
from tkinter import messagebox

BTN_IMAGE = "./Images/GUI - btn login.png"
BG_IMAGE = "./Images/booksBG2.png"
FONT = "Calibri"
FONT_BUTTON = (FONT, 14)


class CLoginGUI:

    def __init__(self, parent_wnd, callback_register, callback_signin):
        # set windows hierarchy
        self._parent_wnd = parent_wnd
        self._this_wnd = tk.Toplevel(parent_wnd) if parent_wnd else tk.Tk()
        self._this_wnd.title("Login")

        self._canvas = None
        self._img_bg = None
        self._img_btn = None

        self._entry_login = None
        self._entry_pw = None

        self._btn_register = None
        self._btn_signin = None

        # data for the registration
        self._login = ''
        self._pw = ''
        self.callback_register = callback_register
        self.callback_signin = callback_signin

        self.create_ui()

    def get_login(self) -> str:
        return self._login

    def get_pw(self) -> str:
        return self._pw

    def create_ui(self):
        # ====== Window size ======
        #WIDTH = 900
        #HEIGHT = 600
        #self._this_wnd.geometry(f"{WIDTH}x{HEIGHT}")

        self._this_wnd.state("zoomed")
        self._this_wnd.resizable(True, True)
        self._this_wnd.configure(bg="#0b0b0f")  # фон всего окна

        # ====== Cyberpunk palette (не режет глаза) ======
        BG = "#0b0b0f"  # почти чёрный (дорогой)
        PANEL = "#11111a"  # чуть светлее для панелей
        TEXT = "#e6e6eb"  # мягкий белый
        MUTED = "#9aa0aa"  # серо-голубой
        CYAN = "#22d3ee"  # акцент 1 (неон-циан)
        PURPLE = "#a855f7"  # акцент 2 (фиолетовый)
        BORDER = "#1f2233"  # тонкая рамка

        # ====== Canvas ======
        self._canvas = tk.Canvas(
            self._this_wnd,
            bg=BG,
            highlightthickness=0,
            bd=0
        )
        self._canvas.pack(fill="both", expand=True)

        self._canvas.bind("<Configure>", self._draw_grid)


        # лёгкая сетка тонкими линиями


        # ====== Main panel (карточка по центру) ======
        panel_x1, panel_y1 = 520, 110
        panel_x2, panel_y2 = 1480, 520

        # тень
        self._canvas.create_rectangle(panel_x1 + 6, panel_y1 + 6, panel_x2 + 6, panel_y2 + 6,
                                      fill="#07070b", outline="")
        # панель
        self._canvas.create_rectangle(panel_x1, panel_y1, panel_x2, panel_y2,
                                      fill=PANEL, outline=BORDER, width=2)

        # верхняя «неоновая» линия (мягкая)
        self._canvas.create_line(panel_x1, panel_y1, panel_x2, panel_y1, fill=CYAN, width=3)

        # ====== Title ======
        self._canvas.create_text(
            (panel_x1 + panel_x2) // 2, panel_y1 + 35,
            text="ONLINE LIBRARY",
            font=("Calibri", 26, "bold"),
            fill=TEXT
        )
        self._canvas.create_text(
            (panel_x1 + panel_x2) // 2, panel_y1 + 70,
            text="study • practice • progress",
            font=("Calibri", 14),
            fill=MUTED
        )

        # ====== Labels ======
        self._canvas.create_text(panel_x1 + 55, panel_y1 + 120,
                                 text="LOGIN",
                                 font=("Calibri", 14, "bold"),
                                 fill=CYAN,
                                 anchor="w")

        self._canvas.create_text(panel_x1 + 55, panel_y1 + 235,
                                 text="PASSWORD",
                                 font=("Calibri", 14, "bold"),
                                 fill=PURPLE,
                                 anchor="w")

        # ====== Entry "frames" (делаем поля красивыми через рамку на canvas) ======
        # Координаты полей

        entry_w = 360
        entry_h = 40

        # Рамки полей (как UI-блоки)
        self._canvas.create_rectangle(panel_x1 + 55, panel_y1 + 145, panel_x1 + 55 + entry_w, panel_y1 + 145 + entry_h,
                                      outline=CYAN, width=2)
        self._canvas.create_rectangle(panel_x1 + 55, panel_y1 + 260, panel_x1 + 55+ entry_w, panel_y1 + 260 + entry_h,
                                      outline=PURPLE, width=2)

        # Hint texts (мягкий, не слепит)
        # self._canvas.create_text(panel_x1 + 55, panel_y1 + 125,
        #                          text="enter your username",
        #                          font=("Calibri", 12),
        #                          fill=MUTED,
        #                          anchor="w")
        # self._canvas.create_text(panel_x1 + 55, panel_y1 + 240,
        #                          text="enter your password",
        #                          font=("Calibri", 12),
        #                          fill=MUTED,
        #                          anchor="w")

        # ====== Entry widgets ======
        # Важно: фон делаем темным, текст светлым
        self._entry_login = tk.Entry(
            self._canvas,
            font=("Calibri", 16),
            fg=TEXT,
            bg="#0e0f17",
            insertbackground=TEXT,  # цвет курсора
            bd=0,
            highlightthickness=0
        )
        self._entry_login.place(x=panel_x1 + 65, y=panel_y1 + 155, width=entry_w - 20, height=entry_h - 14)


        self._entry_pw = tk.Entry(
            self._canvas,
            font=("Calibri", 16),
            fg=TEXT,
            bg="#0e0f17",
            insertbackground=TEXT,
            bd=0,
            highlightthickness=0,
            show="*"
        )
        self._entry_pw.place(x=panel_x1 + 65, y=panel_y1 + 270, width=entry_w - 20, height=entry_h - 14)

        # ====== Buttons ======
        # Можно оставить твою картинку-кнопку, но тогда текст должен быть светлым.


        # Register
        BTN_BG = "#2a2f3a"
        BTN_HOVER = "#343a46"
        BTN_TEXT = "#ffffff"
        BTN_BORDER = "#ffffff"

        # REGISTER
        self._btn_register = tk.Button(
            self._canvas,
            text="REGISTER",
            font=("Calibri", 14, "bold"),
            fg=BTN_TEXT,
            bg=BTN_BG,
            activeforeground=BTN_TEXT,
            activebackground=BTN_HOVER,
            bd=1,  # тонкая рамка
            relief="solid",  # чёткая рамка
            highlightthickness=1,
            highlightbackground=BTN_BORDER,
            highlightcolor=BTN_BORDER,
            command=self.on_click_register
        )
        self._btn_register.place(x=panel_x1 + 650, y=panel_y2 - 220, width=160, height=42)

        # SIGN IN
        self._btn_signin = tk.Button(
            self._canvas,
            text="SIGN IN",
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
            command=self.on_click_signin
        )
        self._btn_signin.place(x=panel_x1 + 650, y=panel_y2 - 290, width=160, height=42)

        # ====== Small footer ======
        self._canvas.create_text(
            (panel_x1 + panel_x2) // 2, panel_y2 - 25,
            text="tip: use strong password • keep your account safe",
            font=("Calibri", 11),
            fill="#7e8593"
        )

    def _draw_grid(self, event=None):
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

    main_gui = None

    def register_cb(data):
        global main_gui
        login = data["login"].strip()
        pw = data["password"].strip()

        if not login:
            messagebox.showerror("Ошибка", "Логин не может быть пустым")
            return

        try:
            # ВАЖНО: add_user принимает ТОЛЬКО 1 аргумент — login
            add_user(login)
            messagebox.showinfo("OK", f"User {login} added.")
            SecondPageGUI(main_gui._this_wnd)
        except Exception as e:
            messagebox.showerror("Ошибка добавления", str(e))

    def signin_cb(data):
        global main_gui
        # здесь будет логика проверки логина/пароля — сейчас просто заглушка
        messagebox.showinfo("Sign in", f"trying enter as:  {data['login']}")
        SecondPageGUI(main_gui._this_wnd)

    main_gui = CLoginGUI(None, register_cb, signin_cb)
    main_gui.run()
