# search_panel.py
import tkinter as tk
from tkinter import messagebox
from styles import *
from button import Btn
from widgets import make_table, insert_rows


class SearchPanel(tk.Frame):

    def __init__(self, parent, db, on_select=None):
        super().__init__(parent, bg=BG_MAIN)
        self.db        = db
        self.on_select = on_select
        self._build()
        self._load_all()

    def _build(self):
        bar = tk.Frame(self, bg=BG_HEADER, height=52)
        bar.pack(fill=tk.X)
        bar.pack_propagate(False)
        tk.Label(bar, text="Search Customers",
                 font=("Helvetica",14,"bold"),
                 bg=BG_HEADER, fg=FG_WHITE).pack(side=tk.LEFT, padx=20, pady=14)

        search_row = tk.Frame(self, bg=BG_MAIN)
        search_row.pack(fill=tk.X, padx=20, pady=14)
        self._q = tk.StringVar()
        e = tk.Entry(search_row, textvariable=self._q,
                     font=FONT_BODY, bg=BG_INPUT, fg=FG_DARK,
                     relief="flat", bd=0,
                     highlightthickness=1,
                     highlightbackground=BORDER,
                     highlightcolor=BORDER_FOCUS,
                     insertbackground=FG_DARK)
        e.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=9)
        e.insert(0, "Search by name or ID number…")
        e.bind("<FocusIn>",
               lambda _: e.delete(0,tk.END) if e.get()=="Search by name or ID number…" else None)
        e.bind("<FocusOut>",
               lambda _: e.insert(0,"Search by name or ID number…") if not e.get() else None)
        e.bind("<Return>", lambda _: self._search())

        Btn(search_row, "🔍  Search", command=self._search,
            kind="primary").pack(side=tk.LEFT, padx=(8,6), ipady=2)
        Btn(search_row, "Show All", command=self._load_all,
            kind="neutral").pack(side=tk.LEFT, ipady=2)

        tk.Label(self, text="Double-click a row to open the account",
                 font=FONT_SMALL, bg=BG_MAIN, fg=FG_MUTED
                 ).pack(anchor="w", padx=20, pady=(0,6))

        tf = tk.Frame(self, bg=BG_MAIN)
        tf.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0,16))
        self._tv = make_table(tf,
            columns=("id","name","dob","id_num","phone","balance"),
            headings=("ID","Full Name","Date of Birth","ID Number","Phone","Balance (€)"),
            widths=[55,180,110,120,130,120])
        self._tv.bind("<Double-1>", self._open)

    def _load_all(self):
        self._q.set("")
        self._show(self.db.get_all_customers())

    def _search(self):
        q = self._q.get().strip()
        if not q or q == "Search by name or ID number…":
            self._load_all(); return
        rows = self.db.search_customers(q)
        self._show(rows)
        if not rows:
            messagebox.showinfo("No Results", f'No customers found for "{q}".')

    def _show(self, rows):
        insert_rows(self._tv, [
            (r["customer_id"],
             f"{r['first_name']} {r['last_name']}",
             r["date_of_birth"] or "—",
             r["id_number"] or "—",
             r["phone"] or "—",
             f"€{r['balance']:,.2f}")
            for r in rows
        ])

    def _open(self, _=None):
        sel = self._tv.selection()
        if sel and self.on_select:
            self.on_select(int(self._tv.item(sel[0])["values"][0]))
