import urllib.request
import re
import webbrowser

sentinel = 'done' # ends when this string is seen
for line in iter(input, sentinel):
    url = urllib.request.urlopen(line)
    sub = "a href=\"/deck/"
    string=url.read().decode("utf-8")
    for match in re.finditer(sub, string):
        down = "https://www.mtggoldfish.com/deck/download/"+string[match.end():match.end()+7]
        webbrowser.open(down)