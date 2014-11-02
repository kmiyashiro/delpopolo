# This is a template for a Python scraper on Morph (https://morph.io)
# including some code snippets below that you should find helpful

import scraperwiki
import lxml.html
import re
import datetime
import logging

logging.basicConfig(level='DEBUG')

# Read in a page
html = scraperwiki.scrape("http://www.delpopolosf.com/", None, "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-us) AppleWebKit/534.27+ (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27")

# Test page
html = open('test/fixture.html').read()

# Remove non-numbers from day, like "th" from "May 30th"
non_number = re.compile(r'(\d)[^\d]+')

# Current year, all dates are current year
current_year = str(datetime.datetime.now().year)

def get_day_elements(html_string):
  # Create tree
  root = lxml.html.fromstring(html_string)
  schedule = root.cssselect("#locations")[0]

  # Remove info paragraph
  schedule.cssselect(".first")[0].drop_tree()

  # Rest of paragraphs are schedule infos
  return schedule.cssselect("p")

# Get day text "May 30th"
def get_day_text(day_element):
  day_text = day.cssselect("strong")[0].text_content()
  return non_number.sub("\g<1>", day_text) + " " + current_year

def get_time_text(day_element):
  time_place_text = _get_time_place_text(day_element)
  return time_place_text.split("@")[0].strip()

def get_date_time_text(day_element):
  return get_day_text(day_element) + ' ' + get_time_text(day_element)

def get_place_text(day_element):
  time_place_text = _get_time_place_text(day_element)
  return time_place_text.split("@")[1].strip()

def get_map_link(day_element):
  return day.cssselect("a")[0].get("href")

def _get_time_place_text(day_element):
  return day_element.cssselect("em")[0].text_content()

# Data to save
data = []

days = get_day_elements(html)

for day in days:
  details = {}

  details["location"] = get_place_text(day)
  details["map_link"] = get_map_link(day)

  # Convert day to date
  try:
    date_time_text = get_date_time_text(day)
    day_date = datetime.datetime.strptime(date_time_text, "%A, %B %d %Y %I:%M %p")
    details["date"] = day_date.isoformat()
  except ValueError as e:
    logging.warning('Failed to format date')

  if details.has_key("date"):
    data.append(details)

for datum in data:
  logging.info(datum)

# Write out to the sqlite database using scraperwiki library
scraperwiki.sqlite.save(unique_keys=['date'], data=data)
