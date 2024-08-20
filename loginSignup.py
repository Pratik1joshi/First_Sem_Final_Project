from customtkinter import *
from PIL import Image
import sqlite3
from hashlib import sha256
from tkinter import messagebox
  
# Function to initialize the database
def init_db():
    conn = sqlite3.connect('petStore.db')  # Ensure consistent database name
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        phone TEXT NOT NULL,
        fullname TEXT NOT NULL,
        logged_in INTEGER DEFAULT 0
    )
    ''')
    cursor.execute("UPDATE users SET logged_in = 0")
    conn.commit()
    conn.close()

# Function to register a user
def register_user(username, password, phone, fullname):
    hashed_password = sha256(password.encode()).hexdigest()
    try:
        conn = sqlite3.connect('petStore.db')  # Ensure consistent database name
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password, phone, fullname) VALUES (?, ?, ?, ?)', (username, hashed_password, phone, fullname))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def login_user(username, password):
    hashed_password = sha256(password.encode()).hexdigest()
    conn = sqlite3.connect('petStore.db')  # Ensure consistent database name
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, hashed_password))
    user = cursor.fetchone()
    conn.close()
    if user:
        return user  # Return the entire user record
    else:
        return None

# Define global variables for frames
login_frame = None
signup_frame = None

# Function to switch between frames with a basic transition
def switch_frames(current_frame, next_frame):
    # Hide the current frame
    current_frame.pack_forget()
    
    # Show the new frame
    next_frame.pack(expand=True, fill="both")

# Function to switch to the signup page
def show_signup():
    if signup_frame and login_frame:
        switch_frames(login_frame, signup_frame)

# Function to switch to the login page
def show_login():
    if login_frame and signup_frame:
        switch_frames(signup_frame, login_frame)

# Function to display the login/signup window
def show_login_signup_window(app):
    global login_frame, signup_frame  # Declare global variables

    def handle_signup():
        username = signup_username_entry.get()
        password = signup_password_entry.get()
        fullname = signup_fullname_entry.get()
        phone = signup_phone_entry.get()
        if not username:
            messagebox.showerror("Error", "Username is required.")
        elif not password:
            messagebox.showerror("Error", "Password is required.")
        elif not fullname:
            messagebox.showerror("Error", "Full Name is required.")
        elif not phone:
            messagebox.showerror("Error", "Phone is required.")
        elif register_user(username, password, phone, fullname):
            messagebox.showinfo("Success", "User registered successfully!")
        else:
            messagebox.showerror("Error", "Username already exists.")

    def handle_login():
        username = login_username_entry.get()
        password = login_password_entry.get()

        user = login_user(username, password)

        if user:
            conn = sqlite3.connect('petStore.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET logged_in = 1 WHERE id = ?", (user[0],))
            conn.commit()
            conn.close()
            app.update_user_name(user)  # Assuming the 5th field is the fullname
            login_signup_window.destroy()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    # Create a new window for login/signup
    login_signup_window = CTkToplevel(app)
    login_signup_window.geometry("1000x640")  # Adjust window size
    login_signup_window.title("Login/Signup")
    login_signup_window.iconbitmap("logo.ico")

    login_signup_window.transient(app)
    
    # Load images
    side_img_data = Image.open("LOGIN.jpg")
    email_icon_data = Image.open("email-icon.png")
    password_icon_data = Image.open("password-icon.png")
    phone_icon_data = Image.open("phone.png")
    user_icon_data = Image.open("user.png")


    # Create CTkImage instances
    side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(500, 640))
    email_icon = CTkImage(dark_image=email_icon_data, light_image=email_icon_data, size=(20, 20))
    password_icon = CTkImage(dark_image=password_icon_data, light_image=password_icon_data, size=(20, 20))
    phone_icon = CTkImage(dark_image=phone_icon_data, light_image=phone_icon_data, size=(20, 20))
    user_icon = CTkImage(dark_image=user_icon_data, light_image=user_icon_data, size=(20, 20))



    # Create image frame
    image_frame = CTkFrame(master=login_signup_window, width=500, height=640)
    image_frame.pack(side="left", fill="both")
    image_frame.pack_propagate(0)  # Prevent resizing

    # Add image to image frame
    CTkLabel(master=image_frame, text="", image=side_img).pack(expand=True, fill="both")

    # Create login frame
    login_frame = CTkFrame(master=login_signup_window, width=500, height=640, fg_color="#ffffff")
    login_frame.pack_propagate(0)
    login_frame.pack(expand=True, side="right")

    # Add widgets to login frame
    CTkLabel(master=login_frame, text="Welcome Back!", text_color="#601E88", anchor="w", justify="left",
             font=("Arial Bold", 32)).pack(anchor="w", pady=(70, 0), padx=(25, 0))
    CTkLabel(master=login_frame, text="Sign in to your account", text_color="#7E7E7E", anchor="w", justify="left", 
             font=("Arial Bold", 18)).pack(anchor="w", padx=(25, 0))

    CTkLabel(master=login_frame, text="  Username:", text_color="#601E88", anchor="w", justify="left", 
             font=("Arial Bold", 24), image=email_icon, compound="left").pack(anchor="w", pady=(38, 0), padx=(25, 0))
    login_username_entry = CTkEntry(master=login_frame, width=305, height=33, fg_color="#EEEEEE", border_color="#601E88", 
                                    border_width=1, text_color="#000000")
    login_username_entry.pack(anchor="w", padx=(25, 0))

    CTkLabel(master=login_frame, text="  Password:", text_color="#601E88", anchor="w", justify="left", 
             font=("Arial Bold", 24), image=password_icon, compound="left").pack(anchor="w", pady=(21, 0), padx=(25, 0))
    login_password_entry = CTkEntry(master=login_frame, width=305, height=33, fg_color="#EEEEEE", 
                                    border_color="#601E88", border_width=1, text_color="#000000", show="*")
    login_password_entry.pack(anchor="w", padx=(25, 0))

    CTkButton(master=login_frame, command=handle_login, text="Login", fg_color="#601E88", hover_color="#E44982", 
              font=("Arial Bold", 22), text_color="#ffffff", width=305, height=35).pack(anchor="w", pady=(40, 0), padx=(25, 0))
    CTkButton(master=login_frame, text="Don't have an account? Create one", fg_color="#EEEEEE", hover_color="#EEEEEE", 
              font=("Arial Bold", 9), text_color="#601E88", width=305, command=show_signup).pack(anchor="w", pady=(20, 0), padx=(25, 0))

    # Create signup frame
    signup_frame = CTkFrame(master=login_signup_window, width=500, height=640, fg_color="#ffffff")
    signup_frame.pack_propagate(0)

    # Add widgets to signup frame
    CTkLabel(master=signup_frame, text="Hey There!", text_color="#601E88", anchor="w", justify="left", 
             font=("Arial Bold", 32)).pack(anchor="w", pady=(70, 0), padx=(25, 0))
    CTkLabel(master=signup_frame, text="Create your account", text_color="#7E7E7E", anchor="w", justify="left", 
             font=("Arial Bold", 18)).pack(anchor="w", padx=(25, 0))

    CTkLabel(master=signup_frame, text="  FullName:", text_color="#601E88", anchor="w", justify="left", 
             font=("Arial Bold", 24), image=user_icon, compound="left").pack(anchor="w", pady=(38, 0), padx=(25, 0))
    signup_fullname_entry = CTkEntry(master=signup_frame, width=305, height=33, fg_color="#EEEEEE", border_color="#601E88", 
                                     border_width=1, text_color="#000000")
    signup_fullname_entry.pack(anchor="w", padx=(25, 0))

    CTkLabel(master=signup_frame, text="  Mobile:", text_color="#601E88", anchor="w", justify="left", 
             font=("Arial Bold", 24), image=phone_icon, compound="left").pack(anchor="w", pady=(21, 0), padx=(25, 0))
    signup_phone_entry = CTkEntry(master=signup_frame, width=305, height=33, fg_color="#EEEEEE", 
                                  border_color="#601E88", border_width=1, text_color="#000000")
    signup_phone_entry.pack(anchor="w", padx=(25, 0))

    CTkLabel(master=signup_frame, text="  Username  :", text_color="#601E88", anchor="w", justify="left", 
             font=("Arial Bold", 24), image=email_icon, compound="left").pack(anchor="w", pady=(18, 0), padx=(25, 0))
    signup_username_entry = CTkEntry(master=signup_frame, width=305, height=33, fg_color="#EEEEEE", 
                                     border_color="#601E88", border_width=1, text_color="#000000")
    signup_username_entry.pack(anchor="w", padx=(25, 0))

    CTkLabel(master=signup_frame, text="  Password:", text_color="#601E88", anchor="w", justify="left", 
             font=("Arial Bold", 24), image=password_icon, compound="left").pack(anchor="w", pady=(21, 0), padx=(25, 0))
    signup_password_entry = CTkEntry(master=signup_frame, width=305, height=33, fg_color="#EEEEEE", 
                                     border_color="#601E88", border_width=1, text_color="#000000", show="*")
    signup_password_entry.pack(anchor="w", padx=(25, 0))

    CTkButton(master=signup_frame, text="Signup", command=handle_signup, fg_color="#601E88", hover_color="#E44982", 
              font=("Arial Bold", 22), text_color="#ffffff", width=305, height=35).pack(anchor="w", pady=(40, 0), padx=(25, 0))
    CTkButton(master=signup_frame, text="Already have an account? Login", fg_color="#EEEEEE", hover_color="#EEEEEE", 
              font=("Arial Bold", 9), text_color="#601E88", width=305, command=show_login).pack(anchor="w", pady=(20, 0), padx=(25, 0))

    # Initially show the login frame
    show_login()

def get_logged_in_user():
    # Logic to return the currently logged-in user's name
    conn = sqlite3.connect('petStore.db')  # Ensure consistent database name
    cursor = conn.cursor()
    cursor.execute("SELECT fullname FROM users WHERE logged_in = 1")  # Use correct column name
    user = cursor.fetchone()
    conn.close()

    if user:
        return user
    return None
