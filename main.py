import customtkinter as ctk
import tkinter as tk
from loginSignup import show_login_signup_window, init_db, get_logged_in_user  # Importing the function from the login/signup file
from petDatabase import getPet_User, inits_db, adopted_pet_users
from PIL import Image, ImageTk
import os
import sqlite3

# Initializing the main window
class MainApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("1000x690")
        self.title("Pet Store")
        init_db()
        inits_db()
        self.logged_in_user = get_logged_in_user()
        self.init_ui()
        # self.adopted_pets_details = adopted_pets_user()

    def init_ui(self):
        # Create a frame for the navbar with a specific background color
        navbar = ctk.CTkFrame(self, height=50, corner_radius=0, fg_color="#aac2e3")
        navbar.pack(side="top", fill="x")  # Add top and bottom padding for the navbar

        # Add the logo to the navbar
        logo = ctk.CTkLabel(navbar, text="Logo", font=("Arial", 18, "bold"), fg_color="#aac2e3", text_color="black")
        logo.place(x=90, y=10)  # Place the logo at specific coordinates

        # Create a function to handle button clicks
        def button_click(action):
            print(f"{action} button clicked")

        # Add buttons to the navbar with black text color
        button_about = ctk.CTkButton(navbar, width=80, text="Home", command=lambda: self.show_hero(), fg_color="#aac2e3", text_color="black")
        button_about.place(x=270, y=10)  # Place the button at specific coordinates

        button_ourworks = ctk.CTkButton(navbar, width=100, text="About Us", command=lambda: button_click("About Us"), fg_color="#aac2e3", text_color="black")
        button_ourworks.place(x=350, y=10)  # Place the button at specific coordinates

        button_adopt = ctk.CTkButton(navbar, width=100, text="Adopt Animals", command=lambda: button_click("Adopt Animals"), fg_color="#aac2e3", text_color="black")
        button_adopt.place(x=450, y=10)  # Place the button at specific coordinates

        button_contact = ctk.CTkButton(navbar, width=100, text="Contact", command=lambda: button_click("Contact"), fg_color="#aac2e3", text_color="black")
        button_contact.place(x=550, y=10)  # Place the button at specific coordinates

        # Add login/signup button to the navbar with specified background color
        self.button_login_signup = ctk.CTkButton(navbar, text="Login/Signup", command=self.show_login_signup, fg_color="#ff7a59", text_color="black")
        self.button_login_signup.place(relx=1.0, x=-100, y=10, anchor="ne")  # Place the button at specific coordinates

        # Load background image  
        bg_image_data = Image.open("mainBackground.png")
        bg_image = ctk.CTkImage(dark_image=bg_image_data, light_image=bg_image_data, size=(1000, 640))

        # Create a frame for the background image
        self.bg_frame = ctk.CTkFrame(self, width=1000, height=640)
        self.bg_frame.pack(fill="both", expand=True)
        self.bg_frame.pack_propagate(0)  # Prevent resizing

        # Add the background image to the frame
        bg_label = ctk.CTkLabel(self.bg_frame,text="", image=bg_image)
        bg_label.pack(fill="both", expand=True)

        # Create and place the "Explore More" button
        explore_button = ctk.CTkButton(
            self, 
            text="Explore More", 
            command=self.show_explore_more, 
            fg_color="#ff7a59", 
            text_color="white", 
            font=("Arial", 16),
            width=200, 
            height=40
        )

        explore_button.place(relx=0.5, rely=0.9, anchor="center")

        if self.logged_in_user:
            self.button_login_signup.configure(text=self.logged_in_user[4], command=self.logout)
        else:
            self.button_login_signup.configure(text="Login/Signup", command=self.show_login_signup)

        self.main_frame = ctk.CTkScrollableFrame(self)
        self.main_frame.pack(fill="both", expand=True)

    def update_user_name(self, name):
        self.logged_in_user = name
        self.button_login_signup.configure(text=name[4], command=self.show_logout_options)

    def show_home(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        ctk.CTkLabel(self.main_frame, text="Welcome to the Pet Store!").pack(pady=20)

    # def show_logout_options(self):
    #     try:
    #         self.category_frame.pack_forget()
    #     except:
    #         print("Done")
    #     try:
    #         self.bg_frame.pack_forget()
    #     except:
    #         print("Done")

    #     # Clear the main frame
    #     for widget in self.main_frame.winfo_children():
    #         widget.destroy()

    #     # Show a popup window with options for logout
    #     self.dropdown = ctk.CTkFrame(self.main_frame, width=1000, height=640)
    #     self.dropdown.pack(fill="both", expand=True, pady=20, padx=20)
    #     self.dropdown.pack_propagate(0)  # Prevent resizing

    #     # Ensure the grid system has enough columns
    #     self.dropdown.grid_columnconfigure(0, weight=1)
    #     self.dropdown.grid_columnconfigure(1, weight=1)
    #     self.dropdown.grid_columnconfigure(2, weight=1)
    #     self.dropdown.grid_columnconfigure(3, weight=1)
    #     self.dropdown.grid_columnconfigure(4, weight=1)
    #     self.dropdown.grid_columnconfigure(5, weight=1)

    #     # Add labels and buttons to the frame
    #     username_label = ctk.CTkLabel(self.dropdown, text="Username:")
    #     username_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    #     user_username_label = ctk.CTkLabel(self.dropdown, text=self.logged_in_user[1])
    #     user_username_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    #     phone_label = ctk.CTkLabel(self.dropdown, text="Phone:")
    #     phone_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    #     user_phone_label = ctk.CTkLabel(self.dropdown, text=self.logged_in_user[3])
    #     user_phone_label.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    #     address_label = ctk.CTkLabel(self.dropdown, text="Address:")
    #     address_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
    #     user_address_label = ctk.CTkLabel(self.dropdown, text="-")
    #     user_address_label.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    #     name_label = ctk.CTkLabel(self.dropdown, text="Name:")
    #     name_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
    #     user_name_label = ctk.CTkLabel(self.dropdown, text=self.logged_in_user[4])
    #     user_name_label.grid(row=3, column=1, padx=5, pady=5, sticky="w")

    #     # Add buttons to the frame
    #     edit_button = ctk.CTkButton(self.dropdown, text="Edit", command=self.edit_account)
    #     edit_button.grid(row=4, column=0, padx=5, pady=5, sticky="w")

    #     logout_button = ctk.CTkButton(self.dropdown, text="Logout", command=self.logout)
    #     logout_button.grid(row=5, column=0, padx=5, pady=5, sticky="w")

    #     delete_account_button = ctk.CTkButton(self.dropdown, text="Delete Account", command=self.remove_account)
    #     delete_account_button.grid(row=6, column=0, padx=5, pady=5, sticky="w")

    #     # Place the adopted_frame in the rightmost column and span 6 rows
    #     adopted_frame = ctk.CTkScrollableFrame(self.dropdown, width=350, height=640)
    #     adopted_frame.grid(row=0, column=5, rowspan=7, sticky="ne", padx=10, pady=10)

    #     print(self.logged_in_user[0],"--------------------------------")

    #     adopted = getPet_User(self.logged_in_user[0])
        
    #     adopt_label = ctk.CTkLabel(adopted_frame, text="Adopted Pets", font=("Arial", 24))
    #     adopt_label.grid(row=0,column=0,padx=10, pady=0)

    #     if adopted:
    #         j=1
    #         for i in adopted :
    #             new_adopt_frame= ctk.CTkFrame(adopted_frame, width=300,height=250)
    #             new_adopt_frame.grid(row=j, column=0, padx=10, pady=20, sticky="n")
    #             # Load the image
    #             images_folder = "pets_picture"

    #             image_path = os.path.join(images_folder, i[1])

    #             img_data = Image.open(image_path)
    #             img_data = img_data.resize((200, 200), Image.LANCZOS)  # Resize image to fit the layout
    #             img_tk = ImageTk.PhotoImage(img_data)

    #             # Image Label - Positioned on the left side
    #             img_label = ctk.CTkLabel(new_adopt_frame, image=img_tk, text="")
    #             img_label.image = img_tk  # Keep a reference to avoid garbage collection
    #             img_label.grid(row=0, column=0,rowspan=3, padx=10, pady=10, sticky="w")

    #             # Details Label - Positioned closer to the image
    #             details_label = ctk.CTkLabel(new_adopt_frame, text=i[2], font=("Arial", 14))
    #             details_label.grid(row=0, column=1, padx=(30, 10), pady=20, sticky="nw")
    #             remove_pet_button = ctk.CTkButton(new_adopt_frame, text="Remove", font=("Arial",18),command=lambda id=i[0]: self.remove_pet_adopted(id))
    #             remove_pet_button.grid(row=3,column=1,padx=10,pady=10, sticky="w")
    #             j+=1


        
    # def remove_pet_adopted(self,id):
    #     conn = sqlite3.connect('petStore.db')
    #     cursor = conn.cursor()
    #     cursor.execute("DELETE FROM pets WHERE pet_id =?", (id,))
    #     conn.commit()
    #     conn.close()
    #     print("Pet removed from adopted list")

        
    def show_logout_options(self):
        # Hide previous frames
        try:
            self.category_frame.pack_forget()
        except:
            print("Done")
        try:
            self.bg_frame.pack_forget()
        except:
            print("Done")

        # Clear the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Show a popup window with options for logout
        self.dropdown = ctk.CTkFrame(self.main_frame, width=1000, height=640)
        self.dropdown.pack(fill="both", expand=True, pady=20, padx=20)
        self.dropdown.pack_propagate(0)  # Prevent resizing

        # Ensure the grid system has enough columns
        for i in range(6):
            self.dropdown.grid_columnconfigure(i, weight=1)

        # Add labels and buttons to the frame
        self.create_labels_and_buttons()

        # Add adopted pets frame
        self.adopted_frame = ctk.CTkScrollableFrame(self.dropdown, width=350, height=640)
        self.adopted_frame.grid(row=0, column=5, rowspan=7, sticky="ne", padx=10, pady=10)

        self.update_adopted_pets()

    def create_labels_and_buttons(self):
        username_label = ctk.CTkLabel(self.dropdown, text="Username:")
        username_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        user_username_label = ctk.CTkLabel(self.dropdown, text=self.logged_in_user[1])
        user_username_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        phone_label = ctk.CTkLabel(self.dropdown, text="Phone:")
        phone_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        user_phone_label = ctk.CTkLabel(self.dropdown, text=self.logged_in_user[3])
        user_phone_label.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        address_label = ctk.CTkLabel(self.dropdown, text="Address:")
        address_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        user_address_label = ctk.CTkLabel(self.dropdown, text="-")
        user_address_label.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        name_label = ctk.CTkLabel(self.dropdown, text="Name:")
        name_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        user_name_label = ctk.CTkLabel(self.dropdown, text=self.logged_in_user[4])
        user_name_label.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Add buttons to the frame
        edit_button = ctk.CTkButton(self.dropdown, text="Edit", command=self.edit_account)
        edit_button.grid(row=4, column=0, padx=5, pady=5, sticky="w")

        logout_button = ctk.CTkButton(self.dropdown, text="Logout", command=self.logout)
        logout_button.grid(row=5, column=0, padx=5, pady=5, sticky="w")

        delete_account_button = ctk.CTkButton(self.dropdown, text="Delete Account", command=self.remove_account)
        delete_account_button.grid(row=6, column=0, padx=5, pady=5, sticky="w")

        # Place the adopted_frame in the rightmost column and span 6 rows
        adopted_frame = ctk.CTkScrollableFrame(self.dropdown, width=350, height=640)
        adopted_frame.grid(row=0, column=5, rowspan=7, sticky="ne", padx=10, pady=10)

    def update_adopted_pets(self):
        # Clear existing adopted pets if any
        for widget in self.adopted_frame.winfo_children():
            widget.destroy()

        # Fetch adopted pets
        adopted = getPet_User(self.logged_in_user[0])

        adopt_label = ctk.CTkLabel(self.adopted_frame, text="Adopted Pets", font=("Arial", 24))
        adopt_label.grid(row=0, column=0, padx=10, pady=0)

        if adopted:
            j = 1
            for i in adopted:
                new_adopt_frame = ctk.CTkFrame(self.adopted_frame, width=300, height=250)
                new_adopt_frame.grid(row=j, column=0, padx=10, pady=20, sticky="n")
                
                # Load the image
                images_folder = "pets_picture"
                image_path = os.path.join(images_folder, i[1])

                img_data = Image.open(image_path)
                img_data = img_data.resize((200, 200), Image.LANCZOS)  # Resize image to fit the layout
                img_tk = ImageTk.PhotoImage(img_data)

                # Image Label - Positioned on the left side
                img_label = ctk.CTkLabel(new_adopt_frame, image=img_tk, text="")
                img_label.image = img_tk  # Keep a reference to avoid garbage collection
                img_label.grid(row=0, column=0, rowspan=3, padx=10, pady=10, sticky="w")

                # Details Label - Positioned closer to the image
                details_label = ctk.CTkLabel(new_adopt_frame, text=i[2], font=("Arial", 14))
                details_label.grid(row=0, column=1, padx=(30, 10), pady=20, sticky="nw")
                
                remove_pet_button = ctk.CTkButton(new_adopt_frame, text="Remove", font=("Arial", 18),
                                                  command=lambda id=i[0]: self.remove_pet_adopted(id))
                remove_pet_button.grid(row=3, column=1, padx=10, pady=10, sticky="w")
                
                j += 1

    def remove_pet_adopted(self, id):
        conn = sqlite3.connect('petStore.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM pets WHERE pet_id=?", (id,))
        conn.commit()
        conn.close()
        print("Pet removed from adopted list")

        # Update the UI to reflect the removal
        self.update_adopted_pets()

    def getPet_User(id):
        conn = sqlite3.connect('petStore.db')
        cursor = conn.cursor()
        cursor.execute("SELECT pet_id, adopted_pet_img, adopted_pet_name, adopted_pet_type FROM pets WHERE owner_id=?", (id,))
        pets = cursor.fetchall()
        conn.close()
        return pets

    def show_login_signup(self):
        show_login_signup_window(self)

    def logout(self):
        self.show_hero()


        conn = sqlite3.connect('petStore.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET logged_in = 0 WHERE fullname = ?", (self.logged_in_user[4],))
        conn.commit()
        conn.close()
        self.logged_in_user = None
        self.button_login_signup.configure(text="Login/Signup", command=self.show_login_signup)
        print("Logged out")

    def remove_account(self):
        self.show_hero()
        conn = sqlite3.connect('petStore.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE fullname =?", (self.logged_in_user[4],))
        conn.commit()
        conn.close()
        self.logged_in_user = None
        self.button_login_signup.configure(text="Login/Signup", command=self.show_login_signup)
        print("Account deleted")

    def edit_account(self):
        edit_frame = ctk.CTkFrame(self.dropdown, width=400, height=400)
        edit_frame.grid(row=4, column=1, padx=10, pady=10)
        edit_frame.pack_propagate(0)

        new_username_label = ctk.CTkLabel(edit_frame, text="New Username:")
        new_username_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        new_username_entry = ctk.CTkEntry(edit_frame, width=200)
        new_username_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        new_phone_label = ctk.CTkLabel(edit_frame, text="New Phone:")
        new_phone_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        new_phone_entry = ctk.CTkEntry(edit_frame, width=200)
        new_phone_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        new_name_label = ctk.CTkLabel(edit_frame, text="New Name:")
        new_name_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        new_name_entry = ctk.CTkEntry(edit_frame, width=200)
        new_name_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # Save button to update the user's information
        # self.old_username=self.logged_in_user[1]
        # self.old_phone = self.logged_in_user[3]
        # self.old_name = self.logged_in_user[4]
        save_button = ctk.CTkButton(edit_frame, text="Save", command=lambda: self.save_edits(new_username_entry.get(), new_phone_entry.get(), new_name_entry.get()))
        save_button.grid(row=3, column=0, padx=10, pady=10)

        cancel_button = ctk.CTkButton(edit_frame, text="Cancel", command=self.show_logout_options)
        cancel_button.grid(row=3, column=1, padx=10, pady=10)

    def save_edits(self, new_username, new_phone, new_name):
        conn = sqlite3.connect('petStore.db')
        cursor = conn.cursor()
        # Check if new_username is provided; if not, use the old username
        final_username = new_username if new_username else self.logged_in_user[1]

        # Check if new_phone is provided; if not, use the old phone
        final_phone = new_phone if new_phone else self.logged_in_user[3]

        # Check if new_name is provided; if not, use the old name
        final_name = new_name if new_name else self.logged_in_user[4]

        # Now, update the database with the final values
        cursor.execute("UPDATE users SET username = ?, phone = ?, fullname = ? WHERE fullname = ?", 
                    (final_username, final_phone, final_name, self.logged_in_user[4]))
        conn.commit()
        conn.close()
        self.logged_in_user = (self.logged_in_user[0], final_username, self.logged_in_user[2], final_phone, final_name, self.logged_in_user[5])
        self.update_user_name(self.logged_in_user)
        self.show_logout_options()
        print("Account edited successfully")

    def show_hero(self):
        try:
            self.category_frame.pack_forget()
        except:
            print("Done")
        try:
            self.dropdown.pack_forget()
        except:
            print("Done")
         # Clear the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Load background image  
        bg_image_data = Image.open("mainBackground.png")
        bg_image = ctk.CTkImage(dark_image=bg_image_data, light_image=bg_image_data, size=(1000, 640))

        # Create a frame for the background image
        self.bg_frame = ctk.CTkFrame(self.main_frame, width=1000, height=640)
        self.bg_frame.pack(fill="both", expand=True)
        self.bg_frame.pack_propagate(0)  # Prevent resizing

        # Add the background image to the frame
        bg_label = ctk.CTkLabel(self.bg_frame,text="", image=bg_image)
        bg_label.pack(fill="both", expand=True)

        # Create and place the "Explore More" button
        explore_button = ctk.CTkButton(
            self.main_frame, 
            text="Explore More", 
            command=self.show_explore_more, 
            fg_color="#ff7a59", 
            text_color="white", 
            font=("Arial", 16),
            width=200, 
            height=40
        )

        explore_button.place(relx=0.5, rely=0.9, anchor="center")
        

    def show_explore_more(self):
        # Remove or hide the background frame
        self.bg_frame.pack_forget()

        # Clear the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        # for widget in self.bg_frame.winfo_children():
        #     widget.destroy()

        images_folder = "pets_picture"

        # Sample images for each category (replace these with your actual image paths)
        category_images = {
            "Dogs": "dog_background.jpg",
            "Cats": "cat_background.jpg",
            "Birds": "birds_background.jpeg",
            "Fish": "fish_background.jpg"
        }

        categories = list(category_images.keys())

        for i, category in enumerate(categories):
            self.category_frame = ctk.CTkFrame(self.main_frame, corner_radius=10, fg_color="#343a40")
            self.category_frame.grid(row=i//2, column=i%2, padx=20, pady=10, ipadx=10, ipady=10, sticky="nsew")

            # Construct the full path to the image
            image_path = os.path.join(images_folder, category_images[category])

            # Load and resize the image using PIL
            img_data = Image.open(image_path)
            img_data = img_data.resize((500, 290), Image.LANCZOS)  # Resize to 200x200 pixels
            img_tk = ImageTk.PhotoImage(img_data)  # Convert the image to PhotoImage

            # Add a label with the image
            img_label = ctk.CTkLabel(self.category_frame, image=img_tk, text="")
            img_label.image = img_tk  # Keep a reference to avoid garbage collection
            img_label.pack(padx=10, pady=10, fill="both", expand=True)

            # Add a label with the category name
            label = ctk.CTkButton(self.category_frame, text=category, font=("Arial", 16, "bold"), text_color="black", command=lambda t=category: self.inside_categories(t))
            label.pack(padx=10, pady=10)

        # Configure grid to make sure frames are positioned nicely
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
            
    def inside_categories(self,category): 
        try:
            self.category_frame.pack_forget()
            for widget in self.main_frame.winfo_children():
                widget.destroy()
        except:
            print("Done")
        try:
            self.pet_details_frame.pack_forget()
            for widget in self.pet_details_frame.winfo_children():
                widget.destroy()
        except:
            print("Done")
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        back_button = ctk.CTkButton(self.main_frame, text="<",command=self.show_explore_more, fg_color="#ff7a59", text_color="white", height=20,width=20)
        back_button.grid(row=0, column=0, padx=0, pady=0, sticky="nw")

        images_folder = "pets_picture"

        inside_dog_categories = {"Husky":"husky.jpeg", 
                                "German Shepherd":"german.jpeg", "Bulldog":"buldog.jpg", 
                                "Golden Retriever":"Golden-Retriever.jpeg","Rottweiler":"rottweiler.jpeg","Alaskan Malamute":"alaskan_malamute.jpg"}
        inside_cat_categories = {"Bombay":"bombay.jpg", "Persian":"persian.jpg", "Norwegian Forest":"Norwegian-Forest-Cat.jpg",
                                 "Ragdoll":"ragdoll.jpg","American Bobtail":"american_bobtail.jpg","Britist Shorthair":"british_shorthair.jpg"}
        inside_bird_categories = {
                                    "Parrot": "parrot.jpg",
                                    "Canary": "canary.jpg",
                                    "Finch": "finch.jpeg",
                                    "Cockatiel": "cockatiel.jpeg",
                                    "Lovebird": "lovebirds.jpg",
                                    "Budgerigar": "budgerigar.jpg"
                                }
        inside_fish_categories = {
                                    "Betta": "betta.jpg",
                                    "Goldfish": "goldfish.jpeg",
                                    "Guppy": "guppy.jpg",
                                    "Angelfish": "angelfish.jpg",
                                    "Neon Tetra": "neon_tetra.webp",
                                    "Molly": "molly.jpg"
                                }

        # print(category)
        
        if category == "Dogs":
            pet_categories = inside_dog_categories
        elif category == "Cats":
            pet_categories = inside_cat_categories
        elif category == "Birds":
            pet_categories = inside_bird_categories
        elif category == "Fish":
            pet_categories = inside_fish_categories

        for i, pet in enumerate(pet_categories.keys()):
            self.category_frame = ctk.CTkFrame(self.main_frame, corner_radius=10, fg_color="#343a40")
            self.category_frame.grid(row=i//2, column=i%2, padx=20, pady=10, ipadx=10, ipady=10, sticky="nsew")

            # Construct the full path to the image
            image_path = os.path.join(images_folder, pet_categories[pet])

            # Load and resize the image using PIL
            img_data = Image.open(image_path)
            img_data = img_data.resize((500, 290), Image.LANCZOS)
            img_tk = ImageTk.PhotoImage(img_data)

            # Add a label with the image
            img_label = ctk.CTkLabel(self.category_frame, image=img_tk, text="")
            img_label.image = img_tk  # Keep a reference to avoid garbage collection
            img_label.pack(padx=10, pady=10, fill="both", expand=True)

            # Add a button with the pet name, and a command to show details
            pet_button = ctk.CTkButton(self.category_frame, text=pet, font=("Arial", 16, "bold"), text_color="black", command=lambda p=pet,c=category,imgPet = pet_categories[pet]: self.show_pet_details(p,c,imgPet))
            pet_button.pack(padx=10, pady=10)
        
        # Configure grid to make sure frames are positioned nicely
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
 
    def show_pet_details(self, pet_name, category, imge):
        # Clear the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Create a new frame for pet details
        self.pet_details_frame = ctk.CTkFrame(self.main_frame, corner_radius=10, fg_color="#343a40")
        self.pet_details_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")

        # Configure the grid to manage layout
        self.main_frame.grid_rowconfigure(0, weight=0)  # For back button
        self.main_frame.grid_rowconfigure(1, weight=1)  # For pet details
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=0)

        # Back Button - Positioned at the top, spanning across two columns
        back_button = ctk.CTkButton(self.main_frame, text="< Back", command=lambda: self.inside_categories(category), fg_color="#ff7a59", text_color="white")
        back_button.grid(row=0, column=0, columnspan=2, pady=10, sticky="nw")

        # Load the image
        images_folder = "pets_picture"
        image_path = os.path.join(images_folder, imge)

        img_data = Image.open(image_path)
        img_data = img_data.resize((500, 400), Image.LANCZOS)  # Resize image to fit the layout
        img_tk = ImageTk.PhotoImage(img_data)

        # Image Label - Positioned on the left side
        img_label = ctk.CTkLabel(self.pet_details_frame, image=img_tk, text="")
        img_label.image = img_tk  # Keep a reference to avoid garbage collection
        img_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Details Label - Positioned closer to the image
        details_label = ctk.CTkLabel(self.pet_details_frame, text=f"Details about {pet_name}", font=("Arial", 24))
        details_label.grid(row=0, column=1, padx=(30, 10), pady=20, sticky="nw")

        # Additional details can be added below the main details
        additional_details_label = ctk.CTkLabel(self.pet_details_frame, text="Additional details go here...", font=("Arial", 16))
        additional_details_label.grid(row=0, column=1, padx=(20, 10), pady=10, sticky="w")

        adopt_button = ctk.CTkButton(self.pet_details_frame, text="Adopt", fg_color="#ff7a59", text_color="white", command=lambda p=pet_name,c=category,img=imge:self.add_to_profile(p,c,imge))
        adopt_button.grid(row=1, column=1, pady=10, sticky="n")

        # Ensure that pet details frame expands properly
        self.pet_details_frame.grid_columnconfigure(0, weight=0)  # Left side (image)
        self.pet_details_frame.grid_columnconfigure(1, weight=1)  # Right side (details)
        self.pet_details_frame.grid_rowconfigure(0, weight=1)  # Top part (image and main details)
        self.pet_details_frame.grid_rowconfigure(1, weight=1)  # Bottom part (additional details)

    def add_to_profile(self,pet_name,category,imge):
        adopted_pet_users( self.logged_in_user[0],imge,pet_name,category)

app = MainApp()
app.mainloop()
