import os
import sqlite3
from datetime import datetime
from tkinter import messagebox

from core.paths import DB_PATH, DATA_DIR

DB_NAME = DB_PATH


def init_db():
    os.makedirs(DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS buses (
            id INTEGER PRIMARY KEY,
            bus_name TEXT NOT NULL,
            route TEXT NOT NULL,
            available_seats INTEGER NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            name TEXT,
            age INTEGER,
            gender TEXT,
            seats INTEGER,
            bus_id INTEGER,
            booking_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(bus_id) REFERENCES buses(id)
        )
    ''')
    conn.commit()

    # Insert sample bus data (only if buses table is empty)
    cursor.execute('SELECT COUNT(*) FROM buses')
    if cursor.fetchone()[0] == 0:
        buses = [
            ("Red Bus", "Chennai - Bangalore", 20),
            ("Blue Bus", "Chennai - Hyderabad", 20),
            ("Green Bus", "Chennai - Coimbatore", 20),
            ("Yellow Bus", "Chennai - Trichy", 20),
            ("Orange Bus", "Chennai - Madurai", 20),
        ]
        cursor.executemany(
            'INSERT INTO buses (bus_name, route, available_seats) VALUES (?, ?, ?)',
            buses,
        )
        conn.commit()

    conn.close()


def register_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute(
            'INSERT INTO users (username, password) VALUES (?, ?)',
            (username, password),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()
    return True


def login_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        'SELECT id FROM users WHERE username = ? AND password = ?',
        (username, password),
    )
    user = cursor.fetchone()
    conn.close()
    if user:
        return user[0]
    return None


def fetch_all_users():
    """ Fetch all registered users from the database """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM users")
    users = cursor.fetchall()
    conn.close()
    return users


def fetch_all_reservations():
    """ Fetch all booked tickets along with user, bus, seats, and booking time """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT reservations.id, users.username, buses.bus_name,
               reservations.seats, reservations.booking_time
        FROM reservations
        JOIN users ON reservations.user_id = users.id
        JOIN buses ON reservations.bus_id = buses.id
        ORDER BY reservations.booking_time DESC
    """)
    reservations = cursor.fetchall()
    conn.close()
    return reservations


def get_ticket_summary():
    """ Get the total number of tickets booked for each bus """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT buses.bus_name, SUM(reservations.seats) AS total_tickets
        FROM reservations
        JOIN buses ON reservations.bus_id = buses.id
        GROUP BY buses.bus_name
    """)
    summary = cursor.fetchall()
    conn.close()
    return summary


def book_ticket(user_id, name, age, gender, seats, selected_bus):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        # Get bus ID and available seats
        parts = selected_bus.split(" - ", 1)
        bus_name = parts[0]
        route = parts[1]

        cursor.execute(
            'SELECT id, available_seats FROM buses WHERE bus_name = ? AND route = ?',
            (bus_name, route),
        )
        bus_data = cursor.fetchone()

        if not bus_data:
            messagebox.showerror("Error", "Selected bus not found.")
            conn.close()
            return False

        bus_id, available_seats = bus_data
        if available_seats < int(seats):
            messagebox.showerror("Error", "Not enough seats available.")
            conn.close()
            return False

        # Insert booking with current timestamp
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('''
            INSERT INTO reservations (user_id, name, age, gender, seats, bus_id, booking_time)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, name, age, gender, int(seats), bus_id, current_time))

        # Update available seats in buses table
        cursor.execute('''
            UPDATE buses SET available_seats = available_seats - ? WHERE id = ?
        ''', (int(seats), bus_id))

        conn.commit()
        messagebox.showinfo(
            "Success",
            f"Ticket booked successfully for {bus_name} with {seats} seat(s)!\n"
            f"Booked at: {current_time}",
        )
        conn.close()
        return True

    except Exception as e:
        messagebox.showerror("Error", f"Booking failed: {str(e)}")
        conn.rollback()
        conn.close()
        return False


def get_bus_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT bus_name, route FROM buses')
    buses = cursor.fetchall()
    conn.close()
    return buses


def fetch_user_bookings(user_id):
    """ Fetch all bookings for a specific user """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT reservations.id, buses.bus_name, reservations.seats, reservations.booking_time
        FROM reservations
        JOIN buses ON reservations.bus_id = buses.id
        WHERE reservations.user_id = ?
        ORDER BY reservations.booking_time DESC
    """, (user_id,))
    bookings = cursor.fetchall()
    conn.close()
    return bookings


def cancel_booking(booking_id, user_id):
    """ Cancel a booking and update available seats """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Fetch the number of seats and bus ID from the booking
    cursor.execute(
        "SELECT seats, bus_id FROM reservations WHERE id = ? AND user_id = ?",
        (booking_id, user_id),
    )
    booking = cursor.fetchone()

    if not booking:
        conn.close()
        return False  # Booking not found

    seats, bus_id = booking

    # Delete the booking
    cursor.execute(
        "DELETE FROM reservations WHERE id = ? AND user_id = ?",
        (booking_id, user_id),
    )

    # Give the seats back to the bus
    cursor.execute(
        "UPDATE buses SET available_seats = available_seats + ? WHERE id = ?",
        (seats, bus_id),
    )

    conn.commit()
    conn.close()
    return True
