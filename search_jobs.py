from bs4 import BeautifulSoup
import urllib.request
import time

class Search_Jobs:
    """
    Searches Job listing at varios websites.
    Currently supports gulftalent.com & inspireselection.com

    Usage:
        search_jobs = Search_Jobs()
        search_jobs.add_urls([list of supported website urls])
        search_jobs.job_results()

    Returns: Creates Resulsts.txt in the same folder.
    """
    def __init__(self):
        self.urlList = list()
        self.results_file = "results.txt"
        #ensure results.txt is empty
        f=open(self.results_file,"w")
        f.close

    def prepare_headers(self):
        """
        Spoofs program as a normal browser.
        Some sites return different page when used
        with default value (considered a mobile device)
        """
        self.req = urllib.request.build_opener()
        self.req.addheaders= [('User-Agent', 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17')]

    def open_url(self, url):
        """
        Opens a given url & creates a Beautiful Soup object.
        """
        self.prepare_headers()
        self.soup = BeautifulSoup(self.req.open(url).read())

    def write_file_header(self, url):
        """
        Writes job url & search date in given text file.
        """
        f = open(self.results_file, "a+")
        f.write ("Searching Job at : " + url + "\n")
        f.write("Updated : " + time.strftime("%A, %d %B, %Y %H:%M") + "\n")
        f.write("-"*100 + "\n")
        return f

    def parse_gulftalent(self, url):
        """
        Parses gulftalent links.
        Jobs are found in 'a' link with class 'text-base' & 'title'.
        First link points to 'Clear All' hence not considered.
        """
        self.open_url(url)

        #find all jobs. Ignore first 'a' as it is not a job.
        jobs = self.soup.find_all('a', {'class':['text-base','title']})[1:]

        f = self.write_file_header(url)

        #iterate thru all jobs found in 'a' tag.
        #Job title is found in <strong> tag.
        for job in jobs:
            job_title = job.find('strong').get_text().strip()
            job_link = job.get('href')
            f.write(job_title + " "*(70-len(job_title)) +job_link + '\n')

        f.write('\n\n')
        f.close()

    def parse_inspireselection(self, url):
        """
        Parses inspireselection links.
        Jobs are found in 'a' link with class 'fltL'.
        """
        self.open_url(url)

        #find all jobs
        jobs = self.soup.find_all('a', {'class':['fltL']})

        f = self.write_file_header(url)

        #iterate thru all jobs found in 'a' tag
        for job in jobs:
            job_title = job.get_text().strip()
            job_link = job.get('href')
            f.write(job_title + " "*(70-len(job_title)) +job_link + '\n')

        f.write('\n\n')
        f.close()

    def add_urls(self, urlList):
        """
        Facilitates adding urls during program
        """
        self.urlList += urlList

    def job_results(self):
        """
        Main function that runs the program.
        """
        if len(self.urlList)>0:
            #if atleast one url was given
            for url in self.urlList:
                print(url)
                #iterate thru all given urls
                if "gulftalent" in url:
                    self.parse_gulftalent(url)
                if "inspireselection" in url:
                    self.parse_inspireselection(url)
        print("done..")

def main():
    search_jobs = Search_Jobs()
    search_jobs.add_urls(
        [
        'http://www.gulftalent.com/home/recruitment-and-jobs-in-uae-1.html',
        'http://www.gulftalent.com/home/recruitment-and-jobs-in-uae-2.html',
        'http://www.gulftalent.com/home/recruitment-and-jobs-in-uae-3.html',
        'http://www.gulftalent.com/home/recruitment-and-jobs-in-qatar-1.html',
        'http://www.gulftalent.com/home/recruitment-and-jobs-in-qatar-2.html',
        'http://www.gulftalent.com/home/recruitment-and-jobs-in-qatar-3.html',
        'http://www.inspireselection.com/candidate/vaclist.asp?search=-1'
        ])

    search_jobs.job_results()
    time.sleep(60)

if __name__ == '__main__':
    main()
