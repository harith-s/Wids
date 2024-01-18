from argparse import ArgumentParser, Namespace
from bs4 import BeautifulSoup
import requests as req
import time

# the depth of recurrsion is thresh

thresh = 2

# function to get html data from a url

def getHTML(url):
    html_req = req.get(url).text
    return BeautifulSoup(html_req, "lxml")

def create_list(empty_list, thresh):
    for i in range(thresh):
        empty_list.append([])
    return empty_list

#sorts the list which contains all types of links into html, js, css, etc

def sorter(list):
    dict = {'html' : [], 'java': [], 'css': [], 'jpg':[], 'others': []}
    for link in list:
        if '.html' in link: 
            dict['html'].append(link)
        elif '.js' in link: 
            dict['java'].append(link)
        elif '.css' in link: 
            dict['css'].append(link)
        elif '.jpg' in link: 
            dict['jpg'].append(link)
        else:
            dict['others'].append(link)
    return dict
    
# function to print the dictionary
    
def dict_print(dic):
    for tag in dic:
        print(tag.title(), ": ")

        # dic[i] is a list which contains all links of a particular type
        for link in dic[tag]:
            print(link)

def list_print(list):
    for index, dict in enumerate(list):
        if index == recur_level -1:
            print(f"Printing only till recursive level {recur_level-1}")
            break    
        dict_print(dict)
            
        print(f"Done printing level {index + 1} of recursion")
        print("Moving onto next level...")
        time.sleep(2)


url = "https://www.geeksforgeeks.org/"
sample_lambda = lambda link : 1 if url in link else 0
soup = getHTML(url)

list_src_int = []
list_src_ext = []

# list_src_int - has dictionaries of src links, index + 1 is the level of recurrsion, domain same as url
# list_src_ext - has dictionaries of src links, index + ! gives the level of recursion, domain same as url

create_list(list_src_ext, thresh)
create_list(list_src_int, thresh)

# list_src_master simply has both int and ext just for the lambda

list_src_master = [list_src_ext,  list_src_int] 

list_src_tags = ['script', 'img', 'audio', 'embed', 'iframe', 'form', 'video', 'track', 'source', 'input']


for recur_level in range(1, thresh + 1):
    if recur_level ==1:
        soup = getHTML(url)
        for line in soup.find_all(list_src_tags):

            # if the link has the domain in it, it will return a 1, the index of int list

            link = line.get("src")

            if link!= None:
                if url in link:
                    list_src_int[0].append(link)
                else:
                    list_src_ext[0].append(link)
    

        list_src_int[0] : dict = sorter(list_src_int[0])
        list_src_ext[0] : dict = sorter(list_src_ext[0])


    elif len(list_src_int[recur_level - 2]['html']) != 0:

        # only selecting the html tags
        for link_int in list_src_int[recur_level - 2]['html']: #going through the html list in the last recursive step
            soup = getHTML(link_int)
            for line in soup.find_all(list_src_tags):
                link = line.get("src")

                if link!= None:
                    if url in link:
                        list_src_int.append(link)
                    else:
                        list_src_ext.append(link)
    else:
        print(f'breaking at recursion level  {recur_level} due to inavailabilty of html pages')
    
        
        list_src_int[recur_level - 1] : dict = sorter(list_src_int[recur_level - 1])
        list_src_ext[recur_level -1] : dict = sorter(list_src_ext[recur_level -1])
 
list_print(list_src_int)
list_print(list_src_ext)


