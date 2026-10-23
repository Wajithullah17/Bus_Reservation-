import tkinter as tk
from tkinter import messagebox

from core.database import book_ticket


class BookingPage:
    def __init__(self, root, user_id, selected_bus, main_page_callback):
        self.root = root
        self.root.title("Bus Reservation System - Booking Page")
        self.root.attributes('-fullscreen', True)
        self.user_id = user_id
        self.selected_bus = selected_bus
        self.main_page_callback = main_page_callback

        # Center Frame
        self.frame = tk.Frame(root, bg='white', bd=3, relief="solid")
        self.frame.place(relx=0.5, rely=0.5, anchor="center", width=700, height=550)

        # Title Label
        self.label_title = tk.Label(
            self.frame, text="Book Your Seat", font=('Arial', 32, 'bold'),
            bg='white', fg='#00796b',
        )
        self.label_title.grid(row=0, column=0, columnspan=2, pady=20)

        # Selected Bus Label
        self.label_selected_bus = tk.Label(
            self.frame, text=f"Bus: {self.selected_bus}", font=('Arial', 24),
            bg='white', fg='#333',
        )
        self.label_selected_bus.grid(row=1, column=0, columnspan=2, pady=10)

        # Name Entry
        self.label_name = tk.Label(
            self.frame, text="Name:", font=('Arial', 22), bg='white', fg='#333'
        )
        self.label_name.grid(row=2, column=0, pady=10, padx=10, sticky="e")
        self.entry_name = tk.Entry(self.frame, font=('Arial', 22), width=18)
        self.entry_name.grid(row=2, column=1, pady=10, padx=10, sticky="w")

        # Age Entry
        self.label_age = tk.Label(
            self.frame, text="Age:", font=('Arial', 22), bg='white', fg='#333'
        )
        self.label_age.grid(row=3, column=0, pady=10, padx=10, sticky="e")
        self.entry_age = tk.Entry(self.frame, font=('Arial', 22), width=18)
        self.entry_age.grid(row=3, column=1, pady=10, padx=10, sticky="w")

        # Gender Dropdown
        self.label_gender = tk.Label(
            self.frame, text="Gender:", font=('Arial', 22), bg='white', fg='#333'
        )
        self.label_gender.grid(row=4, column=0, pady=10, padx=10, sticky="e")
        self.gender_var = tk.StringVar(self.frame)
        self.gender_var.set("Male")
        self.dropdown_gender = tk.OptionMenu(
            self.frame, self.gender_var, "Male", "Female"
        )
        self.dropdown_gender.config(
            font=('Arial', 20), bg='#00796b', fg='#ffffff', width=15
        )
        self.dropdown_gender.grid(row=4, column=1, pady=10, padx=10, sticky="w")

        # Seats Entry
        self.label_seats = tk.Label(
            self.frame, text="Seats:", font=('Arial', 22), bg='white', fg='#333'
        )
        self.label_seats.grid(row=5, column=0, pady=10, padx=10, sticky="e")
        self.entry_seats = tk.Entry(self.frame, font=('Arial', 22), width=18)
        self.entry_seats.grid(row=5, column=1, pady=10, padx=10, sticky="w")

        # Book Button
        self.button_book = tk.Button(
            self.frame, text="Book Now", font=('Arial', 24, 'bold'),
            command=self.book_ticket, bg='#00796b', fg='#ffffff', width=15,
        )
        self.button_book.grid(row=6, column=0, columnspan=2, pady=10)

        # Back Button
        self.button_back = tk.Button(
            self.frame, text="Back", font=('Arial', 16),
            command=self.go_back, bg='#555555', fg='#ffffff', width=10,
        )
        self.button_back.grid(row=7, column=0, columnspan=2, pady=5)

    def book_ticket(self):
        name = self.entry_name.get().strip()
        age = self.entry_age.get().strip()
        gender = self.gender_var.get()
        seats = self.entry_seats.get().strip()

        if not name or not age or not gender or not seats:
            messagebox.showerror("Error", "Please fill all fields.")
            return

        try:
            age = int(age)
            seats = int(seats)
            if age <= 0 or seats <= 0:
                messagebox.showerror("Error", "Age and Seats must be positive numbers.")
                return
        except ValueError:
            messagebox.showerror("Error", "Age and Seats must be valid numbers.")
            return

        # database.book_ticket shows its own success / error messages
        success = book_ticket(self.user_id, name, age, gender, seats, self.selected_bus)

        if success:
            self.root.destroy()
            self.main_page_callback(self.user_id)

    def go_back(self):
        self.root.destroy()
        self.main_page_callback(self.user_id)
