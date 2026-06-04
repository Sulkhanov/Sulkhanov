# login_window.py
import tkinter as tk
from tkinter import messagebox
from styles import *
from button import Btn


class LoginWindow(tk.Tk):

    def __init__(self, on_success):
        super().__init__()
        self.on_success = on_success
        self.title("Bank Customer Service System – Login")
        self.geometry("460x580")
        self.resizable(False, False)
        self.configure(bg=BG_MAIN)
        self._center()
        self._build()

    def _center(self):
        self.update_idletasks()
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"460x580+{(sw-460)//2}+{(sh-580)//2}")

    def _build(self):
        # Header
        hdr = tk.Frame(self, bg=BG_HEADER, height=170)
        hdr.pack(fill=tk.X)
        hdr.pack_propagate(False)
        tk.Label(hdr, text="🏦", font=("Helvetica",52),
                 bg=BG_HEADER, fg=FG_WHITE).pack(pady=(26,4))
        tk.Label(hdr, text="Bank Customer Service",
                 font=("Helvetica",14,"bold"),
                 bg=BG_HEADER, fg=FG_WHITE).pack()

        # Card
        card = tk.Frame(self, bg=BG_CARD)
        card.pack(fill=tk.BOTH, expand=True, padx=36, pady=24)

        tk.Label(card, text="Employee Login",
                 font=("Helvetica",16,"bold"),
                 bg=BG_CARD, fg=FG_DARK).pack(anchor="w", pady=(20,16))

        # Username
        tk.Label(card, text="Username", font=FONT_LABEL,
                 bg=BG_CARD, fg=FG_MUTED).pack(anchor="w")
        self._user = tk.StringVar()
        user_e = tk.Entry(card, textvariable=self._user,
                          font=FONT_BODY, bg=BG_INPUT, fg=FG_DARK,
                          relief="flat", bd=0,
                          highlightthickness=1,
                          highlightbackground=BORDER,
                          highlightcolor=BORDER_FOCUS,
                          insertbackground=FG_DARK)
        user_e.pack(fill=tk.X, ipady=10, pady=(3,14))
        user_e.focus()

        # Password
        tk.Label(card, text="Password", font=FONT_LABEL,
                 bg=BG_CARD, fg=FG_MUTED).pack(anchor="w")
        self._pwd = tk.StringVar()
        tk.Entry(card, textvariable=self._pwd, show="●",
                 font=FONT_BODY, bg=BG_INPUT, fg=FG_DARK,
                 relief="flat", bd=0,
                 highlightthickness=1,
                 highlightbackground=BORDER,
                 highlightcolor=BORDER_FOCUS,
                 insertbackground=FG_DARK).pack(fill=tk.X, ipady=10, pady=(3,6))

        tk.Label(card, text="Default credentials: admin / admin123",
                 font=FONT_SMALL, bg=BG_CARD, fg="#9CA3AF").pack(anchor="w", pady=(4,20))

        # ── LOGIN BUTTON (custom, works on macOS) ─────────────────────────
        Btn(card, "Login", command=self._login,
            kind="primary").pack(fill=tk.X, ipady=4)

        self.bind("<Return>", lambda _: self._login())

    def _login(self):
        from database_manager import DatabaseManager
        db = DatabaseManager()
        user = db.authenticate(self._user.get().strip(),
                               self._pwd.get().strip())
        if user:
            self.destroy()
            self.on_success(user)
        else:
            messagebox.showerror("Login failed",
                                 "Incorrect username or password.")
            self._pwd.set("")
