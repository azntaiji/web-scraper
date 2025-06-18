# Version 2.0.0

# ----- Import dependencies -----
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pandas as pd
import csv
import time
import re

# ----- Search Query -----

# Query user for search term
search_query = input("Enter search term:\n")

# ----- Data Scraping -----

# open test file pass to BS
with open('/Users/azntaiji/seafile/Developer/python/web-scraper/sample_data/test-page.html', 'r') as file:
    soup = BeautifulSoup(file, 'lxml')

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
        like_count = re.sub(r'(\d+).*', r'\1', likes.get_text(strip=True), flags=re.IGNORECASE)
    else:
        like_count = 0

    if comments:
        comment_count = re.sub(r'^(.*?)\s.*', r'\1', comments.get_text(strip=True), flags=re.IGNORECASE)
    else:
        comment_count = 0

    if reposts:
        repost_count = re.sub(r'^(.*?)\s.*', r'\1', reposts.get_text(strip=True), flags=re.IGNORECASE)
    else:
        repost_count = 0

    engagements = int(like_count) + int(comment_count) + int(repost_count)

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

# Set current timestamp
timestamp = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")

# set filename and export to excel
filename = '/Users/azntaiji/Downloads/' + search_query + "_" + str(timestamp) + '.xlsx'
df.to_excel(filename, index=False)

print("File saved! Check downloads folder.")