from argparse import ArgumentParser, Namespace
from bs4 import BeautifulSoup
import requests
import time
import csv

start = time.time()

global max_recursion_level 
global max_no_of_links

max_recursion_level = 3
max_no_of_links = 20

print(f"Maximum number of links requested at any particular level : {max_no_of_links}")

parser = ArgumentParser()

parser.add_argument('-u', '--url', help = "Arguement for the URL", required= True)
parser.add_argument('-t', '--thresh', help = "Threshold for the recursive function", type = int)
parser.add_argument('-o', '--output', help = "Whether or not the content has to be written in a new file", action = "store_true")

# the depth of recurrsion is thresh

args :Namespace = parser.parse_args()

url : str = args.url
thresh : int = args.thresh

if thresh != None and thresh < 0:
    print("Invalid choice for threshold. Program exiting.")
    exit()

def create_list(empty_list, thresh):
    for i in range(thresh):
        empty_list.append([])
    return empty_list

# sorts the list which contains all types of links into html, js, css, etc

def sorter(list_):
    dict = {'html' : set(), 'java': set(), 'css': set(), 'jpg':set(), 'png': set(), 'others': set()}
    for link in list_:
        if '.js' in link: 
            dict['java'].add(link)
        elif '.css' in link: 
            dict['css'].add(link)
        elif '.jpg' in link: 
            dict['jpg'].add(link)
        elif '.png' in link: 
            dict['png'].add(link)
        elif ('.html' or 'http')  and not('.gif' in link): 
            dict['html'].add(link)
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

        
        index += 1
        if index != recur_level:
            print("Moving onto next level...")
        time.sleep(0.5)

def list_write(list_, recur_level, file_object):
    index = 0
    for dict in list_:
        if index >= recur_level:
            file_object.write(f"Printing only till recursive level {recur_level}")
            break    
        file_object.write(f"Recursion level : {index + 1}")
        file_object.write("\n")
        dict_write(dict, file_object)

        
        index += 1
        time.sleep(0.5)
        
def dict_write(dic, file_object):
    file_no = 0
    for tag in dic:
        file_no += len(dic[tag])
    
    file_object.write(f"Total number of files found : {file_no}")
    file_object.write("\n")

        
    for tag in dic:

        file_object.write(f"{tag.title()} :  {len(dic[tag])}")
        file_object.write("\n")

        # dic[i] is a list which contains all links of a particular type

        for link in dic[tag]:
            file_object.write(link)
            file_object.write('\n')
            

list_int = []
list_ext = []

# list_int - has dictionaries of all links, index + 1 is the level of recurrsion, domain same as url
# list_ext - has dictionaries of all links, index + 1 gives the level of recursion, domain different from url


# function called when the threshold is mentioned

def getlinks_t(url, list_int, list_ext, thresh, set_links):

    # creating a list which has empty lists in which links will be put
    
    create_list(list_ext, thresh)
    create_list(list_int, thresh)

    for recur_level in range(1, thresh + 1):

        if recur_level == 1:

            # using with block to close connection automatically

            with requests.get(url, stream=True) as html_req:

                soup = BeautifulSoup(html_req.text, "lxml")
                for line in soup.find_all('a'):

                    # if the link has the domain in it, it will return a 1, the index of int list

                    link = line.get("href")

                    # putting a contraint on the number of links to not overload web server and to reduce processing time

                    if link!= None and link != '' and link not in set_links and len(list_int[0]) < max_no_of_links:
                        if url in link:
                            list_int[0].append(link)
                            # set_links has all the links, so in all cases, all links are added here.
                            set_links.add(link)

                        else:
                            list_ext[0].append(link)
                            set_links.add(link)

                # list_src_tags has all the potential tags which can have src tag 
                            
                list_src_tags = ['script', 'img', 'audio', 'embed', 'iframe', 'form', 'video', 'track', 'source', 'input']
                for line in soup.find_all(list_src_tags):

                    # if the link has the domain in it, it will return a 1, the index of int list

                    link = line.get("src")

                    # putting a contraint on the number of links to not overload web server and to reduce processing time

                    if link!= None and link != '' and link not in set_links and len(list_int[0]) < 2 * max_no_of_links:
                        if url in link:
                            list_int[0].append(link)
                            set_links.add(link)

                        else:
                            list_ext[0].append(link)
                            set_links.add(link)
                
                # sorts the links into dictionaries of sets

                list_int[0] : dict = sorter(list_int[0])
                list_ext[0] : dict = sorter(list_ext[0])
                time.sleep(0.5)


        elif len(list_int[recur_level - 2]['html']) != 0:

            # only selecting the html tags
            
            for link_int in list_int[recur_level - 2]['html']: #going through the html list in the last recursive step

                with requests.get(link_int, stream=True) as html_req:

                    soup = BeautifulSoup(html_req.text, "lxml")

                    for line in soup.find_all('a'):
                        link = line.get("href")
                        
                        if link!= None and link != '' and link != '' and link not in set_links and len(list_int[recur_level -1]) < max_no_of_links:
                            if url in link:
                                list_int[recur_level -1].append(link)
                                set_links.add(link)
                            else:
                                list_ext[recur_level -1].append(link)
                                set_links.add(link)

                    for line in soup.find_all(list_src_tags):
                        link = line.get("src")
                        
                        if link!= None and link != '' and link not in set_links and len(list_int[recur_level -1]) < max_no_of_links:
                            if url in link:
                                list_int[recur_level -1].append(link)
                                set_links.add(link)
                            else:
                                list_ext[recur_level -1].append(link)
                                set_links.add(link)

            list_int[recur_level - 1] : dict = sorter(list_int[recur_level - 1])
            list_ext[recur_level -1] : dict = sorter(list_ext[recur_level -1])
            time.sleep(0.5)

        else:

            # in case there are no more html pages to reference, but recursive threshold hasn't been reached
            recur_level = recur_level -1
            print(f'breaking at recursion level {recur_level} due to inavailabilty of html pages')
            break

    # returning a set which has all links

    return set_links, list_int, list_ext, recur_level

def getlinks_no_thresh(url, list_int, list_ext, set_links):

    
    list_ext =[[]]
    list_int = [[]]
    
    # flag as a variable to check where the flow of the program is

    flag = 0


    while True:
        
        recur_level = 2
        
        # using 'with block' to close connection automatically to avoid inefficiencies

        if flag == 0:
            with requests.get(url, stream=True) as html_req:

                soup = BeautifulSoup(html_req.text, "lxml")

                for line in soup.find_all('a'):

                    link = line.get("href")

                    # putting a contraint on the number of links to not overload web server and to reduce processing time

                    if link!= None and link != '' and link not in set_links and len(list_int[0]) <max_no_of_links:
                        if url in link:
                            list_int[0].append(link)
                            set_links.add(link)

                        else:
                            list_ext[0].append(link)
                            set_links.add(link)

                list_src_tags = ['script', 'img', 'audio', 'embed', 'iframe', 'form', 'video', 'track', 'source', 'input']

                for line in soup.find_all(list_src_tags):

                        link = line.get("src")

                        if link!= None and link != '' and link not in set_links and len(list_int[0]) <40:
                            if url in link:
                                list_int[0].append(link)
                                set_links.add(link)

                            else:
                                list_ext[0].append(link)
                                set_links.add(link)

                list_int[0] : dict = sorter(list_int[0])
                list_ext[0] : dict = sorter(list_ext[0])
                time.sleep(0.5)
                flag  = 1
                list_int.append([])
                list_ext.append([])
        
        else:
		  # loop goes on till we run out of html pages
            
            while len(list_int[recur_level - 2]['html']) != 0:
                
                for link_int in list_int[recur_level - 2]['html']: 

                    with requests.get(link_int, stream=True) as html_req:

                        soup = BeautifulSoup(html_req.text, "lxml")


                        for line in soup.find_all('a'):
                            link = line.get("href")
                                
                            if link!= None and link != '' and link not in set_links and len(list_int[recur_level -1]) <max_no_of_links:
                                if url in link:
                                    list_int[recur_level -1].append(link)
                                    set_links.add(link)
                                else:
                                    list_ext[recur_level -1].append(link)
                                    set_links.add(link)

                        for line in soup.find_all(list_src_tags):
                            link = line.get("src")
                                
                            if link!= None and link != '' and link not in set_links and len(list_int[recur_level -1]) <40:
                                if url in link:
                                    list_int[recur_level -1].append(link)
                                    set_links.add(link)
                                else:
                                    list_ext[recur_level -1].append(link)
                                    set_links.add(link)

                list_int[recur_level - 1] : dict = sorter(list_int[recur_level - 1])
                list_ext[recur_level -1] : dict = sorter(list_ext[recur_level -1])
                time.sleep(0.5)
                recur_level +=1
                list_int.append([])
                list_ext.append([])
                if recur_level > max_recursion_level:
                     
                     # to break out of two loops we use flag variable
                     flag = 100
                     break
            else: 
                # exited out of the loop properly, so while-else statement gets executed.
                break
            if flag == 100:
                 # to break to limit the recursive limit to avoid server overload
                 break

    # returning a set which has all links
            

    return set_links, list_int, list_ext, recur_level

no_threshold = False
set_links = {url}
if args.thresh == None:
    print(f"Maximum recursive level when not prompted : {max_recursion_level}")
    print("Fetching all the links...")
    set_links, list_int_final, list_ext_final, main_recur_level = getlinks_no_thresh(url, list_int, list_ext, set_links)
    
    # subtracting 1 because at the end, an extra empty list is appended to both int and ext lists

    main_recur_level = main_recur_level - 1
    no_threshold = True
else:
    print("Fetching all the links...")
    set_links, list_int_final, list_ext_final, main_recur_level = getlinks_t(url, list_int, list_ext, thresh, set_links)


if args.output:
	with open('list_of_urls.csv', 'w', newline='') as file_obj:
		serial_no = 1
		writer_obj = csv.writer(file_obj)
		writer_obj.writerow(["Sno.", 'Link', 'Recursive_Level', 'Internal_Link', "Link_Type"])
		recur_level = 1
		for subdict_link in list_int_final:
            
			if recur_level <= main_recur_level:
				
				for link_type in subdict_link.keys():
					temp_list = list(subdict_link[link_type])
					for link in temp_list:
						writer_obj.writerow([serial_no, link, recur_level, "True", link_type])
						serial_no +=1
				recur_level += 1
                
		recur_level = 1  
		for subdict_link in list_ext_final:
			if list_ext_final.index(subdict_link) < main_recur_level:
				for link_type in subdict_link.keys():
					temp_list = list(subdict_link[link_type])
					for link in temp_list:
						writer_obj.writerow([serial_no, link, recur_level, "False", link_type])
						serial_no +=1
				recur_level += 1
            
else:
    if no_threshold:
        print(set_links)
    else:
        print("INTERNAL LINKS: ")
        list_print(list_int_final, main_recur_level)
        time.sleep(2)
        print("EXTERNAL LINKS: ")
        list_print(list_ext_final, main_recur_level) 

if args.output:
    f_text = open('urls_terminal.txt', 'w')
    f_text.write("\n\nINTERNAL LINKS: \n\n")
    list_write(list_int_final, main_recur_level, f_text)
    time.sleep(1)
    f_text.write("\n\nEXTERNAL LINKS: \n\n")
    list_write(list_ext_final, main_recur_level, f_text)    

end = time.time()

print()
print(f"Time taken for execution : {round((end - start), 2)} seconds")