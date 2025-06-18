# Version 2.0.1

# ----- Import dependencies -----

from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time
import re
import pandas as pd
import getpass

# ----- Search Query -----

# Query user for search term
search_query = input("Enter search term:\n")

# Store URL encode regex replacements (old,new) as a list
url_encodes = [
    ('\s','%20'),
    ('#','%23')
]

# Loop through URL encode regex replacements, applying to search query
for old, new in url_encodes:
    encoded_search_query = re.sub(old,new,search_query).lower()

# Ask user if they want to scrape for the most recent posts or popular posts and then concatenate search URL and search query
while True:
    post_type = input("Do you want to scrape [R]ecent posts or [P]opular posts?:\n")
    if post_type == "R" or "r":
        search_url = 'https://www.linkedin.com/search/results/content/?keywords=' + encoded_search_query + "&origin=FACETED_SEARCH&sortBy=%22date_posted%22"
        break
    elif post_type == "P" or "p":
        search_url = 'https://www.linkedin.com/search/results/content/?keywords=' + encoded_search_query + "&origin=SWITCH_SEARCH_VERTICAL"
        break
    else:
        print("You entered an invalid response. Please try again by entering 'R' or 'P'.")

# Ask user how many posts they want to scrape
while True:
    post_quantity = input("Approximately how many posts do you want to scrape? Please enter one of the below options, entering 1-4:\n\n[1]: 30-40\n[2]: 50-60\n[3]: 100-120\n[4]: 200+\n")
    if post_quantity == "1":
        scrape_length = 40
        break
    elif post_quantity == "2":
        scrape_length = 80
        break
    elif post_quantity == "3":
        scrape_length = 150
        break
    elif post_quantity == "4":
        scrape_length = 280
        break
    else:
         print("You entered an invalid response. Please try again.")

# Prompt for username and password
user_name = input("Enter your username (name@email):\n")
user_passwd = getpass.getpass(prompt="Enter your password:\n")

# ----- Login to LinkedIn with selenium webdriver -----

# Create webdriver instance
driver = webdriver.Chrome()

print("Opening up a Chrome window and logging in...")

# Open linkedIn's login page
driver.get("https://www.linkedin.com/login")

# Wait for the page to load
time.sleep(2)

# entering username
username = driver.find_element(By.ID, "username")

# Enter Your Email Address
username.send_keys(user_name) 

# entering password
pword = driver.find_element(By.ID, "password")

# Enter Your Password
pword.send_keys(user_passwd)	 

# Click on the log in button
driver.find_element(By.XPATH, "//button[@type='submit']").click()

print("You have 10 seconds to complete the verification check. Please complete it now. If no verification check is shown, please wait 15 seconds...")

time.sleep(10)

# ----- Open feed of search query -----

# Open link
driver.get(search_url) 

print("Scrolling through the feed and scraping data...")

# Scroll to bottom
start = time.time()

# will be used in the while loop
initialScroll = 0
finalScroll = 5000

while True:
    driver.execute_script(f"window.scrollTo({initialScroll},{finalScroll})")
	# this command scrolls the window starting from
	# the pixel value stored in the initialScroll 
	# variable to the pixel value stored at the
	# finalScroll variable
    initialScroll = finalScroll
    finalScroll += 5000

	# we will stop the script for 3 seconds so that 
	# the data can load
    time.sleep(5)
	# You can change it as per your needs and internet speed

    end = time.time()

    print("...")

	# We will scroll for 60 seconds.
	# You can change it as per your needs and internet speed
    if round(end - start) > scrape_length:
        break

# Find all "...more" buttons
more_buttons = driver.find_elements(By.CSS_SELECTOR, 'button.feed-shared-inline-show-more-text__see-more-less-toggle')

# Click each one
for btn in more_buttons:
    try:
        driver.execute_script("arguments[0].click();", btn)
        time.sleep(0.5)  # slight delay to avoid race conditions
    except Exception as e:
        print(f"Could not click button: {e}")
      
# ----- Data Scraping -----
	
# Extract data from entire page
search_src = driver.page_source # This gets the source code of the current page
soup = BeautifulSoup(search_src, 'lxml') # This sets source code to var soup

# Find all post containers
posts = soup.select('ul li.artdeco-card.mb2:has(div)')

# Parse each post and extract the relevant fields
data = []
for post in posts:
    date = post.select_one('div > span.update-components-actor__sub-description.text-body-xsmall > span:nth-child(1)')
    url = post.select_one('div.feed-shared-update-v2')
    author = post.select_one('div.update-components-actor__container > div.update-components-actor__meta > a > span.update-components-actor__title > span:nth-of-type(1) > span > span:nth-of-type(1)')
    title = post.select_one('div.update-components-actor__container > div.update-components-actor__meta > a > span.update-components-actor__description > span:nth-of-type(1)')
    author_url = post.select_one('div.update-components-actor--with-control-menu > div.update-components-actor__container > div.update-components-actor__meta > a:nth-of-type(1)')
    text = post.select_one('div.feed-shared-inline-show-more-text.feed-shared-update-v2__description.feed-shared-inline-show-more-text--minimal-padding')
    likes = post.select_one('li.social-details-social-counts__item.social-details-social-counts__reactions.social-details-social-counts__reactions--left-aligned span')
    comments = post.select_one('div.social-details-social-counts > div > div > ul > li > ul> li.social-details-social-counts__item.social-details-social-counts__comments.social-details-social-counts__item--right-aligned > button')
    reposts = post.select_one('div.social-details-social-counts > div > div > ul > li > ul > li.social-details-social-counts__item.social-details-social-counts__item--right-aligned.social-details-social-counts__item--height-two-x.flex-shrink-1.overflow-hidden > button > span')

    if date:
        # List sub regexes for dates
        date_transformations = [
            (r'^(.*?)\s•.*', r'\1'),
            (r'now', '0'),
            (r'\d+h','0'),
            (r'(\d+)d','\\1'),
            (r'1w','7'),
            (r'2w','14'),
            (r'3w','21'),
            (r'4w','28'),
            (r'5w','35'),
            (r'6w','42'),
            (r'7w','49'),
            (r'8w','56'),
            (r'1mo','30'),
            (r'2mo','60'),
            (r'3mo','90'),
            (r'4mo','120'),
            (r'5mo','150'),
            (r'6mo','180'),
            (r'7mo','210'),
            (r'8mo','240'),
            (r'9mo','270'),
            (r'10mo','300'),
            (r'11mo','330'),
            (r'12mo','365'),
            (r'1yr','365'),
            (r'2yr','730'),
            (r'\d+m','0')
        ]

        # get raw dates
        days = date.get_text(strip=True)

        # loop through regex date transformations on raw dates to return number of days
        for pattern, repl in date_transformations:
            days = re.sub(pattern, repl, days, flags=re.IGNORECASE)

        # Get current date and time
        current_date = datetime.now().date()

        # Calculate the differences between the current date and each number of days
        post_date = current_date - timedelta(days=int(days))

        # Format the post date
        formatted_post_date = post_date.strftime("%Y-%m-%d")

    else:
        formatted_post_date = None

    if url:
        post_url = "https://www.linkedin.com/feed/update/" + url["data-urn"]
    else:
        post_url = None

    if author:
        author_name = author.get_text(strip=True)
    else:
        author_name = None

    if title:
        author_title = re.sub(r'\d+\,*\d+\Wfollowers', r'', title.get_text(strip=True), flags=re.IGNORECASE)
    else:
        author_title = None

    if author_url:
        author_url_value = re.sub(r'\?miniProfileUrn\=.*$', r'', re.sub(r'\/posts$', r'', author_url["href"], flags=re.IGNORECASE), flags=re.IGNORECASE)
    else:
        author_url_value = None

    if text:
        post_text_substitutions = [
            (r'hashtag#', r' #'),
            (r'translation\ssettings|show\soriginal', r'')
        ]

        post_text = text.get_text(strip=True)

        for pattern, repl in post_text_substitutions:
            post_text = re.sub(pattern, repl, post_text, flags=re.IGNORECASE)
    else:
        post_text = None

    if likes:
        like_count = int(re.sub(r'(\d+).*', r'\1', likes.get_text(strip=True), flags=re.IGNORECASE))
    else:
        like_count = 0

    if comments:
        comment_count = int(re.sub(r'^(.*?)\s.*', r'\1', comments.get_text(strip=True), flags=re.IGNORECASE))
    else:
        comment_count = 0

    if reposts:
        repost_count = int(re.sub(r'^(.*?)\s.*', r'\1', reposts.get_text(strip=True), flags=re.IGNORECASE))
    else:
        repost_count = 0

    engagements = like_count + comment_count + repost_count

    data.append({
        'search_query': search_query,
        'post_date': formatted_post_date,
        'post_url': post_url,
        'author_name': author_name,
        'author_title': author_title,
        'author_url': author_url_value,
        'post_text': post_text,
        'likes': like_count,
        'comments': comment_count,
        'reposts': repost_count,
        'engagements': engagements
    })

# Convert to a DataFrame for easier handling
df = pd.DataFrame(data)

# Show the resulting table
print(df)

# ----- Write Data to Excel file -----

# Set current timestamp
timestamp = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")

# set filename and export to excel
filename = '/Users/azntaiji/Downloads/' + search_query + "_" + str(timestamp) + '.xlsx'
df.to_excel(filename, index=False)

print("File saved! Check downloads folder.")