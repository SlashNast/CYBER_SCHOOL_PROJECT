import tkinter as tk
from tkinter import *

from PIL.ImageFont import truetype
from mainpage import  SecondPageGUI

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

        self.create_ui()

    def create_ui(self):
        self._root.title("Client GUI")
        self._root.state("zoomed")

        self._root.resizable(True,True)

        # Create a canvas to cover the entire window
        self._canvas = tk.Canvas(self._root, bg="#0b0b0f", highlightthickness=0, bd= 0)
        self._canvas.pack(fill='both',expand=True)


        self._canvas.bind("<Configure>", self._draw_grid)

        # Add labels, the same as... add text on canvas
        self._canvas.create_text(250,80,text='Client',font=('Calibri',28),fill='#808080')
        self._canvas.create_text(50,180,text='IP:',font=FONT_BUTTON,fill='#000000',anchor='w')
        self._canvas.create_text(50,230,text='Port:',font=FONT_BUTTON,fill='#000000',anchor='w')
        self._canvas.create_text(50,280,text='Send:',font=FONT_BUTTON,fill='#000000',anchor='w')
        self._canvas.create_text(50,330,text='Received:',font=FONT_BUTTON,fill='#000000',anchor='w')

        # Load button image
        self._img_btn = PhotoImage(file=BTN_IMAGE)
        img_btn_w = self._img_btn.width()
        img_btn_h = self._img_btn.height()

        # Button "Connect"
        self._btn_connect = tk.Button(self._canvas,text="Connect",font=FONT_BUTTON,fg="#c0c0c0",compound="center",
                                      width=img_btn_w,height=img_btn_h,image=self._img_btn,bd=0,
                                      command=self.on_click_connect)
        self._btn_connect.place(x=1350, y=50)

        # Button "Disconnect"
        self._btn_disconnect = tk.Button(self._canvas,text="Disconnect",font=FONT_BUTTON,fg="#c0c0c0",compound="center",
                                         width=img_btn_w,height=img_btn_h,image=self._img_btn,bd=0,
                                         command=self.on_click_disconnect,state="disabled")
        self._btn_disconnect.place(x=1350, y=130)

        # Button "Send Data"
        self._btn_send = tk.Button(self._canvas,text="Send Request",font=FONT_BUTTON,fg="#c0c0c0",compound="center",
                                   width=img_btn_w,height=img_btn_h,image=self._img_btn,bd=0,
                                   command=self.on_click_send,state="disabled")
        self._btn_send.place(x=1350, y=210)

        # Button "Login"
        self._btn_login = tk.Button(self._canvas,text="Login",font=FONT_BUTTON,fg="#c0c0c0",compound="center",
                                    width=img_btn_w,height=img_btn_h,image=self._img_btn,bd=0,
                                    command=self.on_click_login)
        self._btn_login.place(x=1350, y=290)

        # Create Entry boxes
        self._entry_IP = tk.Entry(self._canvas,font=('Calibri',16),fg='#808080',width=15)
        self._entry_IP.insert(0,'127.0.0.1')
        self._entry_IP.place(x=200,y=168)

        self._entry_Port = tk.Entry(self._canvas,font=('Calibri',16),fg='#808080',width=15)
        self._entry_Port.insert(0,"8822")
        self._entry_Port.place(x=200,y=218)

        self._entry_Send = tk.Entry(self._canvas,font=('Calibri',16),fg='#808080',width=15)
        self._entry_Send.insert(0,"CMD")
        self._entry_Send.place(x=200,y=268)

        self._entry_Args = tk.Entry(self._canvas,font=('Calibri',16),fg='#808080',width=34)
        self._entry_Args.insert(0,"...")
        self._entry_Args.place(x=425,y=268)

        self._text_Received = tk.Text(self._canvas,font=('Calibri',16),fg='#808080',width=50, height=5)
        self._text_Received.place(x=200,y=318)

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

       # def callback_register(data: json):
           # write_to_log(f"[Client GUI] Register - Received data from Login Wnd : {data}")

        #def callback_signin(data: json):
            #write_to_log(f"[Client GUI] SignIn - Received data from Login Wnd : {data}")

       def callback_register(data: dict):
           # 1) connect если надо
           if self._client_socket is None:
               self._client_socket = self.connect()
               if not self._client_socket:
                   messagebox.showerror("Error", "Can't connect to server")
                   return

           # 2) send REG + json
           self.send_data("REG", json.dumps(data))
           resp = self.receive_data()

           # 3) показать результат
           try:
               obj = json.loads(resp)
               if obj.get("success"):
                   messagebox.showinfo("OK", obj.get("msg", "Registered"))
                   loc_wnd._this_wnd.destroy()  # закрыть окно логина
                   SecondPageGUI(self._root)

                   # открыть SecondPageGUI тут
               else:
                   messagebox.showerror("Error", obj.get("error", "Registration failed"))
           except:
               messagebox.showerror("Error", resp)



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
               if obj.get("success"):
                   messagebox.showinfo("OK", obj.get("msg", "Signed in"))
                   loc_wnd._this_wnd.destroy()  # закрыть окно логина
                   SecondPageGUI(self._root)
                   # открыть SecondPageGUI тут
               else:
                   messagebox.showerror("Error", obj.get("error", "Sign in failed"))
           except:
               messagebox.showerror("Error", resp)


       loc_wnd = CLoginGUI(self._root, callback_register, callback_signin)
       loc_wnd.run()

    def update_received_entry(self):
        message = self.receive_data()
        # self._text_Received.delete(0, tk.END)
        self._text_Received.insert(tk.END, message + "\n")


if __name__ == "__main__":
    client = CClientGUI(CLIENT_HOST,PORT)
    client.run()
