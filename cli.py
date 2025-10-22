import requests
import json

# --- API CONFIGURATION ---
API_BASE_URL = "http://127.0.0.1:8000"
auth_token = None

# --- CORE FUNCTIONS ---

def login():
    """Logs the user in and stores the auth token."""
    global auth_token
    print("\n--- 🔑 User Login ---")
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    
    try:
        response = requests.post(f"{API_BASE_URL}/users/login", data={"username": email, "password": password})
        
        print(f"\n--- DEBUG INFO ---")
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {response.headers}")
        print(f"Response Text (raw): >{response.text}<")
        print(f"--- END DEBUG INFO ---\n")

        if response.status_code == 200:
            auth_token = response.json()["access_token"]
            print("[SUCCESS] Login successful!")
        else:
            # Try to parse JSON, but have a fallback
            try:
                detail = response.json().get('detail')
            except json.JSONDecodeError:
                detail = response.text
            print(f"[ERROR] Login failed. Detail: {detail}")
            
    except requests.exceptions.RequestException as e:
        print(f"\n[ERROR] Could not connect to the API: {e}")

def view_all_items():
    """Retrieves and prints all items (shoutouts) from the API."""
    print("\n--- All Items ---")
    try:
        response = requests.get(f"{API_BASE_URL}/items/")
        if response.status_code == 200:
            items = response.json()
            if not items:
                print("\n-- No items yet! --")
            else:
                for item in items:
                    print(f"\nID: {item['id']}")
                    print(f"  Title: {item['title']}")
                    print(f"  Description: {item['description']}")
                    print(f"  Owner ID: {item['owner_id']}")
                print("---------------------")
        else:
            print(f"\n[ERROR] Could not retrieve items: {response.json().get('detail')}")
            
    except requests.exceptions.RequestException as e:
        print(f"\n[ERROR] Could not connect to the API: {e}")

def add_item():
    """Prompts for item details and adds it via the API."""
    global auth_token
    if not auth_token:
        print("\n[ERROR] You must be logged in to add an item. Please log in first.")
        return

    print("\n--- ✨ Add a New Item ---")
    title = input("Enter the title: ")
    description = input("Enter the description: ")
    
    headers = {"Authorization": f"Bearer {auth_token}"}
    payload = {"title": title, "description": description}
    
    try:
        response = requests.post(f"{API_BASE_URL}/items/", headers=headers, json=payload)
        
        if response.status_code == 200:
            print("\n[SUCCESS] Item added successfully!")
        else:
            print(f"\n[ERROR] Could not add item: {response.json().get('detail')}")
            
    except requests.exceptions.RequestException as e:
        print(f"\n[ERROR] Could not connect to the API: {e}")

# --- MAIN MENU ---

def main_menu():
    """Displays the main menu and handles user input."""
    while True:
        print("\n--- BragBoard API CLI ---")
        print("1. Login")
        print("2. View all items")
        print("3. Add a new item")
        print("4. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            login()
        elif choice == '2':
            view_all_items()
        elif choice == '3':
            add_item()
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
