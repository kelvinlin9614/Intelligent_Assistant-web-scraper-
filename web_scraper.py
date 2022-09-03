# Zewen Lin
import requests
import re
from bs4 import BeautifulSoup


class WebScraper:
    def __init__(self, url, category, location):
        self.url = url
        self.category = category
        self.location = location

    def url_add_category(self):
        if self.url == "https://www.timesjobs.com/":
            return self.url + "candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=" \
                   + self.category + "&txtLocation=" + self.location

    def run(self):
        company_name = []
        skills = []
        job_link = []
        years = []
        location = []
        new_url = self.url_add_category()
        html_text = requests.get(new_url).text
        soup = BeautifulSoup(html_text, 'lxml')
        jobs = soup.find_all("li", class_="clearfix job-bx wht-shd-bx")

        for job in jobs:
            published_date = job.find('span', class_='sim-posted').span.text
            if 'few' in published_date:
                company_name.append(job.find('h3', class_='joblist-comp-name').text.replace('  ', '').strip())
                skills.append(job.find('span', class_='srp-skills').text.replace('  ', '').strip())
                job_link.append(job.find('a').get('href'))
                # regex (find all the range of year)
                years.append(re.findall('\d{1,2} - \d{1,2} yrs', job.find(class_='top-jd-dtl clearfix').text))
                location.append(job.find(class_='top-jd-dtl clearfix').find('span', title_="").text)
        return company_name, skills, job_link, years, location


# ws = WebScraper("https://www.timesjobs.com/", "java", "")
# company, skill, link, year, location = ws.run()
# print(year)
# print(location)
