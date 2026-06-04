# customer_form.py
import tkinter as tk
from tkinter import messagebox
from styles import *
from button import Btn
from calendar_picker import CalendarPicker


class CustomerForm(tk.Frame):

    def __init__(self, parent, db, customer_id=None, on_save=None):
        super().__init__(parent, bg=BG_MAIN)
        self.db          = db
        self.customer_id = customer_id
        self.on_save     = on_save
        self.vars        = {}
        self._build()
        if customer_id:
            self._load()

    def _build(self):
        mode = "Edit Customer Profile" if self.customer_id else "Register New Customer"

        # Title bar
        bar = tk.Frame(self, bg=BG_HEADER, height=52)
        bar.pack(fill=tk.X)
        bar.pack_propagate(False)
        tk.Label(bar, text=mode, font=("Helvetica",14,"bold"),
                 bg=BG_HEADER, fg=FG_WHITE).pack(side=tk.LEFT, padx=20, pady=14)

        # Scrollable area
        canvas = tk.Canvas(self, bg=BG_MAIN, highlightthickness=0)
        sb = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=sb.set)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(fill=tk.BOTH, expand=True)
        content = tk.Frame(canvas, bg=BG_MAIN)
        canvas.create_window((0,0), window=content, anchor="nw")
        content.bind("<Configure>",
                     lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Card
        card = tk.Frame(content, bg=BG_CARD)
        card.pack(fill=tk.X, padx=24, pady=20)
        pad = tk.Frame(card, bg=BG_CARD)
        pad.pack(fill=tk.X, padx=24, pady=20)
        pad.columnconfigure(0, weight=1)
        pad.columnconfigure(1, weight=1)

        def lbl_entry(label, key, row, col, hint=""):
            tk.Label(pad, text=label, font=FONT_LABEL,
                     bg=BG_CARD, fg=FG_MUTED, anchor="w"
                     ).grid(row=row*3, column=col, sticky="w",
                            pady=(12,2), padx=(0,16))
            v = tk.StringVar()
            self.vars[key] = v
            e = tk.Entry(pad, textvariable=v,
                         font=FONT_BODY, bg=BG_INPUT, fg=FG_DARK,
                         relief="flat", bd=0,
                         highlightthickness=1,
                         highlightbackground=BORDER,
                         highlightcolor=BORDER_FOCUS,
                         insertbackground=FG_DARK)
            e.grid(row=row*3+1, column=col, sticky="ew",
                   ipady=9, padx=(0,16))
            if hint:
                tk.Label(pad, text=hint, font=("Helvetica",9),
                         bg=BG_CARD, fg="#9CA3AF", anchor="w"
                         ).grid(row=row*3+2, column=col, sticky="w", padx=(0,16))
            return v, e

        # Row 0
        lbl_entry("First Name *",  "first_name", 0, 0)
        lbl_entry("Last Name *",   "last_name",  0, 1)

        # Row 1 – DOB with calendar
        dob_r = 3
        tk.Label(pad, text="Date of Birth *", font=FONT_LABEL,
                 bg=BG_CARD, fg=FG_MUTED, anchor="w"
                 ).grid(row=dob_r, column=0, sticky="w",
                        pady=(12,2), padx=(0,16))
        dob_var = tk.StringVar()
        self.vars["dob"] = dob_var
        dob_f = tk.Frame(pad, bg=BG_CARD)
        dob_f.grid(row=dob_r+1, column=0, sticky="ew", padx=(0,16))
        dob_f.columnconfigure(0, weight=1)
        tk.Entry(dob_f, textvariable=dob_var,
                 font=FONT_BODY, bg=BG_INPUT, fg=FG_DARK,
                 relief="flat", bd=0,
                 highlightthickness=1,
                 highlightbackground=BORDER,
                 highlightcolor=BORDER_FOCUS,
                 insertbackground=FG_DARK
                 ).grid(row=0, column=0, sticky="ew", ipady=9)
        Btn(dob_f, "📅", command=lambda: CalendarPicker(self, dob_var),
            kind="primary", font=("Helvetica",13)
            ).grid(row=0, column=1, padx=(4,0), ipady=6, sticky="ns")
        tk.Label(pad, text="Click 📅 or type YYYY-MM-DD",
                 font=("Helvetica",9), bg=BG_CARD, fg="#9CA3AF", anchor="w"
                 ).grid(row=dob_r+2, column=0, sticky="w", padx=(0,16))

        lbl_entry("ID Number *",   "id_number", 1, 1, "e.g. LV123456")

        # Row 2
        lbl_entry("Phone",  "phone", 2, 0, "e.g. +371 20000001")
        lbl_entry("Email",  "email", 2, 1, "e.g. name@example.com")

        # Buttons
        btn_row = tk.Frame(card, bg=BG_CARD)
        btn_row.pack(fill=tk.X, padx=24, pady=(0,20))
        Btn(btn_row, "✕  Clear",  command=self._clear,
            kind="neutral").pack(side=tk.RIGHT, padx=(6,0))
        Btn(btn_row, "✓  Save",   command=self._save,
            kind="success").pack(side=tk.RIGHT)

        # ── Customer receipt box (shows after registration) ───────────────
        self._receipt_frame = tk.Frame(content, bg=BG_CARD)
        self._receipt_frame.pack(fill=tk.X, padx=24, pady=(0,20))

    def _load(self):
        d = self.db.get_customer(self.customer_id)
        if not d: return
        self.vars["first_name"].set(d["first_name"])
        self.vars["last_name"].set(d["last_name"])
        self.vars["dob"].set(d["date_of_birth"] or "")
        self.vars["id_number"].set(d["id_number"] or "")
        self.vars["phone"].set(d["phone"] or "")
        self.vars["email"].set(d["email"] or "")

    def _save(self):
        fn  = self.vars["first_name"].get().strip()
        ln  = self.vars["last_name"].get().strip()
        dob = self.vars["dob"].get().strip()
        idn = self.vars["id_number"].get().strip()
        ph  = self.vars["phone"].get().strip()
        em  = self.vars["email"].get().strip()

        if not fn or not ln or not idn or not dob:
            messagebox.showerror("Missing fields",
                "First Name, Last Name, Date of Birth and ID Number are required.")
            return
        try:
            if self.customer_id:
                self.db.update_customer(
                    self.customer_id,
                    first_name=fn, last_name=ln,
                    date_of_birth=dob, id_number=idn,
                    phone=ph, email=em)
                messagebox.showinfo("Saved", "Customer profile updated.")
            else:
                new_id = self.db.add_customer(fn, ln, dob, idn, ph, em)
                self._show_receipt(new_id, fn, ln, dob, idn, ph, em)
                self._clear()
            if self.on_save:
                self.on_save()
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def _show_receipt(self, cid, fn, ln, dob, idn, ph, em):
        """Show a green confirmation box with all customer details."""
        for w in self._receipt_frame.winfo_children():
            w.destroy()

        r = self._receipt_frame
        tk.Frame(r, bg="#15803D", height=4).pack(fill=tk.X)

        inner = tk.Frame(r, bg="#F0FDF4")
        inner.pack(fill=tk.X, padx=0, pady=0)

        tk.Label(inner, text="✅  Customer Registered Successfully",
                 font=("Helvetica",13,"bold"),
                 bg="#F0FDF4", fg="#15803D"
                 ).pack(anchor="w", padx=20, pady=(14,8))

        details = [
            ("Customer ID",    str(cid)),
            ("Full Name",      f"{fn} {ln}"),
            ("Date of Birth",  dob),
            ("ID Number",      idn),
            ("Phone",          ph or "—"),
            ("Email",          em or "—"),
            ("Opening Balance","€0.00"),
            ("Status",         "ACTIVE"),
        ]
        grid = tk.Frame(inner, bg="#F0FDF4")
        grid.pack(fill=tk.X, padx=20, pady=(0,16))
        for i, (label, val) in enumerate(details):
            r2, c2 = divmod(i, 2)
            tk.Label(grid, text=label+":", font=("Helvetica",10),
                     bg="#F0FDF4", fg="#166534", anchor="w"
                     ).grid(row=r2*2, column=c2, sticky="w", padx=(0,30), pady=(6,0))
            tk.Label(grid, text=val, font=("Helvetica",11,"bold"),
                     bg="#F0FDF4", fg="#14532D", anchor="w"
                     ).grid(row=r2*2+1, column=c2, sticky="w", padx=(0,30))
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)

        tk.Label(inner,
                 text="The customer can now be found via Search / Browse.",
                 font=("Helvetica",10), bg="#F0FDF4", fg="#166534"
                 ).pack(anchor="w", padx=20, pady=(0,14))

    def _clear(self):
        for v in self.vars.values():
            v.set("")
        for w in self._receipt_frame.winfo_children():
            w.destroy()
