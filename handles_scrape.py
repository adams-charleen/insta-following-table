import requests
import json
import time
import os
import random

# Instagram credentials
IG_USERNAME = "fill in"
IG_PASSWORD = "fill in"

# Consistent headers
BASE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.166 Safari/537.36",
    "X-IG-App-ID": "936619743392459",  # Instagram app ID
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://www.instagram.com/",
}

# Function to log in and get session cookies
def get_instagram_cookies(username, password):
    session = requests.Session()
    login_url = "https://www.instagram.com/accounts/login/ajax/"
    
    # Get CSRF token
    response = session.get("https://www.instagram.com/", headers=BASE_HEADERS)
    csrf_token = response.cookies.get("csrftoken", "")
    
    # Login payload
    payload = {
        "username": username,
        "enc_password": f"#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}",
        "queryParams": "{}",
        "optIntoOneTap": "false"
    }
    
    login_headers = BASE_HEADERS.copy()
    login_headers["X-CSRFToken"] = csrf_token
    
    # Attempt login
    login_response = session.post(login_url, data=payload, headers=login_headers)
    if login_response.status_code == 200 and login_response.json().get("authenticated"):
        print("Logged in successfully!")
        return session.cookies
    else:
        print(f"Login failed: {login_response.text}")
        return None

# Function to get following list for a user
def get_following_list(cookies, username):
    try:
        session = requests.Session()
        session.cookies = cookies
        headers = BASE_HEADERS.copy()
        
        # Get user ID
        profile_url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"
        response = session.get(profile_url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to get profile for {username}: {response.status_code} - {response.text}")
            return None
        
        user_data = response.json()
        user_id = user_data["data"]["user"]["id"]
        
        # Fetch following list
        following_url = f"https://i.instagram.com/api/v1/friendships/{user_id}/following/"
        params = {
            "count": 100,
        }
        following_handles = set()
        
        while True:
            response = session.get(following_url, headers=headers, params=params)
            if response.status_code != 200:
                print(f"Failed to fetch following for {username}: {response.status_code} - {response.text}")
                break
            
            data = response.json()
            users = data.get("users", [])
            for user in users:
                following_handles.add(user["username"])
            
            next_max_id = data.get("next_max_id")
            if not next_max_id:
                break
            params["max_id"] = next_max_id
            time.sleep(random.uniform(1, 3))
        
        print(f"Found {len(following_handles)} following for {username}")
        return list(following_handles)
    
    except Exception as e:
        print(f"Error scraping following list for {username}: {e}")
        return None

# Main function to scrape following lists
def scrape_following(handles, username, password):
    cookies = get_instagram_cookies(username, password)
    if not cookies:
        return
    
    results = {}
    for i, handle in enumerate(handles):
        print(f"Scraping following for {handle} ({i+1}/{len(handles)})...")
        following_list = get_following_list(cookies, handle)
        if following_list:
            results[handle] = following_list
        else:
            results[handle] = "Failed to retrieve following list"
        time.sleep(random.uniform(2, 4))
    
    output_dir = '/Users/charleenadams/scraping_insta'
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'instagram_following.txt')
    
    with open(output_file, 'w') as file:
        for handle, following in results.items():
            file.write(f"{handle}: {following}\n")
    
    print(f"Following lists saved to {output_file}")
    return results

# Full list of Instagram handles
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
    scrape_following(handles, IG_USERNAME, IG_PASSWORD)
