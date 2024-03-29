# Version 2.0.0

# ----- Import dependencies -----

from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import csv
import time
import re
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
        search_url = 'https://www.linkedin.com/search/results/content/?keywords=' + encoded_search_query + "&origin=FACETED_SEARCH&sortBy=%22relevance%22"
        break
    else:
        print("You entered an invalid response. Please try again by entering 'R' or 'P'.")

# Ask user how many posts they want to scrape
while True:
    post_quantity = input("Approximately how many posts do you want to scrape? Please enter one of the below options, entering 1-4:\n\n[1]: 30-40\n[2]: 50-60\n[3]: 100-120\n[4]: 200+\n")
    if post_quantity == "1":
        scrape_length = 15
        break
    elif post_quantity == "2":
        scrape_length = 30
        break
    elif post_quantity == "3":
        scrape_length = 60
        break
    elif post_quantity == "4":
        scrape_length = 120
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
      
# ----- Extract Data -----
	
# Extract data from entire page
search_src = driver.page_source # This gets the source code of the current page
soup = BeautifulSoup(search_src, 'lxml') # This sets source code to var soup

# Extract post dates source code
date_html = soup.select("div.pt1.mb2.artdeco-card > div > div > div.feed-shared-update-v2 > div > div.update-components-actor > div.update-components-actor__container > div.update-components-actor__meta > a > span.update-components-actor__sub-description > div > span > span:nth-of-type(1)")
 
# Create raw date var as empty list
raw_dates = []
 
# Pull date text from source code and add to list
for date in date_html:
    raw_dates.append(re.sub(r'\s•.*','',date.text.strip()))
    
# List sub regexes for dates
date_transformations = [  
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

# Loop through date regexes to turn raw LinkedIn dates into number of days
for x in range(len(raw_dates)):
    for old, new in date_transformations:
        raw_dates[x] = re.sub(old, new, raw_dates[x])

# Convert raw dates list to int
days_list = [int(x) for x in raw_dates]

# Get current date and time
current_date = datetime.now().date()

# Calculate the differences between the current date and each number of days in the list
result_dates = [current_date - timedelta(days=days) for days in days_list]

# Convert the result dates to post date strings in a specific format
post_date = [date.strftime("%Y-%m-%d") for date in result_dates]

# Extract Post URL
url_html = soup.find_all('div', {'class': 'feed-shared-update-v2'})

post_url = []

for each_url_tag in url_html:
    data_urn_attrb_value = "https://www.linkedin.com/feed/update/" + each_url_tag["data-urn"]
    post_url.append(data_urn_attrb_value)

# Extract author names
author_html = soup.select("div.pt1.mb2.artdeco-card > div > div > div.feed-shared-update-v2 > div > div.update-components-actor > div.update-components-actor__container > div.update-components-actor__meta > a > span.update-components-actor__title > span.update-components-actor__name > span > span:nth-of-type(1)")
 
author_name = []

for author in author_html:
    author_name.append(author.text.strip())
    
# Extract author title
title_html = soup.select("div.pt1.mb2.artdeco-card > div > div > div.feed-shared-update-v2 > div > div.update-components-actor > div.update-components-actor__container > div.update-components-actor__meta > a > span.update-components-actor__description > span:nth-of-type(1)")
 
author_title = []

for x in title_html:
    author_title.append(re.sub('\d+\,*\d+\Wfollowers','',x.text.strip()))
    
# Extract Author URL
author_url_html = soup.select("div.pt1.mb2.artdeco-card > div > div > div.feed-shared-update-v2 > div > div.update-components-actor > div.update-components-actor__container > div.update-components-actor__meta > a:nth-of-type(1)")

author_url = []

for each_url_tag in author_url_html:
    href_attrb_value = each_url_tag["href"]
    author_url.append(re.sub('\?.*','',href_attrb_value.strip()))

# Extract post text
post_text_html = soup.select("div.feed-shared-update-v2 > div > div:nth-of-type(4)")
    
post_text = []

for text in post_text_html:
	post_text.append(text.text.strip())
      
# Extract Engagements
engagement_html = soup.select("div.pt1.mb2.artdeco-card > div > div > div.feed-shared-update-v2 > div > div.update-v2-social-activity")

likes = []
comments = []
reposts = []

strip_engagements = '\scomments|\scomment|\sreposts|\srepost'

for x in engagement_html:
    likes.append(re.sub(r',', '', re.sub(r'\s+|like|Like', ' ', x.text.strip()).split(" ")[0]))
    comments.append(re.sub(r',', '', re.sub(strip_engagements, '', ''.join(re.findall('\d+\scomments|1\scomment', x.text.strip())))))
    reposts.append(re.sub(r',', '', re.sub(strip_engagements, '', ''.join(re.findall('(\d+\sreposts|1\srepost)', x.text.strip())))))

# Function to replace all blank values in a list with 0
def replace_blanks_with_zero(lst):
    return [0 if not item else item for item in lst]

# Replacing blank values in all three lists
likes = replace_blanks_with_zero(likes)
comments = replace_blanks_with_zero(comments)
reposts = replace_blanks_with_zero(reposts)

engagements = [int(a) + int(b) + int(c) for a, b, c in zip(likes, comments, reposts)]

# ----- Write Data to CSV -----

# Combine lists into single list
combined_data = [post_date, post_url, author_name, author_title, author_url, post_text, likes, comments, reposts, engagements]

# Set current timestamp
timestamp = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")

# Write list to CSV
with open('/Users/azntaiji/Downloads/' + search_query + "_" + str(timestamp) + '.csv', 'w', newline='') as file:
	writer = csv.writer(file)
	writer.writerow(['Post Date', 'Post URL', 'Author/Company Name', 'Author Title', 'Author/Company Profile URL', 'Post Text', 'Post Likes', 'Post Comments', 'Post Reposts', 'Total Engagements'])
	writer.writerows(zip(*combined_data))
     
print("File saved! Check downloads folder.")
