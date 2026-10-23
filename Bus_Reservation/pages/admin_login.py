import tkinter as tk
from tkinter import messagebox


class AdminLoginPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Bus Reservation System - Admin Login")
        self.root.attributes('-fullscreen', True)  # Full screen
        self.root.configure(bg='#e0f7fa')  # Background color

        # Center Frame
        self.frame = tk.Frame(root, bg='#e0f7fa')
        self.frame.place(relx=0.5, rely=0.5, anchor='center')

        # Labels
        self.label_username = tk.Label(
            self.frame, text="Admin Username", font=('Arial', 28),
            bg='#e0f7fa', fg='#00796b',
        )
        self.label_username.grid(row=0, column=0, pady=10, padx=20)

        self.label_password = tk.Label(
            self.frame, text="Password", font=('Arial', 28),
            bg='#e0f7fa', fg='#00796b',
        )
        self.label_password.grid(row=1, column=0, pady=10, padx=20)

        # Entries
        self.entry_username = tk.Entry(self.frame, font=('Arial', 28))
        self.entry_username.grid(row=0, column=1, pady=10, padx=20)

        self.entry_password = tk.Entry(self.frame, show='*', font=('Arial', 28))
        self.entry_password.grid(row=1, column=1, pady=10, padx=20)

        # Login Button
        self.button_login = tk.Button(
            self.frame, text="Login", font=('Arial', 28),
            command=self.admin_login, bg='#00796b', fg='#ffffff',
        )
        self.button_login.grid(row=2, column=1, pady=20, padx=20)

        # Back Button
        self.button_back = tk.Button(
            self.frame, text="Back", font=('Arial', 20),
            command=self.go_back, bg='#555555', fg='#ffffff',
        )
        self.button_back.grid(row=2, column=0, pady=20, padx=20)

    def admin_login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if username == "admin" and password == "admin123":
            messagebox.showinfo("Success", "Admin login successful!")
            self.root.destroy()
            import app
            app.admin_main_page()
        else:
            messagebox.showerror("Error", "Invalid admin credentials")

    def go_back(self):
        self.root.destroy()
        import app
        app.login_page()
