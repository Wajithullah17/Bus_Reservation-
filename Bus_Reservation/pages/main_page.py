import os
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk  # For background image

from core.paths import IMAGES_DIR
from core.database import get_bus_data, fetch_user_bookings, cancel_booking


class MainPage:
    def __init__(self, root, user_id):
        self.root = root
        self.root.title("Bus Reservation System - Main Page")
        self.root.attributes('-fullscreen', True)
        self.user_id = user_id
        self.bookings_window = None

        # Load and set background image
        self.bg_image = Image.open(os.path.join(IMAGES_DIR, "bus.jpg"))  # Ensure image exists
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

        # Center Frame for Content
        self.frame = tk.Frame(root, bg='white', bd=3, relief="solid")
        self.frame.place(relx=0.5, rely=0.5, anchor="center", width=750, height=550)

        # Title Label
        self.label_welcome = tk.Label(
            self.frame, text="SEAT SURE", font=('Arial', 28, 'bold'),
            bg='white', fg='#00796b',
        )
        self.label_welcome.pack(pady=20)

        # Fetch bus data and create dropdown
        self.display_bus_dropdown()

        # Book Ticket Button
        self.button_book_ticket = tk.Button(
            self.frame, text="Book Ticket", font=('Arial', 24, 'bold'),
            command=self.open_booking_page, bg="#00796b", fg='#ffffff', width=20,
        )
        self.button_book_ticket.pack(pady=10)

        # View My Bookings Button
        self.button_view_bookings = tk.Button(
            self.frame, text="View My Bookings", font=('Arial', 20),
            command=self.view_my_bookings, bg="#4CAF50", fg="white", width=20,
        )
        self.button_view_bookings.pack(pady=10)

        # Logout Button
        self.button_logout = tk.Button(
            self.frame, text="Logout", font=('Arial', 20),
            command=self.logout, bg="#d9534f", fg="white", width=20,
        )
        self.button_logout.pack(pady=10)

    def display_bus_dropdown(self):
        """ Fetch and display bus selection dropdown """
        bus_data = get_bus_data()

        if not bus_data:
            self.bus_var = tk.StringVar(self.frame)
            self.label_bus_data = tk.Label(
                self.frame, text="No buses available", font=('Arial', 20),
                bg='white', fg='#d9534f',
            )
            self.label_bus_data.pack(pady=10)
            return

        self.bus_var = tk.StringVar(self.frame)
        self.bus_var.set(f"{bus_data[0][0]} - {bus_data[0][1]}")  # Set default bus

        self.label_bus_data = tk.Label(
            self.frame, text="Select Bus:", font=('Arial', 22),
            bg='white', fg='#333',
        )
        self.label_bus_data.pack(pady=10)

        self.dropdown_bus = tk.OptionMenu(
            self.frame, self.bus_var,
            *[f"{bus[0]} - {bus[1]}" for bus in bus_data],
        )
        self.dropdown_bus.config(font=('Arial', 20), bg="#555", fg='#ffffff')
        self.dropdown_bus.pack(pady=10)

    def open_booking_page(self):
        """ Open the Booking Page with the selected bus """
        selected_bus = self.bus_var.get()
        if not selected_bus:
            messagebox.showerror("Error", "Please select a bus.")
            return
        self.root.destroy()
        import app
        app.booking_page(self.user_id, selected_bus, app.main_page)

    def view_my_bookings(self):
        """ Open a new window showing the user's bookings with a cancel option """
        bookings = fetch_user_bookings(self.user_id)

        if not bookings:
            if self.bookings_window is not None and self.bookings_window.winfo_exists():
                self.bookings_window.destroy()
            messagebox.showinfo("No Bookings", "You have not booked any tickets yet.")
            return

        # Replace an already-open bookings window
        if self.bookings_window is not None and self.bookings_window.winfo_exists():
            self.bookings_window.destroy()

        bookings_window = tk.Toplevel(self.root)
        bookings_window.title("My Bookings")
        bookings_window.geometry("700x450")
        self.bookings_window = bookings_window

        # Title Label
        label_title = tk.Label(
            bookings_window, text="My Bookings", font=('Arial', 24, 'bold'),
            fg="#00796b",
        )
        label_title.pack(pady=10)

        # Table to Display Bookings
        self.tree = ttk.Treeview(
            bookings_window,
            columns=("ID", "Bus", "Seats", "Time", "Cancel"),
            show="headings", height=10,
        )
        self.tree.heading("ID", text="Booking ID", anchor="center")
        self.tree.heading("Bus", text="Bus Name", anchor="center")
        self.tree.heading("Seats", text="Seats Booked", anchor="center")
        self.tree.heading("Time", text="Booking Time", anchor="center")
        self.tree.heading("Cancel", text="Cancel Booking", anchor="center")

        self.tree.column("ID", width=80, anchor="center")
        self.tree.column("Bus", width=200, anchor="center")
        self.tree.column("Seats", width=120, anchor="center")
        self.tree.column("Time", width=180, anchor="center")
        self.tree.column("Cancel", width=120, anchor="center")

        self.tree.pack(expand=True, fill="both")

        # Insert user bookings into the table
        for booking in bookings:
            self.tree.insert(
                "", "end",
                values=(booking[0], booking[1], booking[2], booking[3], "Cancel"),
            )

        # Cancel Booking Button
        self.button_cancel = tk.Button(
            bookings_window, text="Cancel Selected Booking",
            font=('Arial', 18, 'bold'), bg="#d9534f", fg="white",
            command=self.cancel_selected_booking,
        )
        self.button_cancel.pack(pady=10)

    def cancel_selected_booking(self):
        """ Cancel the selected booking """
        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showerror("Error", "Please select a booking to cancel.")
            return

        booking_id = self.tree.item(selected_item)['values'][0]

        confirm = messagebox.askyesno(
            "Confirm Cancellation", "Are you sure you want to cancel this booking?"
        )
        if confirm:
            success = cancel_booking(booking_id, self.user_id)
            if success:
                messagebox.showinfo("Success", "Booking canceled successfully.")
                self.view_my_bookings()  # Refresh the booking window
            else:
                messagebox.showerror("Error", "Cancellation failed.")

    def logout(self):
        """ Logout the user and return to the Login Page """
        self.root.destroy()
        import app
        app.login_page()
