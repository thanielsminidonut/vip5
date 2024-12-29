import requests
import uuid
import time
import random
from concurrent.futures import ThreadPoolExecutor
from colorama import init, Fore, Style
import os

def clear_console():
	os.system('cls' if os.name == 'nt' else 'clear')
init(autoreset=True)


user_agents = [
    "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
]

def process_credentials(username, password, token_file_path):
    data = {
        'adid': str(uuid.uuid4()),
        'format': 'json',
        'device_id': str(uuid.uuid4()),
        'cpl': 'true',
        'family_device_id': str(uuid.uuid4()),
        'credentials_type': 'device_based_login_password',
        'error_detail_type': 'button_with_disabled',
        'source': 'device_based_login',
        'email': username,
        'password': password,
        'access_token': '350685531728|62f8ce9f74b12f84c123cc23437a4a32',
        'generate_session_cookies': '1',
        'meta_inf_fbmeta': '',
        'advertiser_id': str(uuid.uuid4()),
        'currently_logged_in_userid': '0',
        'locale': 'en_US',
        'client_country_code': 'US',
        'method': 'auth.login',
        'fb_api_req_friendly_name': 'authenticate',
        'fb_api_caller_class': 'com.facebook.account.login.protocol.Fb4aAuthHandler',
        'api_key': '62f8ce9f74b12f84c123cc23437a4a32',
    }

    url = 'https://graph.facebook.com/auth/login'
    
    headers = {
        'User-Agent': random.choice(user_agents),
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
    }

    try:
        response = requests.post(url, data=data, headers=headers)
        response_data = response.json()
        
        if 'access_token' in response_data:
            token = response_data['access_token']
            save_token(token, token_file_path)
            print(f"{Fore.GREEN}[ SUCCESS ] ---> {Fore.YELLOW}GETTING TOKEN IN {username}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}[ FAILURE ] ---> NO TOKEN FOR {username}: {response_data.get('error', 'Unknown error')}{Style.RESET_ALL}")

    except Exception as e:
        print(f"{Fore.RED}[ ERROR ] ---> ERROR PROCESSING {username}: {e}{Style.RESET_ALL}")

def save_token(token, token_file_path):
    with open(token_file_path, 'a') as token_file:
        token_file.write(token + '\n')
def get_approval_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def approval():
    clear_console()
    user_id = str(os.geteuid())
    uuid = f"{user_id}DS{user_id}"
    key = f"RFCP-{uuid}"

    print("\033[1;37m [\u001b[36m•\033[1;37m] You Need Approval To Use This Tool   \033[1;37m")
    print(f"\033[1;37m [\u001b[36m•\033[1;37m] Your Key :\u001b[36m {key}")
    
    urls = [
        "https://github.com/nathanielromerorfcp/approval/blob/main/PremiumTools/approval.txt"
    ]
    
    key_found = False
    for url in urls:
        approval_data = get_approval_data(url)
        if key in approval_data:
            key_found = True
            break

    if key_found:
        print(f"\033[1;97m >> Your Key Has Been Approved!!!")
        return key
    else:
        
        exit()

def main():
    approval()
    save_option = input("Where do you want to save the tokens? (FRA/RPA): ").strip().lower()
    
    if save_option == 'fra':
        token_file_path = '/sdcard/RFCPTOOLS/tokens/account/fraaccount.txt'
    elif save_option == 'rpa':
        token_file_path = '/sdcard/RFCPTOOLS/tokens/account/rpaaccount.txt'
    else:
        print("Invalid option. Please choose FRA or RPA.")
        return

    credentials_path = '/sdcard/RFCPTOOLS/credentials/id.txt'

    with open(credentials_path, 'r') as file:
        credentials = [line.strip().split(' | ') for line in file.readlines()]

    with ThreadPoolExecutor(max_workers=2) as executor:
        for username, password in credentials:
            executor.submit(process_credentials, username, password, token_file_path)
            time.sleep(2)  

if __name__ == "__main__":
    main()
