import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # For background image

from core.paths import IMAGES_DIR
from core.database import fetch_all_users, fetch_all_reservations, get_ticket_summary


class AdminMainPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Dashboard")
        self.root.attributes('-fullscreen', True)  # Full screen

        # Load and set background image
        self.bg_image = Image.open(os.path.join(IMAGES_DIR, "back.jpg"))  # Ensure this image exists
        self.bg_image = self.bg_image.resize(
            (self.root.winfo_screenwidth(), self.root.winfo_screenheight()),
            Image.Resampling.LANCZOS,
        )
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Create Canvas for background
        self.canvas = tk.Canvas(
            root,
            width=self.root.winfo_screenwidth(),
            height=self.root.winfo_screenheight(),
        )
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # Frame for content
        self.frame = tk.Frame(root, bg='white', bd=3, relief="solid")
        self.frame.place(relx=0.5, rely=0.5, anchor="center", width=1000, height=600)

        # Title
        self.label_title = tk.Label(
            self.frame, text="Admin Dashboard", font=('Arial', 42, 'bold'),
            bg="white", fg="#222",
        )
        self.label_title.pack(pady=20)

        # Create Tabs
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(expand=True, fill="both", padx=20, pady=10)

        # Users Tab
        self.users_frame = tk.Frame(self.notebook, bg="white", padx=20, pady=20)
        self.notebook.add(self.users_frame, text="Registered Users")
        self.display_users()

        # Bookings Tab
        self.bookings_frame = tk.Frame(self.notebook, bg="white", padx=20, pady=20)
        self.notebook.add(self.bookings_frame, text="Tickets Booked")
        self.display_bookings()

        # Summary Tab
        self.summary_frame = tk.Frame(self.notebook, bg="white", padx=20, pady=20)
        self.notebook.add(self.summary_frame, text="Ticket Summary")
        self.display_ticket_summary()

        # Logout Button (Centered Below)
        self.button_logout = tk.Button(
            self.frame, text="Logout", font=('Arial', 24, 'bold'),
            command=self.logout, bg="#d9534f", fg="white", width=12, height=1,
        )
        self.button_logout.pack(pady=20)

    def display_users(self):
        """ Display list of registered users in a table """
        users = fetch_all_users()

        tree = ttk.Treeview(
            self.users_frame, columns=("ID", "Username"),
            show="headings", height=12,
        )
        tree.heading("ID", text="User ID", anchor="center")
        tree.heading("Username", text="Username", anchor="center")
        tree.column("ID", width=150, anchor="center")
        tree.column("Username", width=300, anchor="center")
        tree.pack(expand=True, fill="both")

        for user in users:
            tree.insert("", "end", values=(user[0], user[1]))

    def display_bookings(self):
        """ Display list of booked tickets with details including booking time """
        reservations = fetch_all_reservations()

        tree = ttk.Treeview(
            self.bookings_frame,
            columns=("ID", "User", "Bus", "Seats", "Time"),
            show="headings", height=12,
        )
        tree.heading("ID", text="Booking ID", anchor="center")
        tree.heading("User", text="User Name", anchor="center")
        tree.heading("Bus", text="Bus Name", anchor="center")
        tree.heading("Seats", text="Seats Booked", anchor="center")
        tree.heading("Time", text="Booking Time", anchor="center")

        tree.column("ID", width=100, anchor="center")
        tree.column("User", width=200, anchor="center")
        tree.column("Bus", width=250, anchor="center")
        tree.column("Seats", width=150, anchor="center")
        tree.column("Time", width=200, anchor="center")
        tree.pack(expand=True, fill="both")

        for res in reservations:
            tree.insert("", "end", values=(res[0], res[1], res[2], res[3], res[4]))

    def display_ticket_summary(self):
        """ Display a summary of total bookings per bus """
        ticket_summary = get_ticket_summary()

        tree = ttk.Treeview(
            self.summary_frame, columns=("Bus", "Total Tickets"),
            show="headings", height=12,
        )
        tree.heading("Bus", text="Bus Name", anchor="center")
        tree.heading("Total Tickets", text="Total Tickets Booked", anchor="center")
        tree.column("Bus", width=350, anchor="center")
        tree.column("Total Tickets", width=200, anchor="center")
        tree.pack(expand=True, fill="both")

        for summary in ticket_summary:
            tree.insert("", "end", values=(summary[0], summary[1]))

    def logout(self):
        """ Logout the admin and return to the admin login page """
        self.root.destroy()
        import app
        app.admin_login_page()
