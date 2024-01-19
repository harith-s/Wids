import requests
from bs4 import BeautifulSoup
import time

def getHTML(url):
    html_req = requests.get(url).text
    return BeautifulSoup(html_req, "lxml")

list_href_int = []
list_href_ext = []
thresh = 1


url = "https://www.iitb.ac.in"
sample_lambda = lambda link : 1 if url in link else 0
soup = getHTML(url)


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


def dict_print(dic):

    for tag in dic:
        print(tag.title(), ": ")

        # dic[i] is a list which contains all links of a particular type
        for link in dic[tag]:
            print(link)


def list_print(list_, recur_level):
    index = 0
    for dict in list_:
        if index >= recur_level:
            print(f"Printing only till recursive level {recur_level}")
            break    
        input('what the flip is happeneing')
        dict_print(dict)
            
        print(f"Done printing level {index + 1} of recursion")
        print("Moving onto next level...")
        index += 1
        time.sleep(0.5)

def create_list(empty_list, thresh):
    for i in range(thresh):
        empty_list.append([])
    return empty_list

# list_src_int - has dictionaries of src links, index + 1 is the level of recurrsion, domain same as url
# list_src_ext - has dictionaries of src links, index + ! gives the level of recursion, domain same as url

'''create_list(list_href_ext, thresh)
create_list(list_href_int, thresh)

# list_src_master simply has both int and ext just for the lambda


for recur_level in range(1, thresh + 1):
    if recur_level == 1:
        soup = getHTML(url)
        for line in soup.find_all('a'):

            # if the link has the domain in it, it will return a 1, the index of int list

            link = line.get("href")

            if link!= None:
                if url in link:
                    list_href_int[0].append(link)
                else:
                    list_href_ext[0].append(link)

        list_href_int[0] : dict = sorter(list_href_int[0])
        list_href_ext[0] : dict = sorter(list_href_ext[0])
        
        time.sleep(3)

    elif len(list_href_int[recur_level - 2]['html']) != 0:

        # only selecting the html tags
        for link_int in list_href_int[recur_level - 2]['html']: #going through the html list in the last recursive step
            soup = getHTML(link_int)
            for line in soup.find_all('a'):
                link = line.get("href")

                if link!= None:
                    if url in link:
                        list_href_int.append(link)
                    else:
                        list_href_ext.append(link)
    else:
        print(f'breaking at recursion level  {recur_level} due to inavailabilty of html pages')
    
        
        list_href_int[recur_level - 1] : dict = sorter(list_href_int[recur_level - 1])
        list_href_ext[recur_level -1] : dict = sorter(list_href_ext[recur_level -1])
 
list_print(list_href_int)
list_print(list_href_ext)
'''
# function to print based on threshold

def getlinks_t(url, list_int, list_ext, thresh, link_type, tag, set_links):

    
    create_list(list_ext, thresh)
    create_list(list_int, thresh)

    # list_src_master simply has both int and ext just for the lambda

    for recur_level in range(1, thresh + 1):
        lsize_bool = len(list_int[recur_level -1]) <= 20
        if recur_level == 1:
            # print("hi")
            soup = getHTML(url)
            # print(soup)
            for line in soup.find_all(tag):

                # if the link has the domain in it, it will return a 1, the index of int list

                link = line.get(link_type)

                if link!= None and link not in set_links and lsize_bool:
                    if url in link:
                        list_int[0].append(link)
                        set_links.update(link)
                    else:
                        list_ext[0].append(link)
                        set_links.update(link)
            # print(list_int)
            list_int[0] : dict = sorter(list_int[0])
            list_ext[0] : dict = sorter(list_ext[0])

            # print(list_int[0])
            # input("oh so this is what is causing the problem")

            # print(list_int[0])
            
            # input("hit enter to proceed")


        elif len(list_int[0]['html']) != 0:

            # only selecting the html tags
            # input("hi >>")

            # print((list_int[0]))
            # input("Now this is the int list")
            
            for link_int in list_int[recur_level - 2]['html']: #going through the html list in the last recursive step
                # # input("hi once again")
                # print(link_int)
                soup = getHTML(link_int)


                for line in soup.find_all('a'):
                    link = line.get("href")

                    if link!= None and link not in set_links and lsize_bool:
                        if url in link:
                            list_int[recur_level -1].append(link)
                            set_links.update(link)
                        else:
                            list_ext[recur_level -1].append(link)
                            set_links.update(link)
            list_int[recur_level - 1] : dict = sorter(list_int[recur_level - 1])
            list_ext[recur_level -1] : dict = sorter(list_ext[recur_level -1])

        else:
            print(f'breaking at recursion level  {recur_level} due to inavailabilty of html pages')
        
            
        
        # print('hiiiiiiiiiiii')
        # input("enter to proveed")
    
    list_print(list_int, recur_level)
    list_print(list_ext, recur_level)
    return set_links


# function when the threshhold is not mentioned
    
def getlinks(url, list_int, list_ext, tag, link_type):

    create_list(list_ext, thresh)
    create_list(list_int, thresh)

    soup = getHTML(url)
    for line in soup.find_all(tag):

    # if the link has the domain in it, it will return a 1, the index of int list
        link = line.get(link_type)

        if link!= None:
            if url in link:
                list_int[0].append(link)
            else:
                list_ext[0].append(link)

        list_int[0] : dict = sorter(list_int[0])
        list_ext[0] : dict = sorter(list_ext[0])
        
        recur_level = 2


        while len(list_int[recur_level - 2]['html']) != 0:


            # only selecting the html tags
            for link_int in list_int[recur_level - 2]['html']: 
                #going through the html list in the last recursive step
                # input("hi >> ")
                soup = getHTML(link_int)
                for line in soup.find_all('a'):
                    link = line.get("href")

                    if link!= None:
                        if url in link:
                            list_int.append(link)
                        else:
                            list_ext.append(link)

                list_int[recur_level - 1] : dict = sorter(list_int[recur_level - 1])
                list_ext[recur_level -1] : dict = sorter(list_ext[recur_level -1])
                recur_level += 1
            
            
            
    
    list_print(list_int, recur_level)
    list_print(list_ext, recur_level)


list_int = list_href_int
list_ext = list_href_ext
link_type = "href"
tag = 'a'
set_links = {url}
set_final = getlinks_t(url, list_int, list_ext, 2, link_type, tag, set_links)