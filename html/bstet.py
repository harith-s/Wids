from bs4 import BeautifulSoup

with open('hi.html', 'r') as html_file:
    content = html_file.read()
    
    soup = BeautifulSoup(content, 'lxml')
    tags = soup.find_all('')
    for i in content:
        print(i.h2)