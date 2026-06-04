# widgets.py
import tkinter as tk
from tkinter import ttk
from styles import *


def entry(parent, label_text, var=None, show=None, hint=None):
    """Labeled text entry."""
    tk.Label(parent, text=label_text, font=FONT_LABEL,
             bg=BG_CARD, fg=FG_MUTED, anchor="w").pack(anchor="w", pady=(10,2))
    v = var or tk.StringVar()
    e = tk.Entry(parent, textvariable=v, show=show or "",
                 font=FONT_BODY, bg=BG_INPUT, fg=FG_DARK,
                 relief="flat", bd=0,
                 highlightthickness=1,
                 highlightbackground=BORDER,
                 highlightcolor=BORDER_FOCUS,
                 insertbackground=FG_DARK)
    e.pack(fill=tk.X, ipady=9)
    if hint:
        tk.Label(parent, text=hint, font=("Helvetica",9),
                 bg=BG_CARD, fg="#9CA3AF", anchor="w").pack(anchor="w")
    return v, e


def section_title(parent, text):
    f = tk.Frame(parent, bg=BG_MAIN)
    f.pack(fill=tk.X, pady=(4,10))
    tk.Label(f, text=text, font=FONT_SECTION,
             bg=BG_MAIN, fg=FG_DARK).pack(side=tk.LEFT)
    tk.Frame(f, bg=BORDER, height=1).pack(
        side=tk.LEFT, fill=tk.X, expand=True, padx=(10,0), pady=8)


def make_table(parent, columns, headings, widths):
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("App.Treeview",
                    background="#FFFFFF", foreground=FG_DARK,
                    rowheight=32, fieldbackground="#FFFFFF",
                    font=FONT_BODY, borderwidth=0)
    style.configure("App.Treeview.Heading",
                    background=BG_HEADER, foreground=FG_WHITE,
                    font=("Helvetica",11,"bold"), relief="flat", padding=6)
    style.map("App.Treeview",
              background=[("selected","#DBEAFE")],
              foreground=[("selected", FG_DARK)])

    wrap = tk.Frame(parent, bg="#E5E7EB")
    wrap.pack(fill=tk.BOTH, expand=True)
    sb = ttk.Scrollbar(wrap, orient="vertical")
    sb.pack(side=tk.RIGHT, fill=tk.Y)
    tv = ttk.Treeview(wrap, columns=columns, show="headings",
                      style="App.Treeview", yscrollcommand=sb.set)
    sb.config(command=tv.yview)
    for col, head, w in zip(columns, headings, widths):
        tv.heading(col, text=head)
        tv.column(col, width=w, anchor="center", minwidth=40)
    tv.tag_configure("odd",  background="#F9FAFB")
    tv.tag_configure("even", background="#FFFFFF")
    tv.pack(fill=tk.BOTH, expand=True)
    return tv


def insert_rows(tv, rows):
    tv.delete(*tv.get_children())
    for i, row in enumerate(rows):
        tv.insert("", "end", values=row,
                  tags=("odd" if i % 2 else "even",))
