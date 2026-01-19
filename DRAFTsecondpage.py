import tkinter as tk
from tkinter import *
from tkinter import messagebox

BTN_IMAGE = "./Images/GUI - btn login.png"
BG_IMAGE = "./Images/booksBG2.png"
FONT = "Calibri"
FONT_BUTTON = (FONT, 14)


class SecondPageGUI:

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


        self._canvas.create_text(
            570, 170,  # координаты X и Y
            text="pls choose your learning programm",  # сам текст
            font=("Calibri", 20, "bold"),  # шрифт и размер
            fill="white",  # цвет текста
            #anchor="nw"  # "nw" = привязка к левому верхнему углу
        )

        self._btn_register = tk.Button(
            self._canvas, text="school-stuff help", font=FONT_BUTTON, fg="#4f4b4b",
            compound="center", bd=0
        )
        self._btn_register.place(x=530, y=250)


        self._btn_signin = tk.Button(
            self._canvas, text="Self-education", font=FONT_BUTTON, fg="#4f4b4b",
            compound="center", bd=0
        )
        self._btn_signin.place(x=730, y=250)


        self._btn_register2 = tk.Button(
            self._canvas, text="preparing for bagrut", font=FONT_BUTTON, fg="#4f4b4b",
            compound="center",  bd=0
        )
        self._btn_register2.place(x=300, y=250)



    def run(self):
        self._this_wnd.mainloop()

if __name__ == "__main__":
    # временные функции-заглушки для кнопок
    def on_register():
        print("REGISTER clicked")

    def on_signin():
        print("SIGNIN clicked")

    # создаём окно логина
    gui = SecondPageGUI(None, on_register, on_signin)

    # запускаем главный цикл Tkinter
    tk.mainloop()
