# database_manager.py
import sqlite3
from typing import Optional, List


class DatabaseManager:
    _instance = None

    def __new__(cls, db_path: str = 'bank.db'):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_db(db_path)
        return cls._instance

    def _init_db(self, db_path: str):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()
        self._seed()

    def _create_tables(self):
        cur = self.conn.cursor()
        cur.executescript('''
            CREATE TABLE IF NOT EXISTS employees (
                employee_id  INTEGER PRIMARY KEY AUTOINCREMENT,
                username     TEXT UNIQUE NOT NULL,
                password     TEXT NOT NULL,
                full_name    TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS customers (
                customer_id   INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name    TEXT NOT NULL,
                last_name     TEXT NOT NULL,
                date_of_birth TEXT,
                id_number     TEXT UNIQUE,
                phone         TEXT,
                email         TEXT,
                balance       REAL DEFAULT 0.0,
                status        TEXT DEFAULT 'active'
            );
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id    INTEGER NOT NULL,
                type           TEXT NOT NULL,
                amount         REAL NOT NULL,
                timestamp      TEXT DEFAULT (datetime('now','localtime')),
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
            );
        ''')
        self.conn.commit()

    def _seed(self):
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) FROM employees")
        if cur.fetchone()[0] == 0:
            cur.execute(
                "INSERT INTO employees (username,password,full_name) VALUES (?,?,?)",
                ('admin', 'admin123', 'Bank Administrator')
            )
            self.conn.commit()

    # ── Authentication ────────────────────────────────────────────────────
    def authenticate(self, username, password) -> Optional[dict]:
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM employees WHERE username=? AND password=?",
                    (username, password))
        row = cur.fetchone()
        return dict(row) if row else None

    def get_all_employees(self) -> List[dict]:
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM employees ORDER BY full_name")
        return [dict(r) for r in cur.fetchall()]

    def add_employee(self, username, password, full_name):
        self.conn.execute(
            "INSERT INTO employees (username,password,full_name) VALUES (?,?,?)",
            (username, password, full_name))
        self.conn.commit()

    def update_employee_password(self, employee_id, new_password):
        self.conn.execute(
            "UPDATE employees SET password=? WHERE employee_id=?",
            (new_password, employee_id))
        self.conn.commit()

    def delete_employee(self, employee_id):
        self.conn.execute("DELETE FROM employees WHERE employee_id=?",
                          (employee_id,))
        self.conn.commit()

    # ── Customers ─────────────────────────────────────────────────────────
    def add_customer(self, first_name, last_name, dob,
                     id_num, phone, email) -> int:
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO customers "
            "(first_name,last_name,date_of_birth,id_number,phone,email) "
            "VALUES (?,?,?,?,?,?)",
            (first_name, last_name, dob, id_num, phone, email))
        self.conn.commit()
        return cur.lastrowid

    def get_customer(self, customer_id) -> Optional[dict]:
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM customers WHERE customer_id=?",
                    (customer_id,))
        row = cur.fetchone()
        return dict(row) if row else None

    def search_customers(self, query) -> List[dict]:
        like = f'%{query}%'
        cur = self.conn.cursor()
        cur.execute(
            "SELECT * FROM customers "
            "WHERE (first_name LIKE ? OR last_name LIKE ? OR id_number LIKE ?) "
            "AND status='active'",
            (like, like, like))
        return [dict(r) for r in cur.fetchall()]

    def get_all_customers(self) -> List[dict]:
        cur = self.conn.cursor()
        cur.execute(
            "SELECT * FROM customers WHERE status='active' "
            "ORDER BY last_name, first_name")
        return [dict(r) for r in cur.fetchall()]

    def update_customer(self, customer_id, **fields):
        sets = ', '.join(f'{k}=?' for k in fields)
        vals = list(fields.values()) + [customer_id]
        self.conn.execute(
            f"UPDATE customers SET {sets} WHERE customer_id=?", vals)
        self.conn.commit()

    # ── Transactions ──────────────────────────────────────────────────────
    def deposit(self, customer_id, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        self.conn.execute(
            "UPDATE customers SET balance=balance+? WHERE customer_id=?",
            (amount, customer_id))
        self.conn.execute(
            "INSERT INTO transactions (customer_id,type,amount) VALUES (?,'deposit',?)",
            (customer_id, amount))
        self.conn.commit()

    def withdraw(self, customer_id, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        row = self.get_customer(customer_id)
        if row['balance'] < amount:
            raise ValueError(
                f"Insufficient funds. Balance: €{row['balance']:,.2f}")
        self.conn.execute(
            "UPDATE customers SET balance=balance-? WHERE customer_id=?",
            (amount, customer_id))
        self.conn.execute(
            "INSERT INTO transactions (customer_id,type,amount) VALUES (?,'withdrawal',?)",
            (customer_id, amount))
        self.conn.commit()

    def get_transactions(self, customer_id) -> List[dict]:
        cur = self.conn.cursor()
        cur.execute(
            "SELECT * FROM transactions WHERE customer_id=? "
            "ORDER BY timestamp DESC",
            (customer_id,))
        return [dict(r) for r in cur.fetchall()]

    # ── Account ───────────────────────────────────────────────────────────
    def close_account(self, customer_id):
        row = self.get_customer(customer_id)
        if row['balance'] != 0:
            raise ValueError(
                "Balance must be €0.00 before closing. "
                f"Current balance: €{row['balance']:,.2f}")
        self.conn.execute(
            "UPDATE customers SET status='closed' WHERE customer_id=?",
            (customer_id,))
        self.conn.commit()

    # ── Summary ───────────────────────────────────────────────────────────
    def get_summary(self) -> dict:
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) FROM customers WHERE status='active'")
        total_customers = cur.fetchone()[0]
        cur.execute("SELECT COALESCE(SUM(balance),0) FROM customers WHERE status='active'")
        total_balance = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM transactions WHERE type='deposit'")
        total_deposits = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM transactions WHERE type='withdrawal'")
        total_withdrawals = cur.fetchone()[0]
        return dict(total_customers=total_customers,
                    total_balance=total_balance,
                    total_deposits=total_deposits,
                    total_withdrawals=total_withdrawals)
