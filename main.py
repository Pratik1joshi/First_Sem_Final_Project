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
        self.title("Pawsy Meof Pet Adoption Center")
        self.iconbitmap("logo.ico")
        init_db()
        inits_db()
        self.logged_in_user = get_logged_in_user()
        self.init_ui()

    def init_ui(self):
        # Create a frame for the navbar
        navbar = ctk.CTkFrame(self, height=50, corner_radius=0, fg_color="#aac2e3")
        navbar.pack(side="top", fill="x")  # Add top and bottom padding for the navbar

        logo = ctk.CTkImage(dark_image=Image.open('logo.png'), light_image=Image.open('logo.png'), size=(80, 50))

        # Add the logo to the navbar
        logo = ctk.CTkLabel(navbar, text="", image=logo)
        logo.place(x=90, y=0)  # Place the logo at specific coordinates

        # Add buttons to the navbar
        button_about = ctk.CTkButton(navbar, width=80, text="Home", command=lambda: self.show_hero(), fg_color="#aac2e3", text_color="black")
        button_about.place(x=270, y=10) 

        button_ourworks = ctk.CTkButton(navbar, width=100, text="About Us", command=self.show_about_us, fg_color="#aac2e3", text_color="black")
        button_ourworks.place(x=350, y=10)  

        button_adopt = ctk.CTkButton(navbar, width=100, text="Adopt Animals", command=self.show_explore_more, fg_color="#aac2e3", text_color="black")
        button_adopt.place(x=450, y=10) 

        button_contact = ctk.CTkButton(navbar, width=100, text="Contact", command=self.show_contact_us, fg_color="#aac2e3", text_color="black")
        button_contact.place(x=550, y=10) 

        # Add login/signup button to the navbar
        self.button_login_signup = ctk.CTkButton(navbar, text="Login/Signup", command=self.show_login_signup, fg_color="#ff7a59", text_color="black")
        self.button_login_signup.place(relx=1.0, x=-100, y=10, anchor="ne") 

        # Load background image  
        bg_image_data = Image.open("mainBackground.png")
        bg_image = ctk.CTkImage(dark_image=bg_image_data, light_image=bg_image_data, size=(1000, 640))

        # Create a frame for the background image
        self.bg_frame = ctk.CTkFrame(self, width=1000, height=940)
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
            self.button_login_signup.configure(text=self.logged_in_user[4], command=self.show_logout_options)
        else:
            self.button_login_signup.configure(text="Login/Signup", command=self.show_login_signup)

        self.main_frame = ctk.CTkScrollableFrame(self)
        self.main_frame.pack(fill="both", expand=True)

    
    def show_contact_us(self):
        # Remove any existing content from the contact_us_frame if it exists
        try:
            self.contact_us_frame.destroy()
        except:
            pass
        # Create a new frame for the "Contact Us" content
        self.contact_us_frame = ctk.CTkFrame(self, width=400, height=300, fg_color="#ffffff", corner_radius=10)
        self.contact_us_frame.place(relx=0.5, rely=0.5, anchor="center")

        contact_text = """
        Contact Us

        Phone: +977 9863995341
        Email: jcpratik777@gmail.com
        Address: Kumaripati, Lalitpur, Nepal

        We're here to help you with any questions or concerns you may have.
        """

        contact_label = ctk.CTkLabel(self.contact_us_frame, text=contact_text, wraplength=380, justify="left", text_color="black")
        contact_label.pack(padx=20, pady=20)

        # Add a "Cancel" button to close the contact frame
        cancel_button = ctk.CTkButton(
            self.contact_us_frame, 
            text="Cancel", 
            command=self.contact_us_frame.destroy, 
            fg_color="#ff7a59", 
            text_color="white", 
            width=100, 
            height=30
        )

        cancel_button.pack(pady=10)

    def show_about_us(self):
        # Remove any existing content from the about_us_frame if it exists
        try:
            self.about_us_frame.destroy()
        except:
            pass
        # Create a new frame for the "Contact Us" content
        self.about_us_frame = ctk.CTkFrame(self, width=600, height=500, fg_color="#ffffff", corner_radius=10)
        self.about_us_frame.place(relx=0.5, rely=0.5, anchor="center")

        about_text = """
            Welcome to Pawsy Meof Pet Adoption Center, your trusted partner in bringing joy and companionship to your life through the love of pets. Founded with a passion for animals and a commitment to their well-being, we aim to create a safe and happy environment for every pet and pet owner.

            At Pawsy Meof Pet Adoption Center, we believe that pets are not just animals but family members who bring warmth, laughter, and unconditional love into our lives. Whether you're looking to adopt a new furry friend, find the best products for your pet, or seek expert advice on pet care, we're here to support you every step of the way.

            Our pet shop is more than just a place to buy pets—it's a community where animal lovers come together to share their love for pets. We carefully select our pets from reputable breeders and shelters, ensuring that they are healthy, happy, and ready to become a part of your family. Our adoption process is thorough yet simple, focusing on finding the perfect match between pets and their future families.

            Our team of dedicated animal lovers is always ready to offer personalized advice and assistance, whether you're a first-time pet owner or a seasoned pet parent. We understand the unique needs of each pet and strive to offer solutions that enhance their health, happiness, and well-being.

            At Pawsy Meof Pet Adoption Center, our mission is simple: to connect loving families with loving pets. We believe in the power of the human-animal bond and are committed to nurturing that connection in every way possible.

            Thank you for choosing Pawsy Meof Pet Adoption Center as your trusted source for all things pets. We look forward to helping you find your next best friend and ensuring that every pet lives a happy, healthy, and fulfilling life.
            """
        contact_label = ctk.CTkLabel(self.about_us_frame, text=about_text, wraplength=380, justify="left", text_color="black")
        contact_label.pack(padx=20, pady=20)
        # Add a "Cancel" button to close the contact frame
        cancel_button = ctk.CTkButton(
            self.about_us_frame, 
            text="Cancel", 
            command=self.about_us_frame.destroy, 
            fg_color="#ff7a59", 
            text_color="white", 
            width=100, 
            height=30
        )
        cancel_button.pack(pady=10)



    def update_user_name(self, name):
        self.logged_in_user = name
        self.button_login_signup.configure(text=name[4], command=self.show_logout_options)

    def show_home(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        ctk.CTkLabel(self.main_frame, text="Welcome to the Pet Store!").pack(pady=20)

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
        answer = tk.messagebox.askyesno("Logout Confirmation", "Are you sure you want to log out?")
        if answer:
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
        answer = tk.messagebox.askyesno("Logout Confirmation", "Are you sure you want to log out?")
        if answer:
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
        save_button = ctk.CTkButton(edit_frame, text="Save", 
                                    command=lambda: self.save_edits(new_username_entry.get(), new_phone_entry.get(), new_name_entry.get()))
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
        #hide the background frame
        self.bg_frame.pack_forget()

        # Clear the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        images_folder = "pets_picture"

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

            #full path to the image
            image_path = os.path.join(images_folder, category_images[category])

            # Load and resize the image
            img_data = Image.open(image_path)
            img_data = img_data.resize((500, 290), Image.LANCZOS)
            img_tk = ImageTk.PhotoImage(img_data)

            # Add a label with the image
            img_label = ctk.CTkLabel(self.category_frame, image=img_tk, text="")
            img_label.image = img_tk  # Keep a reference to avoid garbage collection
            img_label.pack(padx=10, pady=10, fill="both", expand=True)

            # Add a label with the category name
            label = ctk.CTkButton(self.category_frame, text=category, font=("Arial", 16, "bold"), text_color="black", 
                                  command=lambda t=category: self.inside_categories(t))
            label.pack(padx=10, pady=10)

        # Configure grid to make sure frames are positioned
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
            pet_button = ctk.CTkButton(self.category_frame, text=pet, font=("Arial", 16, "bold"), text_color="black", 
                                       command=lambda p=pet,c=category,imgPet = pet_categories[pet]: self.show_pet_details(p,c,imgPet))
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
        details_label = ctk.CTkLabel(self.pet_details_frame, text=f"{pet_name}", font=("Arial", 24))
        details_label.grid(row=0, column=1, padx=(30, 10), pady=20, sticky="nw")

        # Additional details can be added below the main details
        additional_details_label = ctk.CTkLabel(self.pet_details_frame, text="Details about this pet", font=("Arial", 16))
        additional_details_label.grid(row=0, column=1, padx=(20, 10), pady=10, sticky="w")

        adopt_button = ctk.CTkButton(self.pet_details_frame, text="Adopt", fg_color="#ff7a59", text_color="white", 
                                     command=lambda p=pet_name,c=category,img=imge:self.add_to_profile(p,c,imge))
        adopt_button.grid(row=1, column=1, pady=10, sticky="n")

        # Ensure that pet details frame expands properly
        self.pet_details_frame.grid_columnconfigure(0, weight=0)  # Left side (image)
        self.pet_details_frame.grid_columnconfigure(1, weight=1)  # Right side (details)
        self.pet_details_frame.grid_rowconfigure(0, weight=1)  # Top part (image and main details)
        self.pet_details_frame.grid_rowconfigure(1, weight=1)  # Bottom part (additional details)

    def add_to_profile(self,pet_name,category,imge):
        if self.logged_in_user:
            tk.messagebox.showinfo("Success!","Pet added")
            adopted_pet_users( self.logged_in_user[0],imge,pet_name,category)
        else:
            tk.messagebox.showerror("Error", "Login First")

app = MainApp()
app.mainloop()
