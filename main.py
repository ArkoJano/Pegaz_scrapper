from passy import USERNAME,PASSWORD
import requests
from bs4 import BeautifulSoup
from pprint import pprint
import re

# USERNAME = ""
# PASSWORD = ""

payload = {"username":USERNAME, 
            "password":PASSWORD,
            "submit":"zaloguj"
            }

base_url = "https://login.uj.edu.pl/login"


class WebsiteConnector:

    def __init__(self, payload, base_url):
        self.payload = payload
        self.base_url = base_url
        self.session = requests.Session()

    def send_get_request(self):
          self.page = self.session.get(self.base_url)
          

    def set_headers(self):
        soup = BeautifulSoup(self.page.content, "html.parser")
        # Pobranie wartosci "hidden"
        input_tags = soup.findAll('input')
        inputs = list()

        for tag in input_tags:
            input_type = tag.attrs.get("type")
            input_value = tag.attrs.get("value")
            input_name = tag.attrs.get("name")
            if input_type == "hidden":
                payload[input_name] = input_value

        # pobranie headerow
        self.headers = self.page.request.headers
        
        self.headers["user-agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
    
    def get_urls(self):

        status = self.session.post(self.base_url, data=self.payload, headers=self.headers)
        soup = BeautifulSoup(status.content, "html.parser")

        a_tags = soup.findAll('a')
        for tag in a_tags:
            a_href = tag.attrs.get("href")
            if "pegaz" in str(a_href):
                pegaz_url = a_href
        
        

        pegaz_data = self.session.get(pegaz_url)
        soup = BeautifulSoup(pegaz_data.content, "html.parser")

        self.urls = dict()

        a_tags = soup.findAll('a')
        for tag in a_tags:
            a_href = tag.attrs.get("href")
            if "https://pegaz.uj.edu.pl/" in str(a_href):
                self.urls['pegaz'] = a_href

            if "https://egzaminy.uj.edu.pl/" in str(a_href):
                self.urls['egzaminy'] = a_href

            
        

    def get_pegaz_soup(self):
        pegaz_data = self.session.get(self.urls['pegaz'])
        self.pegaz_soup = BeautifulSoup(pegaz_data.content, "html.parser")

    def get_egzaminy_soup(self):
        egzaminy_data = self.session.get(self.urls['egzaminy'])
        self.egzaminy_soup = BeautifulSoup(egzaminy_data.content, "html.parser")


    
    # def print_raw_data_to_file(self, platform):
    #     with open('result.html', "w", encoding='utf-8') as p:
    #         if platform == 'pegaz':
    #             p.write(str(self.pegaz_soup))
    #         if platform == 'egzaminy':    
    #             p.write(str(self.egzaminy_soup))

    def get_all_courses(self):
       
        courses_list = ["Filozofia","Prawo internetu", "Algebra z geometrią MS", "Analiza matematyczna II",
                        "Język C++", "Matematyka dyskretna", "Systemy operacyjne"]
        courses_links = dict()
       
        courses = self.pegaz_soup.findAll("a", class_="list-group-item list-group-item-action")
        
        for course in courses:
            course_name = course.findAll("span", class_="media-body")[0]
            course_name = course_name.string.split(".")[0]
            if course_name in courses_list:
                course_link = course.attrs.get("href")
                courses_links[course_name] = course_link
 
        pprint(courses_links)
                    
        ##pprint(courses)

    def zdaned_czy_nie_zdaned(self):
        
        courses_links = dict()
       
        courses = self.egzaminy_soup.findAll("a", class_="list-group-item list-group-item-action")
        
        for course in courses:
            course_link = course.attrs.get("href")
            if "course" in course_link:
                course_name = course.findAll("span", class_="media-body")[0]
                course_name = course_name.string.split(",")[0]
                if "Wykład" in course_name:
                    courses_links[course_name] = course_link
        # pprint(courses_links)

        zdaned_list = list()

        for course_obj in courses_links.items():
            course_data = self.session.get(course_obj[1])
            course_soup = BeautifulSoup(course_data.content, "html.parser")
            link = course_soup.findAll("a", class_="aalink")
            assigns_list = list()
            for data in link:
                href_from_link = data.attrs.get("href")
                if "assign" in href_from_link:
                    one_part_data = self.session.get(href_from_link)
                    one_part_soup = BeautifulSoup(one_part_data.content, "html.parser")
                    
                    title = one_part_soup.find("h2").string
                    
                    zdaned = one_part_soup.find("td", class_="submissionnotgraded cell c1 lastcol")
                    
                    if zdaned == None:

                        print(f"Ocenione zadanie: {title}: {href_from_link}")
                        



pegaz = WebsiteConnector(payload, base_url)
pegaz.send_get_request()
pegaz.set_headers()
pegaz.get_urls()
# pegaz.print_raw_data()
# pegaz.get_all_courses()
# pegaz.get_pegaz_soup()
pegaz.get_egzaminy_soup()
pegaz.zdaned_czy_nie_zdaned()

  

    
    
    



    


    

# status = requests.post(base_url, data=payload)
# pprint(status.content)

# soup = BeautifulSoup(page.content, "html.parser")

# pprint(soup)