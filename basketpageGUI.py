#basketpageGUI.py

import tkinter as tk
import webbrowser
from tkinter import messagebox
import Users_db



class Basket:
    def __init__(self, parent_wnd, user_id):

        self._parent_wnd = parent_wnd
        self.user_id = user_id
        self._this_wnd = tk.Toplevel(parent_wnd) if parent_wnd else tk.Tk()
        self._this_wnd.title("Your saved books:")


        self._canvas = None
        self._sub_buttons = []
        self._btn_back = None

        self.MATERIALS = Users_db.get_user_favorite_materials(self.user_id)

        self.filtered_favorites = self.MATERIALS.copy()
        self._sub_buttons = []
        self.selected_subject = None
        self.submenu_visible = False

        self.create_ui()


    def on_choose(self, url: str):
        if not url:
            messagebox.showerror("Error", "not found")
            return

        webbrowser.open(url)

    def on_remove(self, material_id: int, title: str):
        ok = Users_db.remove_from_favorites(self.user_id, material_id)
        if ok:
            messagebox.showinfo("REMOVE", f"Removed:\n{title}",  parent=self._this_wnd)
        else:
            messagebox.showerror("REMOVE", "Could not remove material",  parent=self._this_wnd)

    def go_back(self):
        self._this_wnd.destroy()


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

        self.scroll_canvas = tk.Canvas(
            self._canvas,
            bg=self.PANEL,
            highlightthickness=0,
            bd=0
        )

        self.scrollbar = tk.Scrollbar(
            self._this_wnd,
            orient="vertical",
            command=self.scroll_canvas.yview
        )

        self.scroll_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.list_frame = tk.Frame(self.scroll_canvas, bg=self.PANEL)

        self.list_window_id = self.scroll_canvas.create_window(
            (0, 0),
            window=self.list_frame,
            anchor="nw"
        )



        self.list_frame.bind("<Configure>", self._on_list_frame_configure)
        self.scroll_canvas.bind("<Configure>", self._on_scroll_canvas_configure)
        self.scroll_canvas.bind_all("<MouseWheel>", self._on_mousewheel)



        self.list_frame.grid_columnconfigure(0, weight=1)
        self.list_frame.grid_columnconfigure(1, weight=0)



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

        self._btn_back.bind("<Enter>", lambda e: e.widget.config(bg=self.BTN_HOVER))
        self._btn_back.bind("<Leave>", lambda e: e.widget.config(bg=self.BTN_BG))



        self.filterbtn = self._make_button(
            "choose filter",
            lambda: self.toggle_submenu("filter")
        )

        self.clear_filterbtn = self._make_button(
            "X",
            lambda: self.clear_filters()
        )

        self._canvas.bind("<Configure>", self._redraw_layout)
        self._this_wnd.after(50, self._redraw_layout, None)
        self._this_wnd.after(100, self.render_favorites)



    def render_favorites(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        for row, (material_id, title, path_or_link) in enumerate(self.filtered_favorites):
            big_btn = self._make_list_button(
                title,
                lambda u=path_or_link: self.on_choose(u)
            )
            big_btn.grid(row=row, column=0, padx=(10, 8), pady=6, sticky="ew")

            remove_btn = self._make_list_saved(
                "REMOVE",
                lambda m_id=material_id, t=title, u=path_or_link: self.on_remove(m_id, t)
            )
            remove_btn.grid(
                row=row,
                column=1,
                padx=(0, 10),
                pady=6
            )



    def _redraw_layout(self, event=None):
        if self._canvas is None:
            return

        self._canvas.delete("all")

        width = self._canvas.winfo_width()
        height = self._canvas.winfo_height()

        if width <= 1 or height <= 1:
            return

        self._draw_grid()

        panel_w = 1160
        panel_h = 520

        self.panel_x1 = (width - panel_w) // 2
        self.panel_y1 = (height - panel_h) // 2
        self.panel_x2 = self.panel_x1 + panel_w
        self.panel_y2 = self.panel_y1 + panel_h

        self._canvas.create_rectangle(
            self.panel_x1 + 6, self.panel_y1 + 6,
            self.panel_x2 + 6, self.panel_y2 + 6,
            fill="#07070b", outline=""
        )

        self._canvas.create_rectangle(
            self.panel_x1, self.panel_y1,
            self.panel_x2, self.panel_y2,
            fill=self.PANEL, outline=self.BORDER, width=2
        )


        self._canvas.create_line(
            self.panel_x1, self.panel_y1,
            self.panel_x2, self.panel_y1,
            fill=self.CYAN, width=3
        )

        self._canvas.create_text(
            (self.panel_x1 + self.panel_x2) // 2,
            self.panel_y1 + 40,
            text="YOUR SAVED MATERIALS",
            font=("Calibri", 26, "bold"),
            fill=self.TEXT
        )

        self._canvas.create_text(
            (self.panel_x1 + self.panel_x2) // 2,
            self.panel_y1 + 70,
            text="choose a task",
            font=("Calibri", 14),
            fill=self.MUTED
        )

        list_x1 = self.panel_x1 + 40
        list_y1 = self.panel_y1 + 110
        list_x2 = self.panel_x2 - 40
        list_y2 = self.panel_y2 - 60

        list_w = list_x2 - list_x1
        list_h = list_y2 - list_y1

        self.scroll_canvas.place(
            x=list_x1,
            y=list_y1,
            width=list_w,
            height=list_h
        )

        self.scrollbar.place(
            x=list_x2 + 8,
            y=list_y1,
            height=list_h
        )

        self._canvas.create_text(
            (self.panel_x1 + self.panel_x2) // 2,
            self.panel_y2 - 28,
            text="tip: pick a test → check your answers",
            font=("Calibri", 11),
            fill="#7e8593"
        )

        self._btn_back.place(x=20, y=20, width=100, height=40)

        self.filterbtn.place(
            x=(self.panel_x1 + self.panel_x2) // 2 - 530,
            y=self.panel_y1 + 20
        )

        self.clear_filterbtn.place(
            x=(self.panel_x1 + self.panel_x2) // 2 - 340,
            y=self.panel_y1 + 20, width=35
        )

        self._this_wnd.update_idletasks()
        self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all"))



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
            width = 17
        )
        btn.bind("<Enter>", lambda e: e.widget.config(bg=self.BTN_HOVER))
        btn.bind("<Leave>", lambda e: e.widget.config(bg=self.BTN_BG))
        return btn


    def _make_sub_button(self, text, y, command=None, w=180, h=30):
        b = self._make_button(text, command if command else (lambda: None))
        b.place(x=(self.panel_x1 + self.panel_x2) // 2 - 450, y=y, width=w, height=h)
        self._sub_buttons.append(b)


    def _clear_sub_buttons(self):
        for b in self._sub_buttons:
            try:
                b.destroy()
            except:
                pass
        self._sub_buttons.clear()


    def show_filter_options(self):

        self._clear_sub_buttons()

        x = (self.panel_x1 + self.panel_x2) // 2 - 100
        y = (self.panel_y1 + 40)

        self._make_sub_button("BY SUBJECT", y + 30, command=lambda: self.on_choose_filters("subject"))


    def show_subject_filter_options(self):

        self._clear_sub_buttons()

        x = (self.panel_x1 + self.panel_x2) // 2 - 100
        y = (self.panel_y1 + 40)

        self._make_sub_button("math", y + 30, command=lambda: self.set_subject(1))
        self._make_sub_button("physics", y + 60, command=lambda: self.set_subject(2))
        self._make_sub_button("english", y + 90, command=lambda: self.set_subject(3))


    def apply_filters(self):
        self.filtered_favorites = []

        for material in self.MATERIALS:
            title = material[1]

            if self.selected_subject:
                if self.selected_subject == 1 and title[:2] != "35":
                    continue
                if self.selected_subject == 2 and title[:2] != "36":
                    continue
                if self.selected_subject == 3 and title[:2] != "16":
                    continue


            self.filtered_favorites.append(material)

        self.render_favorites()



    def set_subject(self, value):
        self.selected_subject= value
        self.apply_filters()

    def on_choose_filters(self, program_type: str):
        if program_type == "filter":
            self.show_filter_options()
        elif program_type == "subject":
            self.show_subject_filter_options()


    def hide_submenu(self):
        for btn in self._sub_buttons:
            btn.destroy()
        self._sub_buttons = []

    def toggle_submenu(self, program_type: str):
        if self.submenu_visible:
            self.hide_submenu()
        else:
            self.on_choose_filters(program_type)

        self.submenu_visible = not self.submenu_visible

    def clear_filters(self):
        self.selected_subject = None

        self.filtered_favorites = self.MATERIALS.copy()
        self.render_favorites()




    def _make_list_button(self, text, command):
        btn = tk.Button(
            self.list_frame,
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
            anchor="w",
            padx=12,
            width=55
        )

        btn.bind("<Enter>", lambda e: e.widget.config(bg=self.BTN_HOVER))
        btn.bind("<Leave>", lambda e: e.widget.config(bg=self.BTN_BG))

        return btn

    def _make_list_saved(self, text, command):
        btn = tk.Button(
            self.list_frame,
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
            width=8
        )

        btn.bind("<Enter>", lambda e: e.widget.config(bg=self.BTN_HOVER))
        btn.bind("<Leave>", lambda e: e.widget.config(bg=self.BTN_BG))

        return btn


    def _on_list_frame_configure(self, event):
        self.scroll_canvas.configure(
            scrollregion=self.scroll_canvas.bbox("all")
        )

    def _on_scroll_canvas_configure(self, event):
        self.scroll_canvas.itemconfig(
            self.list_window_id,
            width=event.width
        )

    def _on_mousewheel(self, event):
        self.scroll_canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )


    def _draw_grid(self, event=None):
        if self._canvas is None:
            return

        width = self._canvas.winfo_width()
        height = self._canvas.winfo_height()
        step = 45

        for x in range(0, width, step):
            self._canvas.create_line(
                x, 0, x, height,
                fill="#2D3458",
                tags="grid"
            )

        for y in range(0, height, step):
            self._canvas.create_line(
                0, y, width, y,
                fill="#2D3458",
                tags="grid"
            )

        self._canvas.tag_lower("grid")

    def show_modal(self):
        self._this_wnd.grab_set()

    def run(self):
        if self._parent_wnd is None:
            self._this_wnd.mainloop()


if __name__ == "__main__":

    gui = Basket(None, 1)
    gui.run()