import bcrypt
import os

USER_DATA_FILE = "users.txt"

#Implement the Password Hashing Function
def hash_password(plain_text_password):
    #Encode the password to bytes (bcrypt requires byte strings)
    password_bytes = plain_text_password.encode('utf-8')

    #Generate a salt using bcrypt.gensalt()
    salt = bcrypt.gensalt()

    #Hash the password using bcrypt.hashpw()
    hashed_password = bcrypt.hashpw(password_bytes, salt)

    #Decode the hash back to a string to store in a text file
    return hashed_password.decode('utf-8')

#Implement the Password Verification Function
def verify_password(plain_text_password, hashed_password):
    #Encode both the plaintext password and the stores hash to bytes
    password_bytes = plain_text_password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')

    #Use bcrypt.checkpw() to verify the password
    # This function extracts the salt from the hash and compares
    return bcrypt.checkpw(password_bytes, hashed_password_bytes)

#Registers a new user by hashing their password and storing credentials.
def register_user(username, password):
    #Check if the username already exists
    if user_exists(username):
        return False
    else:
        # Hash the password
        hashed_password = hash_password(password)

        # Append the new user to the file
        with open(USER_DATA_FILE, "a") as f:
            f.write(f"{username},{hashed_password}\n")
            print(f"Success: User '{username}' registered successfully!")
        return True

#Checks if a username already exists in the user database.
def user_exists(username):
    #Handle the case where the file doesn't exist yet
    if not os.path.exists(USER_DATA_FILE):
        f = open(USER_DATA_FILE, "x")
        f.close()

    #Read the file and check each line for the username
    with open(USER_DATA_FILE, "r") as f:
        for line in f.readlines():
            user, hash1 = line.strip().split(',', 1)
            if user == username:
                return True
    return False

#Authenticates a user by verifying their username and password.
def login_user(username, password):
    #Handle the case where no users are registered yet
    if not os.path.exists(USER_DATA_FILE) or os.path.getsize(USER_DATA_FILE) == 0:
        return False
    #Search for the username in the file
    with open(USER_DATA_FILE, "r") as f:
        #Search for the username in the file
        for line in f.readlines():
            user, hash1 = line.strip().split(',', 1)
            #If username matches, verify the password
            if user == username:
                return verify_password(password, hash1)

    #If we reach here, the username was not found
    return False

#Validates username format.
def validate_username(username):
    if len(username) < 3 or len(username) > 20 or username.isalpha():
        return False,"Username is not valid"

    return True, "Username is valid"

#Validates password strength.
def validate_password(password):
    if len(password) < 6 or len(password) > 50 :
        return False,"Password is not valid"
    
    return True, "Password is valid"

# the main program logic
def display_menu():
    """Displays the main menu options."""
    print("\n" + "="*50)
    print(" MULTI-DOMAIN INTELLIGENCE PLATFORM")
    print(" Secure Authentication System")
    print("="*50)
    print("\n[1] Register a new user")
    print("[2] Login")
    print("[3] Exit")
    print("-"*50)
def main():
    """Main program loop."""
    print("\nWelcome to the Week 7 Authentication System!")

    while True:
        display_menu()
        choice = input("\nPlease select an option (1-3): ").strip()

        if choice == '1':
            # Registration flow
            print("\n--- USER REGISTRATION ---")
            username = input("Enter a username: ").strip()

            # Validate username
            is_valid, error_msg = validate_username(username)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            password = input("Enter a password: ").strip()

            # Validate password
            is_valid, error_msg = validate_password(password)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            # Confirm password
            password_confirm = input("Confirm password: ").strip()
            if password != password_confirm:
                print("Error: Passwords do not match.")
                continue

            if user_exists(username):
                print(f"Error: Username '{username}' already exists.")
            # Register the user
            register_user(username, password)


        elif choice == '2':
            # Login flow
            print("\n--- USER LOGIN ---")
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()

            if not user_exists(username):
                print(f"Error: Username not found.")

            # Attempt login
            if login_user(username, password):
                print("\nYou are now logged in.")
                print("(In a real application, you would now access the dashboard)")

                # Optional: Ask if they want to logout or exit
                input("\nPress Enter to return to main menu...")

            if user_exists(username) and not login_user(username, password):
                print("Error: Invalid password.")

        elif choice == '3':
            # Exit
            print("\nThank you for using the authentication system.")
            print("Exiting...")
            break

        else:
            print("\nError: Invalid option. Please select 1, 2, or 3.")



if __name__ == "__main__":
 main()