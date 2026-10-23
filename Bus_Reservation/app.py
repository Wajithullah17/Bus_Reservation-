"""
SEAT SURE - Bus Reservation System
Entry point. Run with:  python app.py   (from this folder)

Each page lives in its own module and opens in its own Tk window.
Pages call the functions below to navigate to one another.
"""
import tkinter as tk

from core.database import init_db


def _new_root():
    root = tk.Tk()
    # Press Esc to leave fullscreen (handy while developing)
    root.bind("<Escape>", lambda e: root.attributes('-fullscreen', False))
    return root


def register_page():
    from pages.register import RegistrationPage
    root = _new_root()
    RegistrationPage(root)
    root.mainloop()


def login_page():
    from pages.login import LoginPage
    root = _new_root()
    LoginPage(root)
    root.mainloop()


def admin_login_page():
    from pages.admin_login import AdminLoginPage
    root = _new_root()
    AdminLoginPage(root)
    root.mainloop()


def admin_main_page():
    from pages.admin_main_page import AdminMainPage
    root = _new_root()
    AdminMainPage(root)
    root.mainloop()


def main_page(user_id):
    from pages.main_page import MainPage
    root = _new_root()
    MainPage(root, user_id)
    root.mainloop()


def booking_page(user_id, selected_bus, main_page_callback):
    from pages.booking_page import BookingPage
    root = _new_root()
    BookingPage(root, user_id, selected_bus, main_page_callback)
    root.mainloop()


if __name__ == "__main__":
    init_db()
    register_page()
