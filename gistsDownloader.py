# gistsDownloader.py
# Python 3.4


import requests

username = "vinovator"
url = "https://api.github.com/users/" + username + "/gists"

resp = requests.get(url)

gists = resp.json()

for gist in gists:
    for file in gist["files"]:
        fname = gist["files"][file]["filename"]
        furl = gist["files"][file]["raw_url"]
        print("{}:{}".format(fname, furl))

        pyresp = requests.get(furl)

        with open("../vinhub/vinlab/" + fname, "wb") as pyfile:
            for chunk in pyresp.iter_content(chunk_size=1024):
                if chunk:
                    pyfile.write(chunk)
        print("{} downloaded successfully".format(fname))
