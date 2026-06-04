# main_window.py
import tkinter as tk
from styles import *
from button import Btn

NAV = [
    ("🏠", "Dashboard",         "dashboard"),
    ("➕", "Register Customer", "register"),
    ("🔍", "Search / Browse",   "search"),
    ("📊", "Reports",           "reports"),
    ("⚙️", "Settings",          "settings"),
]


class MainWindow(tk.Tk):

    def __init__(self, user: dict):
        super().__init__()
        self.user = user
        self.title("Bank Customer Service System")
        self.configure(bg=BG_MAIN)
        self._center()
        self._build()
        self._show("dashboard")

    def _center(self):
        self.update_idletasks()
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        # Use 90% of screen size, minimum 1000x660
        w = max(1000, int(sw * 0.85))
        h = max(660,  int(sh * 0.88))
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
        self.minsize(900, 620)

    def _build(self):
        from database_manager import DatabaseManager
        self.db = DatabaseManager()

        # ── Sidebar (fixed 200px) ─────────────────────────────────────────
        side = tk.Frame(self, bg=BG_SIDEBAR, width=200)
        side.pack(side=tk.LEFT, fill=tk.Y)
        side.pack_propagate(False)

        # Logo
        logo = tk.Frame(side, bg="#0F1E35", height=68)
        logo.pack(fill=tk.X)
        logo.pack_propagate(False)
        tk.Label(logo, text="🏦  Bank Service",
                 font=("Helvetica", 13, "bold"),
                 bg="#0F1E35", fg=FG_WHITE).pack(expand=True)

        # Employee name
        tk.Label(side,
                 text=f"👤  {self.user['full_name']}",
                 font=("Helvetica", 10),
                 bg=BG_SIDEBAR, fg="#93C5FD",
                 wraplength=180, justify="left"
                 ).pack(anchor="w", padx=12, pady=(10, 4))
        tk.Frame(side, bg="#2D4070", height=1).pack(fill=tk.X, padx=10, pady=5)

        # Nav buttons
        self._nav_btns = {}
        for icon, label, key in NAV:
            b = Btn(side, f"  {icon}  {label}",
                    command=lambda k=key: self._show(k),
                    kind="nav", font=("Helvetica", 10))
            b.config(anchor="w", pady=11)
            b.pack(fill=tk.X, padx=5, pady=1)
            self._nav_btns[key] = b

        tk.Frame(side, bg=BG_SIDEBAR).pack(fill=tk.BOTH, expand=True)

        logout = Btn(side, "  🔓  Logout",
                     command=self._logout,
                     kind="logout", font=("Helvetica", 10))
        logout.config(anchor="w", pady=11)
        logout.pack(fill=tk.X, padx=5, pady=8)

        # ── Content (fills remaining space) ───────────────────────────────
        self._content = tk.Frame(self, bg=BG_MAIN)
        self._content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def _show(self, key, **kw):
        for k, b in self._nav_btns.items():
            b._bg    = BG_SIDEBAR_H if k == key else BG_SIDEBAR
            b._hover = "#3A5090"    if k == key else BG_SIDEBAR_H
            b.config(bg=b._bg)

        for w in self._content.winfo_children():
            w.destroy()

        if key == "dashboard":
            self._dashboard()
        elif key == "register":
            from customer_form import CustomerForm
            CustomerForm(self._content, self.db).pack(fill=tk.BOTH, expand=True)
        elif key == "search":
            from search_panel import SearchPanel
            SearchPanel(self._content, self.db,
                        on_select=lambda cid: self._show("account", customer_id=cid)
                        ).pack(fill=tk.BOTH, expand=True)
        elif key == "reports":
            from report_panel import ReportPanel
            ReportPanel(self._content, self.db).pack(fill=tk.BOTH, expand=True)
        elif key == "settings":
            from settings_panel import SettingsPanel
            SettingsPanel(self._content, self.db, self.user
                          ).pack(fill=tk.BOTH, expand=True)
        elif key == "account":
            from account_view import AccountView
            AccountView(self._content, self.db,
                        customer_id=kw["customer_id"],
                        on_back=lambda: self._show("search")
                        ).pack(fill=tk.BOTH, expand=True)

    def _dashboard(self):
        from widgets import make_table, insert_rows
        s = self.db.get_summary()

        # Title bar
        bar = tk.Frame(self._content, bg=BG_HEADER, height=52)
        bar.pack(fill=tk.X)
        bar.pack_propagate(False)
        tk.Label(bar, text=f"Welcome, {self.user['full_name']}",
                 font=("Helvetica", 13, "bold"),
                 bg=BG_HEADER, fg=FG_WHITE
                 ).pack(side=tk.LEFT, padx=20, pady=14)

        # ── Stat tiles — use grid so they share space equally ─────────────
        tiles_outer = tk.Frame(self._content, bg=BG_MAIN)
        tiles_outer.pack(fill=tk.X, padx=16, pady=14)

        tile_data = [
            ("Active Customers",  str(s["total_customers"]),                          "#1C3A6B"),
            ("Transactions",      str(s["total_deposits"] + s["total_withdrawals"]),   "#15803D"),
            ("Total Funds",       f"€{s['total_balance']:,.2f}",                       "#5B21B6"),
        ]
        for i, (label, val, color) in enumerate(tile_data):
            tile = tk.Frame(tiles_outer, bg=color)
            tile.grid(row=0, column=i,
                      padx=(0 if i == 0 else 8, 0),
                      sticky="nsew", ipadx=10, ipady=12)
            tiles_outer.columnconfigure(i, weight=1)
            tk.Label(tile, text=val,
                     font=("Helvetica", 22, "bold"),
                     bg=color, fg=FG_WHITE).pack(pady=(14, 2))
            tk.Label(tile, text=label,
                     font=("Helvetica", 10),
                     bg=color, fg="#CBD5E0").pack(pady=(0, 14))

        # ── Quick actions ─────────────────────────────────────────────────
        tk.Label(self._content, text="Quick Actions",
                 font=FONT_SECTION, bg=BG_MAIN, fg=FG_DARK
                 ).pack(anchor="w", padx=16, pady=(4, 6))

        btn_row = tk.Frame(self._content, bg=BG_MAIN)
        btn_row.pack(fill=tk.X, padx=16, pady=(0, 12))

        Btn(btn_row, "➕  Register New Customer",
            command=lambda: self._show("register"),
            kind="primary").pack(side=tk.LEFT, padx=(0, 8), ipady=4)
        Btn(btn_row, "🔍  Search Customer",
            command=lambda: self._show("search"),
            kind="neutral").pack(side=tk.LEFT, padx=(0, 8), ipady=4)
        Btn(btn_row, "📊  Reports",
            command=lambda: self._show("reports"),
            kind="neutral").pack(side=tk.LEFT, ipady=4)

        # ── Customer table ────────────────────────────────────────────────
        hdr = tk.Frame(self._content, bg=BG_MAIN)
        hdr.pack(fill=tk.X, padx=16, pady=(4, 6))
        tk.Label(hdr, text="All Active Customers",
                 font=FONT_SECTION, bg=BG_MAIN, fg=FG_DARK).pack(side=tk.LEFT)
        tk.Frame(hdr, bg=BORDER, height=1).pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0), pady=8)

        tf = tk.Frame(self._content, bg=BG_MAIN)
        tf.pack(fill=tk.BOTH, expand=True, padx=16, pady=(0, 14))

        tv = make_table(
            tf,
            columns=("id", "name", "balance", "status"),
            headings=("ID", "Full Name", "Balance (€)", "Status"),
            widths=[60, 280, 160, 100],
        )
        insert_rows(tv, [
            (r["customer_id"],
             f"{r['first_name']} {r['last_name']}",
             f"€{r['balance']:,.2f}",
             r["status"].upper())
            for r in self.db.get_all_customers()
        ])
        tv.bind("<Double-1>", lambda _: self._open_tv(tv))

    def _open_tv(self, tv):
        sel = tv.selection()
        if sel:
            self._show("account",
                       customer_id=int(tv.item(sel[0])["values"][0]))

    def _logout(self):
        self.destroy()
        from login_window import LoginWindow
        LoginWindow(on_success=lambda u: MainWindow(u).mainloop()).mainloop()
