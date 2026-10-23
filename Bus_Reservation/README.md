# SEAT SURE – Bus Reservation Software

A desktop bus ticket booking system built with **Python, Tkinter and SQLite**.
Mini project – B.Sc. Computer Science, The New College (Autonomous), Chennai – March 2025.

## Features

**Passengers**
- Register and log in
- Choose a bus/route and book seats (name, age, gender, seat count)
- Live seat availability (seats are deducted on booking)
- View booking history and cancel a booking (seats are returned)

**Admin**
- Admin login
- Dashboard with tabs: Registered Users, Tickets Booked, Ticket Summary (per bus)

## Project structure

```
seat_sure/
├── app.py                  # entry point + page navigation
├── requirements.txt
├── README.md
├── core/
│   ├── database.py         # SQLite helpers (users, buses, reservations)
│   └── paths.py            # image / database locations
├── pages/
│   ├── register.py         # Register page
│   ├── login.py            # User login page
│   ├── main_page.py        # Bus selection, My Bookings, Cancel
│   ├── booking_page.py     # Book Your Seat form
│   ├── admin_login.py      # Admin login page
│   └── admin_main_page.py  # Admin dashboard
├── assets/images/
│   ├── bus.jpg             # background (replace with your own)
│   └── back.jpg            # admin background (replace with your own)
└── data/                   # bus_reservation.db is created here on first run
```

## Run

```bash
pip install -r requirements.txt
python app.py
```

Tkinter ships with Python on Windows/macOS. On Debian/Ubuntu: `sudo apt install python3-tk`.
Pages open fullscreen – press **Esc** to leave fullscreen.
The database `data/bus_reservation.db` is created automatically on first run with 5 sample buses.

## Admin credentials (demo)

| Username | Password   |
|----------|------------|
| admin    | admin123   |

> Demo project: passwords are stored as plain text and the admin login is hard-coded.
> Hash passwords (e.g. `hashlib`/`bcrypt`) before any real use.

## Tech

Python 3 · Tkinter · Pillow · SQLite3
