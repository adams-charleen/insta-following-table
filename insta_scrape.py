from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# Function to initialize the Chrome driver
def init_driver(headless=True):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")
    options.add_argument("--window-size=1920,1080")
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        return driver
    except Exception as e:
        print(f"Failed to initialize driver: {e}")
        return None

# Function to log into Instagram
def login_to_instagram(driver, username, password):
    try:
        print("Navigating to Instagram login page...")
        driver.get("https://www.instagram.com/accounts/login/")
        
        # Wait for username field
        print("Waiting for username field...")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        print("Username field found.")
        
        # Enter username
        username_field = driver.find_element(By.NAME, "username")
        username_field.clear()
        username_field.send_keys(username)
        print("Username entered.")
        
        # Enter password
        password_field = driver.find_element(By.NAME, "password")
        password_field.clear()
        password_field.send_keys(password)
        print("Password entered.")
        
        # Click login button
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()
        print("Login button clicked.")
        
        # Wait for login to complete (look for Instagram logo or profile element)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//span[text()='Instagram'] | //div[@role='button']"))
        )
        print("Login appears successful.")
        
        # Handle "Save Login Info" popup if it appears
        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[text()='Not Now']"))
            ).click()
            print("Clicked 'Not Now' on Save Login Info popup.")
        except:
            print("No Save Login Info popup detected.")
        
        # Handle "Turn on Notifications" popup if it appears
        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[text()='Not Now']"))
            ).click()
            print("Clicked 'Not Now' on Notifications popup.")
        except:
            print("No Notifications popup detected.")
        
        time.sleep(2)
        return True
    except Exception as e:
        print(f"Login failed: {e}")
        return False

# Function to get Instagram data
def get_instagram_data(driver, username):
    try:
        print(f"Navigating to https://www.instagram.com/{username}/")
        driver.get(f"https://www.instagram.com/{username}/")
        
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//header//section//ul | //div[contains(text(), 'This Account is Private')] | //div[contains(text(), 'Sorry, this page')]"))
        )
        
        if driver.find_elements(By.XPATH, "//div[contains(text(), 'This Account is Private')]"):
            return "Private account"
        if driver.find_elements(By.XPATH, "//div[contains(text(), 'Sorry, this page')]"):
            return "Account not found"

        stats = driver.find_elements(By.XPATH, "//header//section//ul/li")
        if len(stats) < 3:
            raise Exception("Profile stats not fully loaded or structure unexpected")

        posts = stats[0].find_element(By.XPATH, ".//span").text
        followers = stats[1].find_element(By.XPATH, ".//span[@title]").get_attribute("title")
        following = stats[2].find_element(By.XPATH, ".//span").text

        return {"posts": posts, "followers": followers, "following": following}
    
    except Exception as e:
        print(f"Error while scraping {username}: {str(e)}")
        return None

# Main function to scrape a list of handles
def scrape_instagram(handles, ig_username, ig_password, headless=True, batch_size=5):
    results = {}
    driver = init_driver(headless)
    if not driver:
        print("Driver initialization failed, stopping.")
        return
    
    if not login_to_instagram(driver, ig_username, ig_password):
        driver.quit()
        return
    
    for i, username in enumerate(handles):
        if i % batch_size == 0 and i > 0:
            driver.quit()
            driver = init_driver(headless)
            if not driver or not login_to_instagram(driver, ig_username, ig_password):
                print("Driver reinitialization or login failed, stopping.")
                break
        
        print(f"Scraping {username} ({i+1}/{len(handles)})...")
        time.sleep(3)
        data = get_instagram_data(driver, username)
        if data:
            results[username] = data
        else:
            results[username] = "Failed to retrieve data"
    
    driver.quit()
    
    output_dir = '/Users/charleenadams/scraping_insta'
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'instagram_results.txt')

    with open(output_file, 'w') as file:
        for username, data in results.items():
            file.write(f"{username}: {data}\n")

    print(f"Results saved to {output_file}")
    return results

# List of Instagram handles to scrape
handles = [
    "hls_lsfp", "harvardoop", "harvardundergradpsc", "harvardgs4p", "harvj4p",
    "dissentcollective", "hds_muslims", "hgse4palestine", "hgsubds", "jews4liberation",
    "harvardalums4palestine", "hlstzedek", "m1t_caa", "mitg4p", "bostonpsl",
    "bdsboston", "rjp.boston", "pymboston", "bostoncoalitionforpalestine", "boston_dsa",
    "somervilleforpalestine", "mapping_project", "cambridge4palestine", "berkleesjp",
    "jvpboston", "healthcareworkersforpalestine", "nationalsjp", "middleeastmatters",
    "cuapartheiddivest", "hiddenpalestine", "illuminated_cities", "pal_legal",
    "brownmed4palestine", "librarianswithpalestine", "boylstonsjp", "theimeu", "umbsjp"
]

# Run the scraper
if __name__ == "__main__":
    IG_USERNAME = "your_instagram_username"  # Replace with your username
    IG_PASSWORD = "your_instagram_password"  # Replace with your password
    
    scrape_instagram(handles, IG_USERNAME, IG_PASSWORD, headless=False, batch_size=5)
