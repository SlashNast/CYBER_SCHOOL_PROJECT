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
        # Load bg image
        self._img_bg = PhotoImage(file=BG_IMAGE)
        img_width = self._img_bg.width()
        img_height = self._img_bg.height()

        # Set size of the application window = image size
        self._this_wnd.geometry(f'{img_width}x{img_height}')
        self._this_wnd.resizable(False, False)

        # Create a canvas to cover the entire window
        self._canvas = tk.Canvas(self._this_wnd, width=img_width, height=img_height, highlightthickness=0, bd=0)
        self._canvas.pack(fill='both', expand=True)
        self._canvas.create_image(0, 0, anchor="nw", image=self._img_bg)

        # Add labels (text on canvas)
        self._canvas.create_text(30, 40, text='Login:', font=FONT_BUTTON, fill='#000000', anchor='w')
        self._canvas.create_text(30, 120, text='Password:', font=FONT_BUTTON, fill='#000000', anchor='w')

        # Load button image
        self._img_btn = PhotoImage(file=BTN_IMAGE)

        # Button "Register"
        self._btn_register = tk.Button(
            self._canvas, text="Register", font=FONT_BUTTON, fg="#c0c0c0",
            compound="center", image=self._img_btn, bd=0, command=self.on_click_register
        )
        self._btn_register.place(x=530, y=450)

        # Button "SignIn"
        self._btn_signin = tk.Button(
            self._canvas, text="SignIn", font=FONT_BUTTON, fg="#c0c0c0",
            compound="center", image=self._img_btn, bd=0, command=self.on_click_signin
        )
        self._btn_signin.place(x=530, y=500)

        # Create Entry boxes (без лишних пробелов)
        self._entry_login = tk.Entry(self._canvas, font=('Calibri', 16), fg='#202020')
        self._entry_login.place(x=450, y=200, width=260)

        self._entry_pw = tk.Entry(self._canvas, font=('Calibri', 16), fg='#202020', show='*')
        self._entry_pw.place(x=450, y=350, width=260)

        self._canvas.create_text(
            570, 170,  # координаты X и Y
            text="pls enter login",  # сам текст
            font=("Calibri", 20, "bold"),  # шрифт и размер
            fill="white",  # цвет текста
            #anchor="nw"  # "nw" = привязка к левому верхнему углу
        )

        self._canvas.create_text(
            570, 320,  # координаты X и Y
            text="pls enter password",  # сам текст
            font=("Calibri", 20, "bold"),  # шрифт и размер
            fill="white",  # цвет текста
            # anchor="nw"  # "nw" = привязка к левому верхнему углу
        )

    def run(self):
        self._this_wnd.mainloop()

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

    def register_cb(data):
        login = data["login"].strip()
        pw = data["password"].strip()

        if not login:
            messagebox.showerror("Ошибка", "Логин не может быть пустым")
            return

        try:
            # ВАЖНО: add_user принимает ТОЛЬКО 1 аргумент — login
            add_user(login)
            messagebox.showinfo("OK", f"User {login} added.")
        except Exception as e:
            messagebox.showerror("Ошибка добавления", str(e))

    def signin_cb(data):
        # здесь будет логика проверки логина/пароля — сейчас просто заглушка
        messagebox.showinfo("Sign in", f"trying enter as:  {data['login']}")

    wnd = CLoginGUI(None, register_cb, signin_cb)
    wnd.run()