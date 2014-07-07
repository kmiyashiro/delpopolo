# This is a template for a Python scraper on Morph (https://morph.io)
# including some code snippets below that you should find helpful

import scraperwiki
import lxml.html
import re
import datetime


# Read in a page
html = scraperwiki.scrape("http://www.delpopolosf.com/", None, "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-us) AppleWebKit/534.27+ (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27")

# Create tree
root = lxml.html.fromstring(html)


schedule = root.cssselect("#weekly_schedule")[0]

# Remove info paragraph
schedule.cssselect(".first")[0].drop_tree()

# Rest of paragraphs are schedule infos
days = schedule.cssselect("p")

# Remove non-numbers from day, like "th" from "May 30th"
non_number = re.compile(r'(\d)[^\d]+')

# Current year, all dates are current year
current_year = str(datetime.datetime.now().year)

# Data to save
data = []

for day in days:
  details = {}
  # Get day text "May 30th"
  day_text = day.cssselect("strong")[0].text_content()
  day_text = non_number.sub("\g<1>", day_text) + " " + current_year

  time_place_text = day.cssselect("em")[0].text_content()
  time_text = time_place_text.split("@")[0].strip()
  place_text = time_place_text.split("@")[1].strip()

  map_link = day.cssselect("a")[0].get("href")

  date_time_text = day_text + ' ' + time_text

  details["location"] = place_text
  details["map_link"] = map_link

  # Convert day to date
  try:
    day_date = datetime.datetime.strptime(date_time_text, "%A, %B %d %Y %I:%M %p")
    details["date"] = day_date.isoformat()
  except ValueError as e:
    print 'Failed to format date'

  if details.has_key("date"):
    data.append(details)

for datum in data
  print datum

# Write out to the sqlite database using scraperwiki library
scraperwiki.sqlite.save(unique_keys=['date'], data=data)
