import requests
from bs4 import BeautifulSoup
payload = {'page':2, "count":50}
img_req = requests.get("https://www.google.com")
print(img_req.url)