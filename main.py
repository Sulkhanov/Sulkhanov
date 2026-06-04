"""
Bank Customer Service System
Entry point — run this file to start the application.

Default login: admin / admin123
"""
import os
import sys

# Ensure the app directory is on the path
sys.path.insert(0, os.path.dirname(__file__))

from login_window import LoginWindow
from main_window import MainWindow


def on_login_success(user: dict):
    app = MainWindow(user)
    app.mainloop()


if __name__ == '__main__':
    login = LoginWindow(on_success=on_login_success)
    login.mainloop()
