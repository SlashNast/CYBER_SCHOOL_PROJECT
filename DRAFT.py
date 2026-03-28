from Users_db import add_user
from Users_db import find_user

main_gui = None


def register_cb(data):
    global main_gui
    login = data["login"].strip()
    pw = data["password"].strip()

    if not login:
        messagebox.showerror("Ошибка", "Логин не может быть пустым")
        return

    try:
        add_user(login, pw)
        messagebox.showinfo("OK", f"User {login} added.")

        user_id = find_user(login, pw)

        SecondPageGUI(main_gui._this_wnd, main_gui.get_login(), user_id)
    except Exception as e:
        messagebox.showerror("Ошибка добавления", str(e))


def signin_cb(data):
    global main_gui
    login = data["login"].strip()
    pw = data["password"].strip()

    # здесь будет логика проверки логина/пароля — сейчас просто заглушка
    messagebox.showinfo("Sign in", f"trying enter as:  {data['login']}")
    user_id = find_user(login, pw)
    SecondPageGUI(main_gui._this_wnd, main_gui.get_login(), user_id)


main_gui = CLoginGUI(None, register_cb, signin_cb)
main_gui.run()