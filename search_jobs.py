#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Master
#
# Created:     17/05/2015
# Copyright:   (c) Master 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from bs4 import BeautifulSoup
import urllib.request

class Search_Jobs:
    def __init__(self):
        self.urlList = list()
        self.init_results_file("results.txt")

    def prepare_headers(self):
        self.req = urllib.request.build_opener()
        self.req.addheaders= [('User-Agent', 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17')]

    def open_url(self, url):
        self.prepare_headers()
        self.soup = BeautifulSoup(self.req.open(url).read())
        #self.file_writer("rrr.txt", self.soup.prettify().encode('UTF-8'))

    def parse_gulftalent(self, url):
        f = open("results.txt","a")
        url_domain = url[:url.find(".com")+4]
        self.open_url(url)
        jobs = self.soup.find_all('a', {'class':['text-base','title']})[1:]
        print("Found " , len(jobs)," jobs on the page")
        for job in jobs:
            job_title = job.find('strong').get_text().strip()
            job_link = job.get('href')
            f.write(job_title + " "*(70-len(job_title)) + url_domain+job_link + '\n')
        f.write('\n\n')
        f.close()

    def add_urls(self, urlList):
        self.urlList += urlList

    def job_results(self):
        if len(self.urlList)>0:
            for url in self.urlList:
                print("opening url : " + url)
                if "gulftalent" in url:
                    self.parse_gulftalent(url)

    def init_results_file(self, file_name):
        f = open(file_name,"w")
        f.close

def main():
    search_jobs = Search_Jobs()
    search_jobs.add_urls(
        [
            'http://www.gulftalent.com/home/recruitment-and-jobs-in-uae-1.html',
            'http://www.gulftalent.com/home/recruitment-and-jobs-in-qatar-1.html'
        ])
    search_jobs.job_results()

if __name__ == '__main__':
    main()
