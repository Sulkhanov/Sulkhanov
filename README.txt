================================================================
  Bank Customer Service System
  Software Engineering Course Project - TSI 2025
  Student: Farrukh Sulkhanov | Code: ST79251 | Group: 4302BDA
================================================================

HOW TO RUN
----------

Windows:
  Double-click  run.bat
  (or open CMD, cd into this folder, type: python main.py)

Mac / Linux:
  Open Terminal, cd into this folder, then:
    bash run.sh
  (or directly: python3 main.py)

DEFAULT LOGIN
-------------
  Username : admin
  Password : admin123

REQUIREMENTS
------------
  Python 3.10 or higher
  tkinter  (included with Python on Windows and macOS)

  Linux only - install tkinter if missing:
    sudo apt install python3-tk        (Ubuntu/Debian)
    sudo dnf install python3-tkinter   (Fedora)

FEATURES
--------
  Login / Logout with employee authentication
  Register new customers (name, DOB, ID number, phone, email)
  Search and browse all active customers
  View account details and full transaction history
  Deposit funds (with positive-amount validation)
  Withdraw funds (with insufficient-funds check)
  Edit customer profile
  Close account (requires zero balance)
  Summary reports dashboard

FILES
-----
  main.py              Entry point - run this
  login_window.py      Authentication screen
  main_window.py       Main navigation + dashboard
  customer_form.py     Register / Edit customer form
  account_view.py      Account details, deposit, withdraw, close
  search_panel.py      Customer search and browse table
  report_panel.py      Summary statistics (4 tiles)
  database_manager.py  SQLite data access layer (Singleton)
  models.py            Customer and Transaction data classes
  styles.py            Colours, fonts, button styles
  widgets.py           Reusable UI components
  bank.db              SQLite database (auto-created on first run)

================================================================
