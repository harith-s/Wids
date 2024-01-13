from bs4 import BeautifulSoup
import requests as req
import time
print("Put the skills you are familiar with")
familiar_skills = input(">")


def find_jobs(familiar_skills):
    print(f"filering out {familiar_skills}")
    html_req = req.get("https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=&searchTextText=&txtKeywords=python&txtLocation=").text
    soup = BeautifulSoup(html_req, "lxml")
    list_jobs = soup.find_all("li", class_="clearfix job-bx wht-shd-bx")

    for job in list_jobs:
        span = job.find("span", class_ = "sim-posted").span.text
        if span == "Posted few days ago":
            comp_name = job.find("h3", class_ = "joblist-comp-name").text.replace(" ", '')
            skills = job.find("span", class_ = 'srp-skills').text.replace(" ", '')
            list_skills = skills.split(",")
            list_skills[-1] = list_skills[-1].replace('\r\n', '')
            list_skills[0] = list_skills[0].replace('\n', '')
            list_skills[0] = list_skills[0].replace('\r', '')
            for skill in list_skills:
                if skill not in familiar_skills:
                    break
            else:

                more_info = job.header.h2.a['href'].replace(" ", '')
                
                print(f'''
Company name  : {comp_name.strip()} 
Skills        : {skills.strip()}
More info     : {more_info.strip()}
''')
                


if __name__ == "__main__":
    while True:
        find_jobs(familiar_skills)
        wait_min = 10
        print(f"Waiting for {wait_min} seconds...")
        time.sleep(wait_min)