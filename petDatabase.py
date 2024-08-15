from customtkinter import *
import sqlite3


def inits_db():
    conn = sqlite3.connect('petStore.db')  # Ensure consistent database name
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pets (
        pet_id INTEGER PRIMARY KEY AUTOINCREMENT,
        adopted_pet_img TEXT NOT NULL,
        adopted_pet_name TEXT NOT NULL,
        adopted_pet_type TEXT NOT NULL,
        owner_id INTEGER,
        FOREIGN KEY (owner_id) REFERENCES users (id)
    )
    ''')
    conn.commit()
    conn.close()

def adopted_pet_users( owner_id,image, name, type):
    conn = sqlite3.connect('petStore.db')  # Ensure consistent database name
    cursor = conn.cursor()
    cursor.execute('INSERT INTO pets (adopted_pet_img, adopted_pet_name, adopted_pet_type, owner_id) VALUES (?, ?, ?, ?)', (image,name,type,owner_id))
    conn.commit()
    conn.close()

def getPet_User(id):
    conn = sqlite3.connect('petStore.db')  # Ensure consistent database name
    cursor = conn.cursor()
    cursor.execute("SELECT pet_id, adopted_pet_img, adopted_pet_name, adopted_pet_type FROM pets WHERE owner_id=?",(id,))
    pets = cursor.fetchall()
    conn.close()
    return pets