import re

# Create post_date list with sample data 
post_date = ['1d •', '2d • Edited •', '3d •', '4d • Edited •', '5d •', '6d •', '7d •', '1w •', '2w •', '3w • Edited •', '4w •', '1mo • Edited •', '2mo •', '1y • Edited •']

trimmed_dates = [re.sub(r'\s•.*','',date) for date in post_date]

print(trimmed_dates)

converted_dates = [re.sub(r'd','',date) for date in trimmed_dates]

print(converted_dates)