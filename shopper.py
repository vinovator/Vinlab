# python 3
# shopper.py

'''
This is a very simple and effective program.
Open multiple shopping sites for one search parameter at one go
Search for a product term as a command prompt argument
Multiple words separated by space is fine
e.g. shooper.py iphone 6
'''

import sys
import webbrowser

amazon = "http://www.amazon.in/s/field-keywords="
flipkart = "http://www.flipkart.com/search?q="
snapdeal = "http://www.snapdeal.com/search?noOfResults=20&keyword="
junglee = "http://www.junglee.com/mn/search/junglee/ref=nav_sb_gw_noss?field-keywords="

if len(sys.argv) > 1:
    mysearch = " ".join(sys.argv[1:])
else:
    print("enter a search term")
    exit()

webbrowser.open(amazon + mysearch)
webbrowser.open(flipkart + mysearch)
webbrowser.open(snapdeal + mysearch)
webbrowser.open(junglee + mysearch)
