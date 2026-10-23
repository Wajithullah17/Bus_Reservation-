import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

from core.paths import IMAGES_DIR
from core.database import register_user, init_db


class RegistrationPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Bus Reservation System - Register")
        self.root.attributes('-fullscreen', True)

        # Load and resize background image
        self.bg_image = Image.open(os.path.join(IMAGES_DIR, "bus.jpg"))  # Ensure this image exists in the same directory
        self.bg_image = self.bg_image.resize(
            (self.root.winfo_screenwidth(), self.root.winfo_screenheight()),
            Image.Resampling.LANCZOS,
        )
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Canvas for background image
        self.canvas = tk.Canvas(
            root,
            width=self.root.winfo_screenwidth(),
            height=self.root.winfo_screenheight(),
        )
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # Frame for the form
        self.frame = tk.Frame(root, bg='#ffffff', bd=4, relief="solid")
        self.frame.place(relx=0.5, rely=0.5, anchor="center", width=600, height=500)

        # Title Label
        self.label_title = tk.Label(
            self.frame, text="Register", font=('Arial', 42, 'bold'),
            bg='#ffffff', fg='#00796b',
        )
        self.label_title.pack(pady=20)

        # Username & Password
        self.entry_username = self.create_entry("Username")
        self.entry_password = self.create_entry("Password", show="*")

        # Register Button
        self.button_register = tk.Button(
            self.frame, text="Register", font=('Arial', 24, 'bold'),
            command=self.register_user, bg='#00796b', fg='#ffffff',
            width=20, height=1,
        )
        self.button_register.pack(pady=8)

        # Buttons Frame for alignment
        self.button_frame = tk.Frame(self.frame, bg="#ffffff")
        self.button_frame.pack(pady=10)

        # Admin Login Button (Left Side)
        self.button_admin_login = tk.Button(
            self.button_frame, text="Admin Login", font=('Arial', 20),
            command=self.open_admin_login_page, bg='#00483f', fg='#ffffff',
            width=14, height=1,
        )
        self.button_admin_login.grid(row=0, column=0, padx=10)

        # Login Button (Right Side)
        self.button_login = tk.Button(
            self.button_frame, text="Login", font=('Arial', 20),
            command=self.open_login_page, bg='#005a4a', fg='#ffffff',
            width=14, height=1,
        )
        self.button_login.grid(row=0, column=1, padx=10)

        init_db()

    def create_entry(self, placeholder, show=""):
        label = tk.Label(
            self.frame, text=placeholder, font=('Arial', 22),
            bg='#ffffff', fg='#333333',
        )
        label.pack(pady=5)
        entry = tk.Entry(
            self.frame, font=('Arial', 24), show=show, width=22,
            bd=2, relief="solid",
        )
        entry.pack(pady=10)
        return entry

    def register_user(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "All fields are required!")
            return

        if register_user(username, password):
            messagebox.showinfo("Success", "User registered successfully!")
            self.root.destroy()
            import app
            app.login_page()
        else:
            messagebox.showerror("Error", "Username already exists")

    def open_login_page(self):
        self.root.destroy()
        import app
        app.login_page()

    def open_admin_login_page(self):
        self.root.destroy()
        import app
        app.admin_login_page()
