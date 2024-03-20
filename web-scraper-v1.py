# ----- Import dependencies -----

from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import time
import re

current_date_time = datetime.now()
current_date = current_date_time.date()

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
    search_query = re.sub(old,new,search_query).lower()

# Concatenate search URL and search query
search_url = 'https://www.linkedin.com/search/results/content/?keywords=' + search_query + "&origin=FACETED_SEARCH&sid=_HP&sortBy=%22date_posted%22"

# ----- Login to LinkedIn with selenium webdriver -----

# Create webdriver instance
driver = webdriver.Chrome()

# Open linkedIn's login page
driver.get("https://www.linkedin.com/login")

# Wait for the page to load
time.sleep(2)

# entering username
username = driver.find_element(By.ID, "username")

# Enter Your Email Address
username.send_keys("zach@azntaiji.com") 

# entering password
pword = driver.find_element(By.ID, "password")

# Enter Your Password
pword.send_keys("taijisan")	 

# Click on the log in button
driver.find_element(By.XPATH, "//button[@type='submit']").click()

time.sleep(15)

# ----- Open feed of search query -----

# Open link
driver.get(search_url) 

# Scroll to bottom
start = time.time()

# will be used in the while loop
initialScroll = 0
finalScroll = 4000

while True:
	driver.execute_script(f"window.scrollTo({initialScroll},{finalScroll})")
	# this command scrolls the window starting from
	# the pixel value stored in the initialScroll 
	# variable to the pixel value stored at the
	# finalScroll variable
	initialScroll = finalScroll
	finalScroll += 4000

	# we will stop the script for 3 seconds so that 
	# the data can load
	time.sleep(5)
	# You can change it as per your needs and internet speed

	end = time.time()

	# We will scroll for 20 seconds.
	# You can change it as per your needs and internet speed
	if round(end - start) > 5:
		break
      
# ----- Extract Data -----
	
# Extract data from entire page
search_src = driver.page_source # This gets the source code of the current page
soup = BeautifulSoup(search_src, 'lxml') # This sets var soup

# Extract post dates
date_html = soup.select("div.update-components-actor--with-control-menu span.update-components-actor__sub-description div span > span:nth-of-type(1)")
 
post_date = []
 
for date in date_html:
    post_date.append(re.sub(r'\s•.*','',date.text.strip()))

# Extract Post URL
url_html = soup.find_all('div', {'class': 'feed-shared-update-v2'})

post_url = []

for each_url_tag in url_html:
      data_urn_attrb_value = "https://www.linkedin.com/feed/update/" + each_url_tag["data-urn"]
      post_url.append(data_urn_attrb_value)

# Extract author names
author_html = soup.select("div.update-components-actor--with-control-menu span.update-components-actor__name > span:nth-of-type(1)")
 
author_name = []

for author in author_html:
    author_name.append(author.text.strip())
    
# Extract author title
title_html = soup.select("div.update-components-actor--with-control-menu span.update-components-actor__description > span:nth-of-type(1)")
 
author_title = []

for x in title_html:
    author_title.append(re.sub('\d+\,*\d+\Wfollowers','',x.text.strip()))
    
# Extract company followers
followers_html = soup.select("div.update-components-actor--with-control-menu span.update-components-actor__description > span:nth-of-type(1)")
 
company_followers = []

for x in followers_html:
    company_followers.append(
          re.sub('(^\D*)','',x.text.strip().split("followers")[0]))
    
# Extract Author URL
author_url_html = soup.select("div.update-components-actor--with-control-menu div.update-components-actor__container > a:nth-of-type(1)")

author_url = []

for each_url_tag in author_url_html:
    href_attrb_value = each_url_tag["href"]
    author_url.append(re.sub('\?.*','',href_attrb_value.strip()))
    
# Extract post text
    
post_text_html = soup.select("div.feed-shared-update-v2__description-wrapper > div > div.update-components-text > span.break-words > span")
    
post_text = []

for text in post_text_html:
	post_text.append(text.text.lower().strip())
      
# Extract Engagements
      
engagement_html = soup.select("div.social-details-social-counts > div > div > ul")

likes = []
comments = []
reposts = []

strip_engagements = '\scomments|\scomment|\sreposts|\srepost'

for x in engagement_html:
      likes.append(re.sub(r'\s+', ' ', x.text.strip()).split(" ")[0])
      comments.append(re.sub(strip_engagements, '', ''.join(re.findall('\d+\scomments|1\scomment', x.text.strip()))))
      reposts.append(re.sub(strip_engagements, '', ''.join(re.findall('(\d+\sreposts|1\srepost)', x.text.strip()))))

# ----- Write Data to CSV -----

# Combine arrays
combined_data = [post_date, post_url, author_name, author_title, author_url, company_followers,post_text, likes, comments, reposts]
print(combined_data)

# Write to CSV
with open('/Users/azntaiji/Downloads/' + str(current_date) + '_' + search_query + '.csv', 'w', newline='') as file:
	writer = csv.writer(file)
	writer.writerow(['Post Date','Post URL','Author/Company Name','Author Title','Author/Company Profile URL','Company Followers','Post Text','Post Likes','Post Comments','Post Reposts'])
	writer.writerows(zip(*combined_data))