from argparse import ArgumentParser, Namespace
from bs4 import BeautifulSoup
import requests as req
import re

parser = ArgumentParser()

# parser.add_argument('-u', '--url', help = "Arguement for the URL", required= True)
# parser.add_argument('-t', '--thresh', help = "Threshold for the recursive function", type = int, required= True)
# parser.add_argument('-o', '--output', help = "Whether or not the content has to be written in a new file", action = "store_true")



# args :Namespace = parser.parse_args()

# url : str = args.url
# rthresh : int = args.thresh
html_req = req.get("https://www.geeksforgeeks.org/").text
soup = BeautifulSoup(html_req, "lxml")


for link in soup.find_all('a', 
						attrs={'href': re.compile("^https://")}): 
	# display the actual urls 
	print(link.get('href')) 
	
print('\n\n\n\n\n\n\n')
for link in soup.find_all('a', 
						attrs={'src': re.compile("^https://")}): 
	# display the actual urls 
	print(link.get('src')) 
# if args.output:
#     f = open('list_of_urls.txt', 'w')
#     f.write("hi")