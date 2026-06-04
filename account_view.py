# account_view.py
import tkinter as tk
from tkinter import messagebox
from styles import *
from button import Btn
from widgets import make_table, insert_rows


class AccountView(tk.Frame):

    def __init__(self, parent, db, customer_id, on_back=None):
        super().__init__(parent, bg=BG_MAIN)
        self.db          = db
        self.customer_id = customer_id
        self.on_back     = on_back
        self._build()
        self._refresh()

    def _build(self):
        # Top bar
        top = tk.Frame(self, bg=BG_HEADER, height=52)
        top.pack(fill=tk.X)
        top.pack_propagate(False)
        if self.on_back:
            Btn(top, "← Back", command=self.on_back,
                kind="neutral", font=("Helvetica",10,"bold")
                ).pack(side=tk.LEFT, padx=12, pady=8, ipady=2)
        self._name_lbl = tk.Label(top, text="",
                                  font=("Helvetica",14,"bold"),
                                  bg=BG_HEADER, fg=FG_WHITE)
        self._name_lbl.pack(side=tk.LEFT, padx=8)

        # Profile card
        info_card = tk.Frame(self, bg=BG_CARD)
        info_card.pack(fill=tk.X, padx=20, pady=(14,0))
        inner = tk.Frame(info_card, bg=BG_CARD)
        inner.pack(fill=tk.X, padx=20, pady=14)
        self._info = {}
        fields = [("Customer ID","id"),("Date of Birth","dob"),
                  ("ID Number","id_num"),("Phone","phone"),
                  ("Email","email"),("Status","status")]
        for i,(label,key) in enumerate(fields):
            r,c = divmod(i,3)
            tk.Label(inner, text=label, font=("Helvetica",9),
                     bg=BG_CARD, fg=FG_MUTED
                     ).grid(row=r*2, column=c, sticky="w", padx=(0,30), pady=(8,0))
            v = tk.StringVar()
            self._info[key] = v
            tk.Label(inner, textvariable=v,
                     font=("Helvetica",11,"bold"),
                     bg=BG_CARD, fg=FG_DARK
                     ).grid(row=r*2+1, column=c, sticky="w", padx=(0,30))

        # Balance strip
        bal = tk.Frame(self, bg="#0F2A50", height=56)
        bal.pack(fill=tk.X, padx=20, pady=(10,0))
        bal.pack_propagate(False)
        tk.Label(bal, text="Account Balance",
                 font=("Helvetica",10), bg="#0F2A50", fg="#93C5FD"
                 ).pack(side=tk.LEFT, padx=20)
        self._bal_lbl = tk.Label(bal, text="",
                                 font=("Helvetica",20,"bold"),
                                 bg="#0F2A50", fg=FG_WHITE)
        self._bal_lbl.pack(side=tk.LEFT)

        # Action buttons
        acts = tk.Frame(self, bg=BG_MAIN)
        acts.pack(fill=tk.X, padx=20, pady=12)
        Btn(acts, "💰  Deposit",      command=self._deposit, kind="success").pack(side=tk.LEFT, padx=(0,8), ipady=3)
        Btn(acts, "💸  Withdraw",     command=self._withdraw, kind="danger").pack(side=tk.LEFT, padx=(0,8), ipady=3)
        Btn(acts, "✏️  Edit Profile", command=self._edit,    kind="primary").pack(side=tk.LEFT, padx=(0,8), ipady=3)
        Btn(acts, "🔒  Close Account",command=self._close,   kind="neutral").pack(side=tk.RIGHT, ipady=3)

        # Transaction history
        hdr = tk.Frame(self, bg=BG_MAIN)
        hdr.pack(fill=tk.X, padx=20, pady=(4,6))
        tk.Label(hdr, text="Transaction History",
                 font=FONT_SECTION, bg=BG_MAIN, fg=FG_DARK).pack(side=tk.LEFT)
        tk.Frame(hdr, bg=BORDER, height=1).pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=(10,0), pady=9)

        tf = tk.Frame(self, bg=BG_MAIN)
        tf.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0,16))
        self._tv = make_table(tf,
            columns=("id","type","amount","ts"),
            headings=("ID","Type","Amount (€)","Date & Time"),
            widths=[60,130,150,220])

    def _refresh(self):
        d = self.db.get_customer(self.customer_id)
        if not d: return
        self._name_lbl.config(text=f"{d['first_name']} {d['last_name']}")
        self._info["id"].set(str(d["customer_id"]))
        self._info["dob"].set(d["date_of_birth"] or "—")
        self._info["id_num"].set(d["id_number"] or "—")
        self._info["phone"].set(d["phone"] or "—")
        self._info["email"].set(d["email"] or "—")
        self._info["status"].set(d["status"].upper())
        self._bal_lbl.config(text=f"€ {d['balance']:,.2f}")
        txs = self.db.get_transactions(self.customer_id)
        insert_rows(self._tv, [
            (t["transaction_id"],
             t["type"].capitalize(),
             ("+" if t["type"]=="deposit" else "−") + f"€{t['amount']:,.2f}",
             t["timestamp"])
            for t in txs
        ])

    def _amount_dialog(self, title):
        dlg = tk.Toplevel(self)
        dlg.title(title)
        dlg.geometry("340x190")
        dlg.resizable(False, False)
        dlg.grab_set()
        dlg.configure(bg=BG_MAIN)
        tk.Label(dlg, text=title, font=("Helvetica",13,"bold"),
                 bg=BG_MAIN, fg=FG_DARK).pack(pady=(22,4))
        tk.Label(dlg, text="Enter amount (€):", font=FONT_LABEL,
                 bg=BG_MAIN, fg=FG_MUTED).pack()
        amt = tk.StringVar()
        e = tk.Entry(dlg, textvariable=amt,
                     font=("Helvetica",16), bg=BG_INPUT, fg=FG_DARK,
                     relief="flat", bd=0,
                     highlightthickness=1,
                     highlightbackground=BORDER,
                     highlightcolor=BORDER_FOCUS,
                     insertbackground=FG_DARK,
                     justify="center")
        e.pack(padx=40, ipady=9, fill=tk.X, pady=10)
        e.focus()
        result = [None]
        def confirm():
            try:
                result[0] = float(amt.get().strip().replace(",","."))
                dlg.destroy()
            except ValueError:
                messagebox.showerror("Invalid","Enter a valid number.",parent=dlg)
        Btn(dlg, "Confirm", command=confirm, kind="primary").pack(pady=4)
        dlg.bind("<Return>", lambda _: confirm())
        dlg.wait_window()
        return result[0]

    def _deposit(self):
        amount = self._amount_dialog("Deposit Funds")
        if amount is None: return
        try:
            self.db.deposit(self.customer_id, amount)
            self._refresh()
            messagebox.showinfo("Deposited", f"€{amount:,.2f} added to account.")
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def _withdraw(self):
        amount = self._amount_dialog("Withdraw Funds")
        if amount is None: return
        try:
            self.db.withdraw(self.customer_id, amount)
            self._refresh()
            messagebox.showinfo("Withdrawn", f"€{amount:,.2f} withdrawn.")
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def _edit(self):
        from customer_form import CustomerForm
        dlg = tk.Toplevel(self)
        dlg.title("Edit Profile")
        dlg.geometry("660x540")
        dlg.grab_set()
        dlg.configure(bg=BG_MAIN)
        CustomerForm(dlg, self.db,
                     customer_id=self.customer_id,
                     on_save=lambda: (self._refresh(), dlg.destroy())
                     ).pack(fill=tk.BOTH, expand=True)

    def _close(self):
        if not messagebox.askyesno("Close Account",
            "Permanently close this account?\nBalance must be €0.00."):
            return
        try:
            self.db.close_account(self.customer_id)
            messagebox.showinfo("Closed","Account closed successfully.")
            if self.on_back: self.on_back()
        except Exception as ex:
            messagebox.showerror("Cannot Close", str(ex))
