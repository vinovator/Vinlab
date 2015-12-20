# Python 3
# XKCDDownloader.py
########################################################################################################################
# Algorithm
# 1) Open the latest page of XKCD
# 2) Download the image, title and alternate text from the page and save the images in specified folder
# 3) Build a html file which contains the alt, title and src in a html file
# 4) If any error in download skip the page
# 5) Find the previous page url from current page and repeat steps 2, 3 & 4
# 6) Continue until you find the very 1st comic

# file title format - val + "-" + alt
# val - unique number in the url of each comic page
# alt - title of each comic
########################################################################################################################

import requests
import bs4
import os


# Folder name to contain all comic images and html file
comicPath = "XKCD"

# For the very 1st comic, the "prev" attribute carries the value "#". Indicates end of loop
endChar = "#"


def write_html(text):
    # TODO: Unicode characters will be printed as gibberish. Find an elegant solution
    with open(os.path.join(comicPath, "xkcd" + ".html"), "a", encoding="utf-8") as xkcdHtmlFile:
        xkcdHtmlFile.write(text)


def build_block(alt, title, src):
    block = "<tr><td>"
    block += "<head><b>" + alt + "</b></head>"
    block += "<p></P>"
    block += "<img src=" + "\"" + src + "\"" + ">"
    block += "<body><p><i>" + title + "</i></p></body>"
    block += "<p></P>"
    block += "<p>-----------------------</p>"
    block += "</td></tr>"
    return block


def download_image(pageUrl):
    # Create a folder under the root folder called "XKCD". If already exists, ignore
    os.makedirs(comicPath, exist_ok=True)

    print("Downloading comic from " + pageUrl)
    imgResponse = requests.get(pageUrl)
    imgSoup = bs4.BeautifulSoup(imgResponse.text)

    imgLinks = imgSoup.find_all("div", {"id": "comic"})

    for tag in imgLinks:
        attrs = tag.find_all("img")
        for attr in attrs:
            alt = attr.get("alt")
            src = attr.get("src")
            title = attr.get("title")

    baseUrl, pageNum = pageUrl.split("/")[-3:-1]

    #print("base url: {0}, pageNum: {1}".format(baseUrl, pageNum))

    # Download the comic image in png format and save it in specific folder
    pngRes = requests.get("http:" + src)
    with open(os.path.join(comicPath, pageNum + " " + alt + ".png"), "wb") as xkcdFile:
        for chunk in pngRes.iter_content(1024):
            xkcdFile.write(chunk)
        print("XKCD comic downloaded at path {0}".format(os.path.join(comicPath, pageNum + " " + alt + ".png")))

    # Define global variable which is used to construct the html file with all XKCD comics
    htmlBlockString = ""

    # Build the html block string for thie iteration of comic
    htmlBlockString += build_block(alt, title, pageNum + " " + alt + ".png")

    # Append the html file with the specific block of current loop's comic strip
    write_html(htmlBlockString)

    print("html block constructed for {0} {1}".format(pageNum, alt))


def navigate_url(myUrl, baseUrl, comicCounter):
    print("comic number: ", comicCounter)
    # Get the response object from the url
    myResponse = requests.get(myUrl)

    # Pass the text of the response object to beautifulsoup
    mySoup = bs4.BeautifulSoup(myResponse.text)
    myLinks = mySoup.find_all("a", {"rel": "prev"})

    prevList = list()

    for link in myLinks:
        prevList.append(link.get("href"))

    # XKCD has 2 placeholders for "prev" links. Use set to extract distinct values from list
    imgSet = set(prevList)
    for val in imgSet:
        while val != endChar:
            download_image((baseUrl + val))
        #while comicCounter < 10:
            comicCounter += 1
            # return statement is important for recursive functions, otherwise infinite loop
            return navigate_url(baseUrl + val, baseUrl, comicCounter)


def main():
    myUrl = "http://www.xkcd.com"
    baseUrl = myUrl

    # Start the construction of html file
    write_html("<html>")

    # TODO: download_image function extracts pageNum variable which will be blank for the latest page. Explore
    # Download the image from the latest url first
    #download_image(myUrl)

    # Navigate to the previous comic url and then continue the process
    navigate_url(myUrl, baseUrl, comicCounter = 0)

    # Complete the construction of html file
    write_html("</html>")

    print("XKCD html file created at path {0}".format(os.path.join(comicPath, "xkcd" + ".html")))
    print("--------------Done---------------------")


if __name__ == "__main__":
    main()
