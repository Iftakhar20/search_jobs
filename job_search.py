#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Master
#
# Created:     12/05/2015
# Copyright:   (c) Master 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from bs4 import BeautifulSoup
from urllib.request import urlopen
import time

def add_headers(request):
    request.add_header('Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11')
    return request

def main():
    """Main function starts webscrapping.
       Uses a dict describing functions for each website
    """
    links = {
                "http://www.inspireselection.com/candidate/vacList.asp?search=-1": get_inspire_selection_jobs,
                "http://www.gulftalent.com/home/recruitment-and-jobs-in-uae-1.html": get_gulftalent_jobs ,
                "http://www.gulftalent.com/home/recruitment-and-jobs-in-qatar-1.html": get_gulftalent_jobs,
    }
    #call functions with urls as arguments
    for l in links:
        print("Calling " + l  + "...")
        links[l](l)
    print("Finished creating result file")

def get_gulftalent_jobs(base_url):
    """Accessess gulftalent.com jobs portal and scraps jobs title & links.
       Writes all scrapped info to result.txt in the same folder
    """
    host_url = "http://www.gulftalent.com"
    soup = BeautifulSoup(urlopen(base_url).read())

    #open result.txt & write header
    written_file = open("result.txt", "a")
    written_file.write(soup.title.string.strip() + " (Updated : " + time.strftime("%d-%b-%Y %H:%M:%S")+ ")\n")
    written_file.write("Searched at : " + base_url)
    written_file.write(")\n"+ "-"*100 + "\n")

    #finds all links to jobs
    jobs =soup.find_all('a',{"class":"job-results-item"})
    for j in jobs:
        #job title is found in a child div having class 'title'
        job_title = j.find_all('div',{"class":"title"})[0].encode_contents(formatter="html").strip().decode("utf-8")
        #job location is found in a child div having class 'location'
        job_location = j.find_all('div',{"class":"location"})[0].encode_contents(formatter="html").strip().decode("utf-8")

        written_file.write(job_title + ", " + job_location + " "*(70-len(job_title)-len(job_location)) + host_url+j.get('href') + "\n")

    #close result.txt
    written_file.write("\n\n")
    written_file.close

def get_inspire_selection_jobs(base_url):
    """Accessess inspireselection.com jobs portal and scraps jobs title & links.
       Writes all scrapped info to result.txt in the same folder
    """
    soup = BeautifulSoup(urlopen(base_url).read())
    jobs = soup.find_all('div', {"class":"vacList"})

    #open result.txt & write header
    written_file = open("result.txt", "w")
    written_file.write(soup.title.string.strip() + " (Updated : " + time.strftime("%d-%b-%Y %H:%M:%S")+ ")\n")
    written_file.write("Searched at : " + base_url)
    written_file.write(")\n"+ "-"*100 + "\n")

    #finds all links to jobs
    for job in jobs:
        #job title is found in a child 'a' tag
        job_title = job.find_all("a", {"class":"fltL"})
        for j in job_title:
            job_link = j.get("href")
            j =j.encode_contents(formatter="html").strip().decode("utf-8").split(",")[0]
            written_file.write(j + " "*(70-len(j)) + job_link + "\n")

    #close result.txt
    written_file.write("\n\n")
    written_file.close

if __name__ == '__main__':
    main()