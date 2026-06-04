# calendar_picker.py
# A clean pop-up calendar widget for date selection

import tkinter as tk
import calendar
from datetime import date
from styles import BG_CARD, BG_HEADER, FG_WHITE, FG_DARK, FG_MUTED, BORDER, FONT_BODY, FONT_LABEL, FONT_BTN


class CalendarPicker(tk.Toplevel):
    """
    Pop-up month calendar. Call CalendarPicker(parent, var) where
    var is a StringVar that receives the selected date as YYYY-MM-DD.
    """

    def __init__(self, parent, var: tk.StringVar):
        super().__init__(parent)
        self.var = var
        self.title("Pick a date")
        self.resizable(False, False)
        self.grab_set()
        self.configure(bg=BG_CARD)

        # Start from var value or today
        try:
            parts = var.get().split("-")
            self._year  = int(parts[0])
            self._month = int(parts[1])
        except Exception:
            today = date.today()
            self._year  = today.year - 30   # sensible default for DOB
            self._month = today.month

        self._selected_day = None
        self._build()
        self._center(parent)

    def _center(self, parent):
        self.update_idletasks()
        px = parent.winfo_rootx() + parent.winfo_width()  // 2
        py = parent.winfo_rooty() + parent.winfo_height() // 2
        w, h = self.winfo_width(), self.winfo_height()
        self.geometry(f"+{px - w//2}+{py - h//2}")

    def _build(self):
        # ── Navigation bar ────────────────────────────────────────────────
        nav = tk.Frame(self, bg=BG_HEADER)
        nav.pack(fill=tk.X)

        tk.Button(
            nav, text="◀", command=self._prev_month,
            bg=BG_HEADER, fg=FG_WHITE, relief="flat",
            font=FONT_BTN, cursor="hand2", bd=0,
            activebackground="#2D4F8A", activeforeground=FG_WHITE
        ).pack(side=tk.LEFT, padx=8, pady=6)

        self._header_lbl = tk.Label(
            nav, text="", font=("Helvetica", 12, "bold"),
            bg=BG_HEADER, fg=FG_WHITE
        )
        self._header_lbl.pack(side=tk.LEFT, expand=True)

        tk.Button(
            nav, text="▶", command=self._next_month,
            bg=BG_HEADER, fg=FG_WHITE, relief="flat",
            font=FONT_BTN, cursor="hand2", bd=0,
            activebackground="#2D4F8A", activeforeground=FG_WHITE
        ).pack(side=tk.RIGHT, padx=8, pady=6)

        # ── Year quick-jump ───────────────────────────────────────────────
        yr_frame = tk.Frame(self, bg=BG_CARD)
        yr_frame.pack(fill=tk.X, padx=10, pady=(8, 0))

        tk.Label(yr_frame, text="Year:", font=FONT_LABEL,
                 bg=BG_CARD, fg=FG_MUTED).pack(side=tk.LEFT)

        self._year_var = tk.StringVar(value=str(self._year))
        yr_entry = tk.Entry(
            yr_frame, textvariable=self._year_var, width=6,
            font=FONT_BODY, bg="#F0F4FF", fg=FG_DARK,
            relief="flat", bd=0,
            highlightthickness=1, highlightbackground=BORDER
        )
        yr_entry.pack(side=tk.LEFT, padx=(6, 0), ipady=4)
        yr_entry.bind("<Return>", self._jump_year)

        tk.Button(
            yr_frame, text="Go", command=self._jump_year,
            bg="#1C3A6B", fg=FG_WHITE, relief="flat",
            font=("Helvetica", 10, "bold"), cursor="hand2", bd=0,
            padx=8, pady=3,
            activebackground="#2D4F8A", activeforeground=FG_WHITE
        ).pack(side=tk.LEFT, padx=6)

        # ── Day-name headers ──────────────────────────────────────────────
        days_frame = tk.Frame(self, bg=BG_CARD)
        days_frame.pack(padx=10, pady=(8, 2))
        for d in ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]:
            color = "#DC2626" if d in ("Sa", "Su") else FG_MUTED
            tk.Label(
                days_frame, text=d, width=4,
                font=("Helvetica", 10, "bold"),
                bg=BG_CARD, fg=color
            ).pack(side=tk.LEFT)

        # ── Day grid ─────────────────────────────────────────────────────
        self._grid_frame = tk.Frame(self, bg=BG_CARD)
        self._grid_frame.pack(padx=10, pady=(0, 10))

        self._refresh()

    def _refresh(self):
        # Clear old day buttons
        for w in self._grid_frame.winfo_children():
            w.destroy()

        self._header_lbl.config(
            text=f"{calendar.month_name[self._month]} {self._year}"
        )
        self._year_var.set(str(self._year))

        cal = calendar.monthcalendar(self._year, self._month)
        today = date.today()

        for week in cal:
            row_frame = tk.Frame(self._grid_frame, bg=BG_CARD)
            row_frame.pack()
            for col, day in enumerate(week):
                if day == 0:
                    tk.Label(
                        row_frame, text="", width=4,
                        bg=BG_CARD
                    ).pack(side=tk.LEFT, pady=1)
                else:
                    is_today    = (day == today.day and
                                   self._month == today.month and
                                   self._year  == today.year)
                    is_weekend  = col >= 5
                    is_selected = (day == self._selected_day)

                    if is_selected:
                        bg, fg = "#1C3A6B", FG_WHITE
                    elif is_today:
                        bg, fg = "#DBEAFE", "#1C3A6B"
                    elif is_weekend:
                        bg, fg = BG_CARD, "#DC2626"
                    else:
                        bg, fg = BG_CARD, FG_DARK

                    btn = tk.Button(
                        row_frame, text=str(day), width=3,
                        font=("Helvetica", 10),
                        bg=bg, fg=fg,
                        relief="flat", bd=0, cursor="hand2",
                        activebackground="#BFDBFE",
                        activeforeground=FG_DARK,
                        command=lambda d=day: self._pick(d)
                    )
                    btn.pack(side=tk.LEFT, padx=1, pady=1)

    def _pick(self, day):
        self._selected_day = day
        self.var.set(f"{self._year:04d}-{self._month:02d}-{day:02d}")
        self.destroy()

    def _prev_month(self):
        if self._month == 1:
            self._month, self._year = 12, self._year - 1
        else:
            self._month -= 1
        self._refresh()

    def _next_month(self):
        if self._month == 12:
            self._month, self._year = 1, self._year + 1
        else:
            self._month += 1
        self._refresh()

    def _jump_year(self, _event=None):
        try:
            y = int(self._year_var.get())
            if 1900 <= y <= 2100:
                self._year = y
                self._refresh()
        except ValueError:
            pass
