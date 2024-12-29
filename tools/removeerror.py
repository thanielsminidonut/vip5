


import requests
import time
from colorama import Fore, Style, init
import os
import platform

init(autoreset=True)

def display_logo():
    logo = """
             ██████  ███████  ██████ ██████  
             ██   ██ ██      ██      ██   ██ 
             ██████  █████   ██      ██████  
             ██   ██ ██      ██      ██      
             ██   ██ ██       ██████ ██      
                  ʀᴇᴍᴏᴠᴇ ɪɴᴠᴀʟɪᴅ ᴀᴄᴄᴏᴜɴᴛ    
    """
    print(Fore.YELLOW + Style.BRIGHT + logo)

def clear_console():
    # Clear console for different operating systems
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def get_facebook_user_details(access_token):
    url = 'https://graph.facebook.com/me'
    params = {
        'fields': 'name,id,link',
        'access_token': access_token
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        user_details = response.json()
        user_id = user_details.get('id')

        # Print valid account details
        status = "VALID ACCOUNT"
        print(Fore.GREEN + f"ID: {user_id} --> {status}")

        # Save user ID to credentials folder
        credentials_folder = '/sdcard/RFCPTOOLS/tokens/credentials'
        os.makedirs(credentials_folder, exist_ok=True)
        iduser_file_path = os.path.join(credentials_folder, 'accountid.txt')
        
        with open(iduser_file_path, 'a') as file:
            file.write(f"{user_id}\n")
        
        return True  # Valid token
        
    except requests.exceptions.RequestException as e:
        user_id = access_token
        status = "SUSPENDED"
        print(Fore.RED + f"  ID:  --> {status}")
        print(Fore.RED + "Error: " + Style.BRIGHT + str(e))
        if '401' in str(e):
            print(Fore.RED + "The access token might be expired or invalid.")
        return False  # Invalid token

def delete_invalid_tokens(file_path, tokens_to_delete):
    try:
        with open(file_path, 'r') as file:
            tokens = file.read().strip().split('\n')

        valid_tokens = [token for token in tokens if token not in tokens_to_delete]
        
        with open(file_path, 'w') as file:
            for token in valid_tokens:
                file.write(token + '\n')

        print(Fore.CYAN + f"Deleted {len(tokens_to_delete)} invalid tokens from {file_path}.")
        
    except Exception as e:
        print(Fore.RED + f"An error occurred while deleting tokens: {e}")

def process_tokens(file_path):
    valid_tokens = []
    error_tokens_count = 0
    invalid_tokens = []

    try:
        with open(file_path, 'r') as file:
            tokens = file.read().strip().split('\n')

        for token in tokens:
            if token:
                if get_facebook_user_details(token):
                    valid_tokens.append(token)
                else:
                    error_tokens_count += 1
                    invalid_tokens.append(token)  # Track invalid tokens
                time.sleep(1)  # Throttle requests

        # Write only valid tokens back to the file
        with open(file_path, 'w') as file:
            for token in valid_tokens:
                file.write(token + '\n')

        print(Fore.CYAN + f"Total valid accounts: {len(valid_tokens)}")
        print(Fore.CYAN + f"Total suspended accounts: {error_tokens_count}")

        return invalid_tokens  # Return list of invalid tokens

    except FileNotFoundError:
        print(Fore.RED + f"Error: The file {file_path} does not exist.")
    except Exception as e:
        print(Fore.RED + f"An unexpected error occurred: {e}")

def display_menu():
    print(Fore.YELLOW + "Where would you like to delete the invalid tokens?")
    print("1. FRA ACCOUNT")
    print("2. RPA ACCOUNT")
    print("3. RPA PAGE")
    print("4. FRA PAGE")

def main():
    clear_console()  # Clear console at the start
    display_logo()  # Display the logo before processing tokens

    while True:
        # Ask user for the token file path
        token_file_name = input(Fore.CYAN + "Enter the name of the token file  : ")
        tokens_folder = '/sdcard/RFCPTOOLS/tokens/account'
        token_file_path = os.path.join(tokens_folder, token_file_name)
        
        invalid_tokens = process_tokens(token_file_path)

        # Check if invalid tokens were detected and show the menu
        if invalid_tokens:
            print(Fore.YELLOW + f"Invalid tokens detected: {invalid_tokens}")  # Show invalid tokens
            display_menu()
            
            while True:
                choice = input(Fore.CYAN + "Enter your choice (1/2/3/4): ")
                if choice in {'1', '2', '3', '4'}:
                    break
                print(Fore.RED + "Invalid choice. Please enter 1, 2, 3, or 4.")

            if choice == '1':
                delete_invalid_tokens(os.path.join(tokens_folder, 'account', 'fraaccount.txt'), invalid_tokens)
            elif choice == '2':
                delete_invalid_tokens(os.path.join(tokens_folder, 'account', 'rpaaccount.txt'), invalid_tokens)
            elif choice == '3':
                delete_invalid_tokens(os.path.join(tokens_folder, 'account', 'rpapage.txt'), invalid_tokens)
            elif choice == '4':
                delete_invalid_tokens(os.path.join(tokens_folder, 'account', 'frapage.txt'), invalid_tokens)
            
            input(Fore.CYAN + "Press Enter to go back...")
        else:
            print(Fore.YELLOW + "No invalid tokens found. Nothing to delete.")
        
        # Ask if the user wants to continue or exit
        continue_choice = input(Fore.CYAN + "Do you want to check another token file? (yes/no): ").strip().lower()
        clear_console()  # Clear console on user response
        if continue_choice != 'yes':
            print(Fore.YELLOW + "Exiting the program.")
            break

if __name__ == '__main__':
    main()
