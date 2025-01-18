from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import csv
from datetime import datetime
import pandas as pd
import pickle
import os

# Constants
WHATSAPP_WEB_URL = 'https://web.whatsapp.com/'
COOKIES_FILE = 'whatsapp_cookies.pkl'
USER_DATA_DIR = 'chrome_profile'

# Message content
message = """*FREE Skill Development Course with 100% Job Assistance*

Join our *Warehouse Supervisor Training Program* in the *Logistics & Supply Chain Management Sector* and take the first step toward a promising career.

* *Duration*: 3 Months
* *Eligibility*: 12th Pass or Above
* *Fees: Absolutely FREE*
* *Certified by: NSDC & Govt. Approved*"""

def setup_driver():
    """Setup Chrome driver with persistent profile"""
    chrome_options = Options()
    chrome_options.add_argument(f'user-data-dir={os.path.abspath(USER_DATA_DIR)}')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def is_logged_in(driver):
    """Check if WhatsApp Web is logged in"""
    try:
        driver.implicitly_wait(5)
        search_box = driver.find_element(By.XPATH, '//*[@id="side"]/div[1]/div/div[2]/div[2]/div/div')
        return True
    except:
        return False

def load_numbers_from_csv():
    """Load numbers from CSV and return as DataFrame"""
    try:
        if not os.path.exists('mobile_numbers.csv'):
            # Create new CSV if it doesn't exist
            df = pd.DataFrame(columns=['number', 'status', 'timestamp'])
            df.to_csv('mobile_numbers.csv', index=False)
            return df
        return pd.read_csv('mobile_numbers.csv')
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return pd.DataFrame(columns=['number', 'status', 'timestamp'])

def update_status_batch(df):
    """Save all status updates to CSV at once"""
    try:
        df.to_csv('mobile_numbers.csv', index=False)
        return True
    except Exception as e:
        print(f"Error saving CSV: {e}")
        df.to_csv('mobile_numbers_' + datetime.now() + '.csv', index=False)
        return False

def update_status(df, number, status, index):
    """Update status and timestamp for a number in DataFrame"""
    try:
        # Update existing row
        df.loc[index, 'status'] = status
        df.loc[index, 'timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return df
        
    except Exception as e:
        print(f"Error updating status for {number}: {e}")
        return df

def send_whatsapp_messages():
    # Initialize WebDriver with persistent profile
    driver = setup_driver()
    
    try:
        # Load numbers from CSV
        df = load_numbers_from_csv()
        status_updates_needed = False
        
        # Open WhatsApp Web
        driver.get(WHATSAPP_WEB_URL)
        
        # Check if already logged in
        if not is_logged_in(driver):
            print("Please scan the QR code to log in...")
            input("Press Enter after scanning the QR code...")
        else:
            print("Using existing WhatsApp session...")
        
        # Ensure we're fully loaded
        time.sleep(5)
        
        # Process each number
        for index, row in df.iterrows():
            number = str(int(row['number']))
            current_status = str(row.get('status', ''))
            
            # Skip if already sent
            if current_status.lower() == 'sent':
                print(f"{index + 1} Skipping {number} - already sent")
                continue
                
            try:
                print(f"{index + 1} Sending to {number}...")
                
                # Search for the contact
                search_box = driver.find_element(By.XPATH, '//*[@id="side"]/div[1]/div/div[2]/div[2]/div/div')
                search_box.click()
                search_box.send_keys(Keys.CONTROL, 'a')
                time.sleep(1)
                search_box.send_keys(Keys.BACKSPACE)
                time.sleep(1)
                
                # Enter number and send message
                search_box.send_keys(number)
                time.sleep(2)
                search_box.send_keys(Keys.ENTER)
                time.sleep(2)
                
                # Find and fill message box
                msg_box = driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[1]/div[2]/div[1]/p')
                msg_box.click()
                msg_box.send_keys(Keys.CONTROL, 'v')
                time.sleep(1)
                msg_box.send_keys(Keys.ENTER)
                
                # Clear search
                search_box.send_keys(Keys.ESCAPE)
                search_box.send_keys(Keys.ESCAPE)
                search_box.send_keys(Keys.ESCAPE)
                
                # Update status in DataFrame
                df = update_status(df, number, 'sent', index)
                status_updates_needed = True
                print(f"{index + 1} Message sent to {number}")
                
                # Wait between messages to avoid rate limiting
                time.sleep(3)
                
            except Exception as e:
                print(f"{index + 1} Failed to send message to {number}: {e}")
                df = update_status(df, number, 'failed', index)
                status_updates_needed = True
                time.sleep(2)
                
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Save all status updates at once
        if status_updates_needed:
            print("Saving status updates...")
            update_status_batch(df)
            
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    # Create profile directory if it doesn't exist
    if not os.path.exists(USER_DATA_DIR):
        os.makedirs(USER_DATA_DIR)
        
    send_whatsapp_messages()