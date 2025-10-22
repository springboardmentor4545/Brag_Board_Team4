import tkinter as tk                                           #python -m uvicorn backend.main:app --reload
from tkinter import scrolledtext, messagebox, simpledialog     #http://127.0.0.1:8000
import requests
import psycopg2
import os

class BragBoardApp:
    def __init__(self, master):
        self.master = master
        master.title("BragBoard API Client")
        self.api_base_url = "http://127.0.0.1:8000"
        self.auth_token = None

        # --- Login Frame ---
        login_frame = tk.Frame(master, padx=10, pady=10, relief=tk.RIDGE, borderwidth=2)
        login_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(login_frame, text="Login", font=("Helvetica", 12, "bold")).grid(row=0, column=0, columnspan=3)

        tk.Label(login_frame, text="Email:").grid(row=1, column=0, sticky="w")
        self.email_entry = tk.Entry(login_frame, width=40)
        self.email_entry.grid(row=1, column=1, sticky="ew")
        self.email_entry.insert(0, "alice@company.com")

        tk.Label(login_frame, text="Password:").grid(row=2, column=0, sticky="w")
        self.password_entry = tk.Entry(login_frame, show="*", width=40)
        self.password_entry.grid(row=2, column=1, sticky="ew")
        self.password_entry.insert(0, "password123")

        self.login_button = tk.Button(login_frame, text="Login", command=self.login)
        self.login_button.grid(row=1, column=2, rowspan=2, padx=5)
        
        self.status_label = tk.Label(login_frame, text="Status: Not Logged In", fg="red")
        self.status_label.grid(row=3, column=0, columnspan=3, sticky="w")

        # --- Main Content Frame ---
        main_frame = tk.Frame(master, padx=10, pady=10)
        main_frame.pack(fill="both", expand=True)

        # Items display
        items_frame = tk.Frame(main_frame)
        items_frame.pack(fill="both", expand=True, side=tk.LEFT, padx=(0, 10))
        tk.Label(items_frame, text="Items (Brags)").pack(anchor="w")
        self.items_text = scrolledtext.ScrolledText(items_frame, width=80, height=15)
        self.items_text.pack(fill="both", expand=True)
        self.refresh_button = tk.Button(items_frame, text="Refresh Items", command=self.load_items)
        self.refresh_button.pack(pady=5)

        # Add Item form
        add_frame = tk.Frame(main_frame, relief=tk.RIDGE, borderwidth=2, padx=10, pady=10)
        add_frame.pack(fill="y", side=tk.RIGHT)
        tk.Label(add_frame, text="Add New Item", font=("Helvetica", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 10))
        tk.Label(add_frame, text="Title:").grid(row=1, column=0, sticky="w")
        self.title_entry = tk.Entry(add_frame, width=30)
        self.title_entry.grid(row=1, column=1, sticky="ew")
        tk.Label(add_frame, text="Description:").grid(row=2, column=0, sticky="w")
        self.desc_entry = tk.Entry(add_frame, width=30)
        self.desc_entry.grid(row=2, column=1, sticky="ew")
        self.submit_button = tk.Button(add_frame, text="Submit Item", command=self.add_item)
        self.submit_button.grid(row=3, column=0, columnspan=2, pady=10)

        # --- DB Setup Frame ---
        db_frame = tk.Frame(master, padx=10, pady=10, relief=tk.RIDGE, borderwidth=2)
        db_frame.pack(fill="x", padx=10, pady=5)
        tk.Label(db_frame, text="Database Setup", font=("Helvetica", 10, "bold")).pack(anchor="w")
        self.setup_button = tk.Button(db_frame, text="Run SQL Setup Script", command=self.setup_database)
        self.setup_button.pack(side="left", padx=5)
        tk.Label(db_frame, text="(For seeding the DB with test data)").pack(side="left")

        self.load_items()

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        if not email or not password:
            messagebox.showerror("Error", "Email and password cannot be empty.")
            return

        try:
            response = requests.post(f"{self.api_base_url}/users/login", data={"username": email, "password": password})
            if response.status_code == 200:
                self.auth_token = response.json()["access_token"]
                self.status_label.config(text=f"Status: Logged in as {email}", fg="green")
                messagebox.showinfo("Success", "Login successful!")
            else:
                self.auth_token = None
                self.status_label.config(text="Status: Login Failed", fg="red")
                messagebox.showerror("Login Failed", response.json().get("detail", "Unknown error"))
        except requests.exceptions.RequestException as e:
            messagebox.showerror("API Error", f"Could not connect to the API: {e}")

    def load_items(self):
        self.items_text.delete(1.0, tk.END)
        self.items_text.insert(tk.END, "Loading items...\n")
        try:
            response = requests.get(f"{self.api_base_url}/items/")
            self.items_text.delete(1.0, tk.END)
            if response.status_code == 200:
                items = response.json()
                if not items:
                    self.items_text.insert(tk.END, "No items found.")
                else:
                    for item in items:
                        self.items_text.insert(tk.END, f"ID: {item['id']}\n")
                        self.items_text.insert(tk.END, f"  Title: {item['title']}\n")
                        self.items_text.insert(tk.END, f"  Description: {item['description']}\n")
                        self.items_text.insert(tk.END, f"  Owner ID: {item['owner_id']}\n\n")
            else:
                self.items_text.insert(tk.END, f"Error: {response.json().get('detail')}")
        except requests.exceptions.RequestException as e:
            self.items_text.delete(1.0, tk.END)
            self.items_text.insert(tk.END, f"Error loading items: {e}")

    def add_item(self):
        if not self.auth_token:
            messagebox.showerror("Error", "You must be logged in to add an item.")
            return

        title = self.title_entry.get()
        description = self.desc_entry.get()
        if not title:
            messagebox.showerror("Error", "Title is required.")
            return

        headers = {"Authorization": f"Bearer {self.auth_token}"}
        payload = {"title": title, "description": description}

        try:
            response = requests.post(f"{self.api_base_url}/items/", headers=headers, json=payload)
            if response.status_code == 200:
                messagebox.showinfo("Success", "Item added successfully!")
                self.title_entry.delete(0, tk.END)
                self.desc_entry.delete(0, tk.END)
                self.load_items()
            else:
                messagebox.showerror("Error", f"Could not add item: {response.json().get('detail')}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("API Error", f"Could not connect to the API: {e}")

    def setup_database(self):
        password = simpledialog.askstring("Password", "Enter PostgreSQL password for user 'postgres':", show='*')
        if not password:
            return

        try:
            conn = psycopg2.connect(host="localhost", port="5432", user="postgres", password=password, dbname="project_db")
            cur = conn.cursor()
            script_path = os.path.join(os.path.dirname(__file__), 'db_setup.sql')
            with open(script_path, 'r', encoding='utf-8') as f:
                sql_script = f.read()
            cur.execute(sql_script)
            conn.commit()
            cur.close()
            conn.close()
            messagebox.showinfo("Success", "Database setup script executed successfully!")
            self.load_items()
        except psycopg2.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        except FileNotFoundError:
            messagebox.showerror("File Error", f"db_setup.sql not found in the directory.")

if __name__ == "__main__":
    root = tk.Tk()
    app = BragBoardApp(root)
    root.mainloop()