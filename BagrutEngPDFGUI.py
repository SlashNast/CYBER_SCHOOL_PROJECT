#BagrutEngPdf.py
import tkinter as tk
import os
import webbrowser
from tkinter import messagebox
import Users_db



class Engpdfs:
    def __init__(self, parent_wnd, user_id):
        self._parent_wnd = parent_wnd
        self.user_id = user_id
        self._this_wnd = tk.Toplevel(parent_wnd) if parent_wnd else tk.Tk()

        self._this_wnd.title("Choose learning program")

        self._canvas = None



        self.PDFENG_DIR = os.path.join(self._get_project_root(), "pdfsBAGRUTENG")
        self.PDFS = [
            (30, "Module A, 16381, S25", "summer2025, שאלון-16381A.pdf"),
            (31, "Module A, 16381, S25, answers", "summer2025, פתרון-16381A.pdf"),
            (32, "Module C, 16382, S25", "summer2025, שאלון-16382C.pdf"),
            (33, "Module C, 16382, S25, answers", "summer2025, פתרון-16381C.pdf"),
            (34, "Module G, 16582, S25", "summer2025, שאלון-16582G.pdf"),
            (35, "Module G, 16582, S25, answers", "summer2025, פתרון-16381G.pdf"),
            (36, "Module E, 16471, S25", "summer2025, 16471-שאלוןE.pdf"),
            (37, "Module E, 16471, S25, answers", "summer2025, פתרון-16381E.pdf"),

        ]

        self.filtered_pdfs = self.PDFS.copy()
        self._sub_buttons = []
        self._current_submenu = None
        self.submenu_visible = False
        self.selected_yahidot = None
        self.selected_grade = None

        self.create_ui()
        #self._create_scroll_area()
        #self._fill_buttons()

    def _get_project_root(self):
        return os.path.dirname(os.path.abspath(__file__))

    def on_choose(self, filename: str):
        if not filename:
            messagebox.showerror("Error", "No PDF file provided",  parent=self._this_wnd)
            return

        pdf_path = os.path.join(self.PDFENG_DIR, filename)
        self.open_pdf(pdf_path)



    def on_save(self, material_id, title):
        ok = Users_db.add_to_favorites(self.user_id, material_id)
        if ok:
            messagebox.showinfo("SAVE", f"Saved:\n{title}", parent=self._this_wnd)
        else:
            messagebox.showerror("SAVE", f"This material is already in favorites",  parent=self._this_wnd)

    def go_back(self):
        self._this_wnd.destroy()



    def open_pdf(self, pdf_path: str):
        pdf_abs = os.path.abspath(pdf_path)

        if not os.path.exists(pdf_abs):
            messagebox.showerror("Error", f"PDF not found:\n{pdf_abs}",  parent=self._this_wnd)
            return

        webbrowser.open_new(r"file://" + pdf_abs)



    def create_ui(self):
        # ====== Window ======
        self._this_wnd.state("zoomed")
        self._this_wnd.resizable(True, True)
        self._this_wnd.configure(bg="#0b0b0f")

        # ====== Cyberpunk palette ======
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

        # ====== Canvas ======
        self._canvas = tk.Canvas(
            self._this_wnd,
            bg=self.BG,
            highlightthickness=0,
            bd=0
        )
        self._canvas.pack(fill="both", expand=True)

        # ====== Scroll area ======
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

        self._canvas.bind("<Configure>", self._redraw_layout)
        self._this_wnd.after(50, self._redraw_layout, None)

        self._canvas.bind("<Configure>", self._redraw_layout)
        self._this_wnd.after(50, self._redraw_layout, None)
        self._this_wnd.after(100, self.render_pdfs)

    def render_pdfs(self):
        # очищаем экран
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        # рисуем текущий список
        for row, (material_id, title, filename) in enumerate(self.filtered_pdfs):
            big_btn = self._make_list_button(
                title,
                lambda f=filename: self.on_choose(f)
            )
            big_btn.grid(row=row, column=0, padx=(10, 8), pady=6, sticky="ew")

            save_btn = self._make_list_saved(
                "SAVE",
                lambda m_id=material_id, t=title: self.on_save(m_id, t)
            )
            save_btn.grid(row=row, column=1, padx=(0, 10), pady=6)



    def _redraw_layout(self, event=None):
        if self._canvas is None:
            return

        self._canvas.delete("all")

        width = self._canvas.winfo_width()
        height = self._canvas.winfo_height()

        if width <= 1 or height <= 1:
            return

        self._draw_grid()

        # ====== Main panel ======
        panel_w = 960
        panel_h = 450

        self.panel_x1 = (width - panel_w) // 2
        self.panel_y1 = (height - panel_h) // 2
        self.panel_x2 = self.panel_x1 + panel_w
        self.panel_y2 = self.panel_y1 + panel_h

        # shadow
        self._canvas.create_rectangle(
            self.panel_x1 + 6, self.panel_y1 + 6,
            self.panel_x2 + 6, self.panel_y2 + 6,
            fill="#07070b", outline=""
        )

        # panel
        self._canvas.create_rectangle(
            self.panel_x1, self.panel_y1,
            self.panel_x2, self.panel_y2,
            fill=self.PANEL, outline=self.BORDER, width=2
        )

        # neon line
        self._canvas.create_line(
            self.panel_x1, self.panel_y1,
            self.panel_x2, self.panel_y1,
            fill=self.CYAN, width=3
        )

        # title
        self._canvas.create_text(
            (self.panel_x1 + self.panel_x2) // 2,
            self.panel_y1 + 40,
            text="CHOOSE YOUR BAGRUT EXAM",
            font=("Calibri", 26, "bold"),
            fill=self.TEXT
        )

        self._canvas.create_text(
            (self.panel_x1 + self.panel_x2) // 2,
            self.panel_y1 + 70,
            text="choose your sheelon",
            font=("Calibri", 14),
            fill=self.MUTED
        )

        self.filterbtn = self._make_button("choose filter", lambda: self.toggle_submenu("filter"))

        self.filterbtn.place(x = (self.panel_x1 + self.panel_x2) // 2 - 450, y = self.panel_y1 + 20 )

        # list area
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

        # footer
        self._canvas.create_text(
            (self.panel_x1 + self.panel_x2) // 2,
            self.panel_y2 - 28,
            text="tip: pick a program → then pick a subject",
            font=("Calibri", 11),
            fill="#7e8593"
        )

        self._btn_back.place(x=20, y=20, width=100, height=40)

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

    def _make_sub_button(self, text, x, y, command=None, w=180, h=30):
        b = self._make_button(text, command if command else (lambda: None))
        b.place(x = (self.panel_x1 + self.panel_x2) // 2 - 450, y = y , width=w, height=h)
        self._sub_buttons.append(b)

    def _clear_sub_buttons(self):
        for b in self._sub_buttons:
            try:
                b.destroy()
            except:
                pass
        self._sub_buttons.clear()

    def show_filter_options(self):
        self._current_submenu = "bagrut"
        self._clear_sub_buttons()

        x = (self.panel_x1 + self.panel_x2) // 2 - 100
        y = (self.panel_y1 + 40)


        self._make_sub_button("BY GRADE", x, y + 30, command=lambda: self.on_choose_filters("grade"))
        self._make_sub_button("BY YEAR", x, y + 60) #command=lambda: self.on_choose_bagrut("bagrutphys"))
        self._make_sub_button("BY YAHIDOT", x, y + 90,  command=lambda: self.on_choose_filters("yahidot"))

    def show_yahidot_filter_options(self):
        self._current_submenu = "yahidot"
        self._clear_sub_buttons()

        x = (self.panel_x1 + self.panel_x2) // 2 - 100
        y = (self.panel_y1 + 40)


        self._make_sub_button("3", x, y + 30, command=lambda: self.set_yahidot(3))
        self._make_sub_button("4", x, y + 60, command=lambda: self.set_yahidot(4))
        self._make_sub_button("5", x, y + 90, command=lambda: self.set_yahidot(5))

    def show_grade_filter_options(self):
        self._current_submenu = "grade"
        self._clear_sub_buttons()

        x = (self.panel_x1 + self.panel_x2) // 2 - 100
        y = (self.panel_y1 + 40)


        self._make_sub_button("11 grade", x, y + 30, command=lambda: self.set_grade(11))
        self._make_sub_button("12 grade", x, y + 60, command=lambda: self.set_grade(12))

    def apply_filters(self):
        self.filtered_pdfs = []

        for pdf in self.PDFS:
            title = pdf[1]
            filename = pdf[2]

            # фильтр по yahidot
            if self.selected_yahidot:
                if self.selected_yahidot == 3 and not any(l in filename for l in ("A", "C")):
                    continue
                if self.selected_yahidot == 4 and not any(l in filename for l in ("C", "E")):
                    continue
                if self.selected_yahidot == 5 and not any(l in filename for l in ("E", "G")):
                    continue

            # фильтр по grade
            if self.selected_grade:
                if self.selected_grade == 11 and not any(l in filename for l in ("A", "C", "E")):
                    continue
                if self.selected_grade == 12 and not any(l in filename for l in ("C", "E", "G")):
                    continue

            self.filtered_pdfs.append(pdf)

        self.render_pdfs()

    def set_yahidot(self, value):
        self.selected_yahidot = value
        self.apply_filters()

    def set_grade(self, value):
        self.selected_grade = value
        self.apply_filters()





    def _rebuild_submenu_if_needed(self):

        if self._current_submenu == "filter":
            self.show_filter_options()
        elif self._current_submenu == "yahidot":
            self.show_yahidot_filter_options()
        elif self._current_submenu == "grade":
            self.show_grade_filter_options()


    def on_choose_filters(self, program_type: str):
        if program_type == "filter":
            self.show_filter_options()
        elif program_type == "yahidot":
            self.show_yahidot_filter_options()
        elif program_type == "grade":
            self.show_grade_filter_options()


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
            # пересчитываем область прокрутки под размер содержимого
            self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all"))

    def _on_scroll_canvas_configure(self, event):
            # чтобы внутренний frame растягивался по ширине scroll_canvas
            self.scroll_canvas.itemconfig(self.list_window_id, width=event.width)

    def _on_mousewheel(self, event):
            # Windows: event.delta обычно кратен 120
            self.scroll_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        # ================= Grid =================

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

        # ================= Window helpers =================

    def show_modal(self):
        self._this_wnd.grab_set()

    def run(self):
        # запускать mainloop только если это корневое окно
        if self._parent_wnd is None:
            self._this_wnd.mainloop()

if __name__ == "__main__":
    gui = Engpdfs(None,1)
    gui.run()