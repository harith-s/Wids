from argparse import ArgumentParser, Namespace
from bs4 import BeautifulSoup
import requests 
import time

# the depth of recurrsion is thresh

thresh = 2
url = "https://www.timesjobs.com/"


def create_list(empty_list, thresh):
    for i in range(thresh):
        empty_list.append([])
    return empty_list

# sorts the list which contains all types of links into html, js, css, etc

def sorter(list_):
    dict = {'html' : set(), 'java': set(), 'css': set(), 'jpg':set(), 'others': set()}
    for link in list_:
        if '.html' or 'http' in link: 
            dict['html'].add(link)
        elif '.js' in link: 
            dict['java'].add(link)
        elif '.css' in link: 
            dict['css'].add(link)
        elif '.jpg' in link: 
            dict['jpg'].add(link)
        else:
            dict['others'].add(link)

    
    return dict
    
# function to print the dictionary
    
def dict_print(dic):
    file_no = 0
    for tag in dic:
        file_no += len(dic[tag])
    
    print(f"Total number of files found : {file_no}")
        
    for tag in dic:

        print(tag.title(), ": ", len(dic[tag]))

        # dic[i] is a list which contains all links of a particular type

        for link in dic[tag]:
            print(link)

def list_print(list_, recur_level):
    index = 0
    for dict in list_:
        if index >= recur_level:
            print(f"Printing only till recursive level {recur_level}")
            break    
        print(f"Recursion level : {index + 1}")
        dict_print(dict)

        print("Moving onto next level...")
        index += 1
        time.sleep(0.5)




list_src_int = []
list_src_ext = []
list_href_int = []
list_href_ext = []
list_int = []
list_ext = []

# list_src_int - has dictionaries of src links, index + 1 is the level of recurrsion, domain same as url
# list_src_ext - has dictionaries of src links, index + ! gives the level of recursion, domain same as url
 

list_src_tags = ['script', 'img', 'audio', 'embed', 'iframe', 'form', 'video', 'track', 'source', 'input']


# function called when the threshold is mentioned

def getlinks_t(url, list_int, list_ext, thresh, link_type, tag, set_links):

    
    create_list(list_ext, thresh)
    create_list(list_int, thresh)

    # list_src_master simply has both int and ext just for the lambda

    for recur_level in range(1, thresh + 1):

        lsize_bool = len(list_int[recur_level -1]) <= 20

        if recur_level == 1:

            # using with block to close connection automatically

            with requests.get(url, stream=True) as html_req:

                soup = BeautifulSoup(html_req.text, "lxml")
                for line in soup.find_all(tag):

                    # if the link has the domain in it, it will return a 1, the index of int list

                    link = line.get(link_type)

                    # putting a contraint on the number of links to not overload web server and to reduce processing time

                    if link!= None and link not in set_links and len(list_int[0]) <20:
                        if url in link:
                            list_int[0].append(link)
                            set_links.update(link)

                        else:
                            list_ext[0].append(link)
                            set_links.update(link)
                
                # sorts the links into dictionaries

                list_int[0] : dict = sorter(list_int[0])
                list_ext[0] : dict = sorter(list_ext[0])


        elif len(list_int[0]['html']) != 0:

            # only selecting the html tags
            
            for link_int in list_int[recur_level - 2]['html']: #going through the html list in the last recursive step

                with requests.get(url, stream=True) as html_req:

                    soup = BeautifulSoup(html_req.text, "lxml")


                    for line in soup.find_all('a'):
                        link = line.get("href")
                        
                        if link!= None and link not in set_links and len(list_int[recur_level -1]) <20:
                            if url in link:
                                list_int[recur_level -1].append(link)
                                set_links.update(link)
                            else:
                                list_ext[recur_level -1].append(link)
                                set_links.update(link)

            list_int[recur_level - 1] : dict = sorter(list_int[recur_level - 1])
            list_ext[recur_level -1] : dict = sorter(list_ext[recur_level -1])

        else:

            # in case there are no more html pages to reference, but recursive threshold hasn't been reached

            print(f'breaking at recursion level  {recur_level} due to inavailabilty of html pages')
    
    # list_print(list_int, recur_level)
    # list_print(list_ext, recur_level)

    # returning a set which has all links

    return set_links, list_int, list_ext, recur_level


set_links = {url}
set_links, list_int, list_ext, main_recur_level = getlinks_t(url, list_href_int, list_href_ext, thresh, "href", 'a', set_links)
set_links,temp_int, temp_ext, dummy= getlinks_t(url, list_src_int, list_src_ext, thresh, "src", list_src_tags, set_links)

for i in range(len(list_int)):
    for key in list_int[i]:
        list_int[i][key].union(temp_int[i])
print(len(list_ext), "length of ext list")
for i in range(len(list_ext)):
    print("hi")
    for key in list_ext[i]:
        # print(temp_ext[i])
        if i < dummy - 1:
            list_ext[i][key].union(temp_ext[i][key])

    
