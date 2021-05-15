from passy import USERNAME,PASSWORD
import requests
from bs4 import BeautifulSoup
from pprint import pprint

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
    
    def get_into_pegaz_main(self):

        status = self.session.post(self.base_url, data=self.payload, headers=self.headers)
        soup = BeautifulSoup(status.content, "html.parser")

        a_tags = soup.findAll('a')
        for tag in a_tags:
            a_href = tag.attrs.get("href")
            if "pegaz" in str(a_href):
                pegaz_url = a_href


        self.pegaz_data = self.session.get(pegaz_url)
        soup = BeautifulSoup(self.pegaz_data.content, "html.parser")

        a_tags = soup.findAll('a')
        for tag in a_tags:
            a_href = tag.attrs.get("href")
            if "pegaz" in str(a_href):
                pegaz_url = a_href

        self.pegaz_data = self.session.get(pegaz_url)
        self.pegaz_soup = BeautifulSoup(self.pegaz_data.content, "html.parser")

        

    def print_raw_data(self):
        pprint(self.pegaz_soup)

    def print_raw_data_to_file(self):
        with open('pegaz.html', "w", encoding='utf-8') as p:
            p.write(str(self.pegaz_soup))

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



pegaz = WebsiteConnector(payload, base_url)
pegaz.send_get_request()
pegaz.set_headers()
pegaz.get_into_pegaz_main()
# pegaz.print_raw_data()
# pegaz.print_raw_data_to_file()
pegaz.get_all_courses()
  

    
    
    



    


    

# status = requests.post(base_url, data=payload)
# pprint(status.content)

# soup = BeautifulSoup(page.content, "html.parser")

# pprint(soup)