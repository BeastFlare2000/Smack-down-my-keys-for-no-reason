from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
start_url='https://exoplanets.nasa.gov/discovery/exoplanet-catalog/'
browser = webdriver.chrome("C:/Users/pl787/OneDrive/Desktop/folder of most cool (Python)/C128/chromedriver copy.exe")
browser.get(start_url)
time.sleep(10)
headers = ["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date", "hyperlink", "planet_type", "planet_radius", "orbital_radius", "orbital_period", "eccentricity"]
planet_data = []
new_planet_data = []
def scrap():
    for i in range(1,430):
        while True:
            time.sleep(2)
            soup = BeautifulSoup(browser.page_source, "html.parser")
            current_page_num = int(soup.find_all('input',ATTRS={'class','page_num'})[0].get('value'))
            if current_page_num<i:
                browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
            elif current_page_num>i:
                browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[1]/a').click()
            else:
                break
        for ul_tag in soup.find_all("ul", attrs={"class", "exoplanet"}):
            li_tags = ul_tag.find_all("li")
            temp_list = []
            for index, li_tag in enumerate(li_tags):
                if index == 0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")
            planet_data.append(temp_list)
        browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
    def scrap_2(hyperlink):
        try:
            page = requests.get(hyperlink)
            soup = BeautifulSoup(page.page_source, "html.parser")
            temp_list = []
            for tr_tag in soup.find_all("tr", attrs={"class": "fact_row"}): 
                td_tags = tr_tag.find_all("td") 
                for td_tag in td_tags: 
                    try: 
                        temp_list.append(td_tag.find_all("div", attrs={"class": "value"})[0].contents[0]) 
                    except: 
                        temp_list.append("") 
                        new_planet_data.append(temp_list) 
        except: 
            time.sleep(1) 
            scrap_2(hyperlink)
scrap()
for index, data in enumerate(planet_data): 
    scrap_2(data[5]) 
    print(f"{index+1} page done 2") 
    final_planet_data = [] 
for index, data in enumerate(planet_data):
     new_planet_data_element = new_planet_data[index] 
     new_planet_data_element = [elem.replace("\n", "") for elem in new_planet_data_element] 
new_planet_data_element = new_planet_data_element[:7] 
final_planet_data.append(data + new_planet_data_element) 
with open("final.csv", "w") as f: 
    csvwriter = csv.writer(f) 
    csvwriter.writerow(headers) 
    csvwriter.writerows(final_planet_data)
