# python 3
# Cricinfoscraper.py

"""
Simple webscraper to download cartoons from cricinfo site.
The url is http://www.espncricinfo.com/ci/content/story/author.html?author=333
TODO: The page is javascript rendered, hence only few strips get downloaded.
Change the code to dynamically scroll the page to fetch more cartoons.
Tip - use phantomJs to scroll the page down.
"""


import requests
from bs4 import BeautifulSoup
import os

base_url = "http://www.cricinfo.com/"

# This is the folder where the cartoon strips get downloaded
base_folder = "cricinfo"
os.makedirs(base_folder, exist_ok=True)

# This is the url for cartoons page
resp = requests.get(
    "http://www.espncricinfo.com/ci/content/story/author.html?author=333")

soup = BeautifulSoup(resp.content, "lxml")

cartoon_div = soup.find_all("div", {"class": "story-imgwrap"})

for tag in cartoon_div:
    attrs = tag.find_all("img", {"class": "img-full"})
    for attr in attrs:
        src = attr.get("src")
        alt = attr.get("alt")  # Not used
        title = attr.get("title")  # Not used

        # The filename of the cartoon is formatted to indicate preview.
        # for e.g. filename is of format ddddddd.x.jpg.
        # The .x.jpg is format indicates preview image
        # strip the last digit following a dot to get full image

        src = src.split(".")[0] + ".jpg"

        cartoon_resp = requests.get(base_url + src, "lxml")

        try:
            with open("cricinfo/" + src.split("/")[-1], "wb") as cartoon:
                for chunk in cartoon_resp.iter_content(chunk_size=1024):
                    if chunk:
                        cartoon.write(chunk)
            print("Cartoon strip {} downloaded".format(src.split("/")[-1]))
        except Exception as e:
            print(e)
            continue
