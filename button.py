# button.py
# Custom button that works on macOS (native tk.Button ignores bg on Mac)

import tkinter as tk
from styles import FONT_BTN, FG_WHITE, FG_DARK


class Btn(tk.Label):
    """
    A Label styled as a button. Works on macOS where tk.Button
    ignores background colour. Supports hover highlight.
    """

    STYLES = {
        "primary": ("#1C3A6B", "#2D4F8A", FG_WHITE),
        "success": ("#15803D", "#166534", FG_WHITE),
        "danger":  ("#DC2626", "#B91C1C", FG_WHITE),
        "neutral": ("#4B5563", "#374151", FG_WHITE),
        "light":   ("#E5E7EB", "#D1D5DB", FG_DARK),
        "logout":  ("#7F1D1D", "#991B1B", FG_WHITE),
        "nav":     ("#1C2B4A", "#2D4070", FG_WHITE),
        "nav_on":  ("#2D4070", "#3A5090", FG_WHITE),
        "cal_nav": ("#1C3A6B", "#2D4F8A", FG_WHITE),
    }

    def __init__(self, parent, text, command=None,
                 kind="primary", width=None, font=None, **kw):
        bg, hover_bg, fg = self.STYLES.get(kind, self.STYLES["primary"])
        super().__init__(
            parent,
            text=text,
            bg=bg,
            fg=fg,
            font=font or FONT_BTN,
            cursor="hand2",
            pady=8,
            padx=16,
            anchor="center",
            **kw
        )
        if width:
            self.config(width=width)

        self._bg     = bg
        self._hover  = hover_bg
        self._cmd    = command

        self.bind("<Enter>",         self._on_enter)
        self.bind("<Leave>",         self._on_leave)
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)

    def _on_enter(self, _):
        self.config(bg=self._hover)

    def _on_leave(self, _):
        self.config(bg=self._bg)

    def _on_press(self, _):
        self.config(relief="sunken")

    def _on_release(self, _):
        self.config(relief="flat")
        if self._cmd:
            self._cmd()
