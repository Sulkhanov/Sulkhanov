# report_panel.py
import tkinter as tk
from styles import *
from button import Btn


class ReportPanel(tk.Frame):

    def __init__(self, parent, db):
        super().__init__(parent, bg=BG_MAIN)
        self.db = db
        self._build()

    def _build(self):
        bar = tk.Frame(self, bg=BG_HEADER, height=52)
        bar.pack(fill=tk.X)
        bar.pack_propagate(False)
        tk.Label(bar, text="Summary Report",
                 font=("Helvetica",14,"bold"),
                 bg=BG_HEADER, fg=FG_WHITE).pack(side=tk.LEFT, padx=20, pady=14)

        s = self.db.get_summary()
        grid = tk.Frame(self, bg=BG_MAIN)
        grid.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        for i,(label,val,color,icon) in enumerate([
            ("Active Customers",  str(s["total_customers"]),       "#1C3A6B","👤"),
            ("Deposits Made",     str(s["total_deposits"]),         "#15803D","📥"),
            ("Withdrawals Made",  str(s["total_withdrawals"]),      "#DC2626","📤"),
            ("Total Funds Held",  f"€{s['total_balance']:,.2f}",   "#5B21B6","💶"),
        ]):
            r,c = divmod(i,2)
            tile = tk.Frame(grid, bg=color)
            tile.grid(row=r, column=c, padx=10, pady=10,
                      sticky="nsew", ipadx=20, ipady=24)
            grid.rowconfigure(r, weight=1)
            grid.columnconfigure(c, weight=1)
            tk.Label(tile, text=icon, font=("Helvetica",38),
                     bg=color, fg=FG_WHITE).pack(pady=(20,6))
            tk.Label(tile, text=val, font=("Helvetica",30,"bold"),
                     bg=color, fg=FG_WHITE).pack()
            tk.Label(tile, text=label, font=("Helvetica",11),
                     bg=color, fg="#CBD5E0").pack(pady=(2,20))

        Btn(self, "🔄  Refresh", command=self._refresh,
            kind="neutral").pack(pady=10, ipady=3)

    def _refresh(self):
        for w in self.winfo_children(): w.destroy()
        self._build()
