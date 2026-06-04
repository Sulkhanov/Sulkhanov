# settings_panel.py
# Admin settings: change own password, manage other employees

import tkinter as tk
from tkinter import messagebox
from styles import *
from button import Btn
from widgets import make_table, insert_rows


class SettingsPanel(tk.Frame):

    def __init__(self, parent, db, current_user: dict):
        super().__init__(parent, bg=BG_MAIN)
        self.db           = db
        self.current_user = current_user
        self._build()

    def _build(self):
        # Title
        bar = tk.Frame(self, bg=BG_HEADER, height=52)
        bar.pack(fill=tk.X)
        bar.pack_propagate(False)
        tk.Label(bar, text="⚙️  Settings",
                 font=("Helvetica",14,"bold"),
                 bg=BG_HEADER, fg=FG_WHITE).pack(side=tk.LEFT, padx=20, pady=14)

        # Scrollable
        canvas = tk.Canvas(self, bg=BG_MAIN, highlightthickness=0)
        sb = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=sb.set)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(fill=tk.BOTH, expand=True)
        body = tk.Frame(canvas, bg=BG_MAIN)
        canvas.create_window((0,0), window=body, anchor="nw")
        body.bind("<Configure>",
                  lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        self._build_change_password(body)
        self._build_employee_manager(body)

    # ── Section 1: Change own password ───────────────────────────────────
    def _build_change_password(self, parent):
        card = tk.Frame(parent, bg=BG_CARD)
        card.pack(fill=tk.X, padx=24, pady=(20,10))

        tk.Label(card, text="Change My Password",
                 font=("Helvetica",13,"bold"),
                 bg=BG_CARD, fg=FG_DARK).pack(anchor="w", padx=20, pady=(16,4))
        tk.Label(card,
                 text=f"Logged in as: {self.current_user['full_name']} "
                      f"(@{self.current_user['username']})",
                 font=FONT_SMALL, bg=BG_CARD, fg=FG_MUTED
                 ).pack(anchor="w", padx=20, pady=(0,12))

        row = tk.Frame(card, bg=BG_CARD)
        row.pack(fill=tk.X, padx=20, pady=(0,16))

        tk.Label(row, text="New Password:", font=FONT_LABEL,
                 bg=BG_CARD, fg=FG_MUTED).pack(side=tk.LEFT)
        self._new_pwd = tk.StringVar()
        tk.Entry(row, textvariable=self._new_pwd, show="●",
                 font=FONT_BODY, bg=BG_INPUT, fg=FG_DARK,
                 relief="flat", bd=0,
                 highlightthickness=1,
                 highlightbackground=BORDER,
                 highlightcolor=BORDER_FOCUS,
                 insertbackground=FG_DARK,
                 width=22
                 ).pack(side=tk.LEFT, padx=(10,12), ipady=8)

        tk.Label(row, text="Confirm:", font=FONT_LABEL,
                 bg=BG_CARD, fg=FG_MUTED).pack(side=tk.LEFT)
        self._confirm_pwd = tk.StringVar()
        tk.Entry(row, textvariable=self._confirm_pwd, show="●",
                 font=FONT_BODY, bg=BG_INPUT, fg=FG_DARK,
                 relief="flat", bd=0,
                 highlightthickness=1,
                 highlightbackground=BORDER,
                 highlightcolor=BORDER_FOCUS,
                 insertbackground=FG_DARK,
                 width=22
                 ).pack(side=tk.LEFT, padx=(10,12), ipady=8)

        Btn(row, "Update Password",
            command=self._change_password,
            kind="primary").pack(side=tk.LEFT, ipady=2)

    def _change_password(self):
        p1 = self._new_pwd.get().strip()
        p2 = self._confirm_pwd.get().strip()
        if not p1:
            messagebox.showerror("Error", "Password cannot be empty.")
            return
        if p1 != p2:
            messagebox.showerror("Error", "Passwords do not match.")
            return
        if len(p1) < 4:
            messagebox.showerror("Error", "Password must be at least 4 characters.")
            return
        self.db.update_employee_password(self.current_user["employee_id"], p1)
        messagebox.showinfo("Success", "Password updated. Use it next time you log in.")
        self._new_pwd.set("")
        self._confirm_pwd.set("")

    # ── Section 2: Manage employees ───────────────────────────────────────
    def _build_employee_manager(self, parent):
        card = tk.Frame(parent, bg=BG_CARD)
        card.pack(fill=tk.X, padx=24, pady=(0,20))

        tk.Label(card, text="Manage Employee Accounts",
                 font=("Helvetica",13,"bold"),
                 bg=BG_CARD, fg=FG_DARK).pack(anchor="w", padx=20, pady=(16,12))

        # Add employee form
        add_f = tk.Frame(card, bg="#F9FAFB")
        add_f.pack(fill=tk.X, padx=20, pady=(0,12))

        tk.Label(add_f, text="Add new employee",
                 font=("Helvetica",11,"bold"),
                 bg="#F9FAFB", fg=FG_DARK).pack(anchor="w", padx=12, pady=(10,6))

        row = tk.Frame(add_f, bg="#F9FAFB")
        row.pack(fill=tk.X, padx=12, pady=(0,12))

        def lbl_e(text, width=14):
            tk.Label(row, text=text, font=("Helvetica",10),
                     bg="#F9FAFB", fg=FG_MUTED).pack(side=tk.LEFT)
            v = tk.StringVar()
            tk.Entry(row, textvariable=v,
                     font=FONT_BODY, bg=BG_INPUT, fg=FG_DARK,
                     relief="flat", bd=0,
                     highlightthickness=1,
                     highlightbackground=BORDER,
                     highlightcolor=BORDER_FOCUS,
                     insertbackground=FG_DARK,
                     width=width
                     ).pack(side=tk.LEFT, padx=(6,14), ipady=7)
            return v

        self._emp_name = lbl_e("Full Name:", 18)
        self._emp_user = lbl_e("Username:", 14)
        self._emp_pwd  = lbl_e("Password:", 14)

        Btn(row, "Add Employee",
            command=self._add_employee,
            kind="success").pack(side=tk.LEFT, ipady=2)

        # Employee list
        tk.Label(card, text="Current Employees",
                 font=("Helvetica",11,"bold"),
                 bg=BG_CARD, fg=FG_DARK).pack(anchor="w", padx=20, pady=(4,6))

        tbl_f = tk.Frame(card, bg=BG_CARD)
        tbl_f.pack(fill=tk.X, padx=20, pady=(0,16))

        self._emp_tv = make_table(
            tbl_f,
            columns=("id","name","username"),
            headings=("ID","Full Name","Username"),
            widths=[60, 240, 180])

        btn_row = tk.Frame(card, bg=BG_CARD)
        btn_row.pack(fill=tk.X, padx=20, pady=(0,16))
        Btn(btn_row, "🔄  Refresh List",
            command=self._load_employees,
            kind="neutral").pack(side=tk.LEFT, padx=(0,10), ipady=2)
        Btn(btn_row, "🗑  Delete Selected",
            command=self._delete_employee,
            kind="danger").pack(side=tk.LEFT, ipady=2)

        self._load_employees()

    def _load_employees(self):
        emps = self.db.get_all_employees()
        insert_rows(self._emp_tv, [
            (e["employee_id"], e["full_name"], e["username"])
            for e in emps
        ])

    def _add_employee(self):
        name = self._emp_name.get().strip()
        user = self._emp_user.get().strip()
        pwd  = self._emp_pwd.get().strip()
        if not name or not user or not pwd:
            messagebox.showerror("Error", "All fields are required.")
            return
        try:
            self.db.add_employee(user, pwd, name)
            messagebox.showinfo("Added", f"Employee '{name}' added.")
            self._emp_name.set("")
            self._emp_user.set("")
            self._emp_pwd.set("")
            self._load_employees()
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def _delete_employee(self):
        sel = self._emp_tv.selection()
        if not sel:
            messagebox.showwarning("Select", "Select an employee first.")
            return
        eid = int(self._emp_tv.item(sel[0])["values"][0])
        if eid == self.current_user["employee_id"]:
            messagebox.showerror("Error", "You cannot delete your own account.")
            return
        name = self._emp_tv.item(sel[0])["values"][1]
        if messagebox.askyesno("Delete", f"Delete employee '{name}'?"):
            self.db.delete_employee(eid)
            self._load_employees()
