import requests
from bs4 import BeautifulSoup
from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys
import time
from time import sleep 
import datetime
import unicodedata
import urllib3
import urllib
from urllib.parse import urlencode, urlparse, parse_qs
import html
from lxml.html import fromstring
import json 
import http


url = "https://www.workana.com/login" 
username = "YOUR EMAIL"
password = "YOUR PASSWORD"
page_limit = 3

driver = webdriver.Firefox(r'C:\Users\Gabriel\anaconda3\Lib\site-packages\seleniumwire\webdriver')  ##change to your path
sleep(2)

driver.header_overrides = {
    'Referer': 'referer_string',
}

driver.get(url)
sleep(3)

fp = webdriver.FirefoxProfile()
path_modify_header = r'C:\Users\Gabriel\Desktop\helloWorld\modify_headers-0.7.1.1-fx.xpi'  ##change to your path
fp.add_extension(path_modify_header)
fp.set_preference("modifyheaders.headers.count", 1)
fp.set_preference("modifyheaders.headers.action0", "Will")
fp.set_preference("modifyheaders.headers.name0", "FFOX") 
fp.set_preference("modifyheaders.headers.value0", "20.2") 
fp.set_preference("modifyheaders.headers.enabled0", True)
fp.set_preference("modifyheaders.config.active", True)
fp.set_preference("modifyheaders.config.alwaysOn", True)


driver.find_element_by_name("email").send_keys(username)
sleep(0.5)
driver.find_element_by_name("password").send_keys(password)
sleep(0.5)
driver.find_element_by_css_selector("button.btn").click()
sleep(5)

driver.header_overrides = {
    'Referer': 'referer_string',
}

fp = webdriver.FirefoxProfile()
fp.add_extension(path_modify_header)
fp.set_preference("modifyheaders.headers.count", 1)
fp.set_preference("modifyheaders.headers.action0", "Will")
fp.set_preference("modifyheaders.headers.name0", "FFOX") 
fp.set_preference("modifyheaders.headers.value0", "20.2") 
fp.set_preference("modifyheaders.headers.enabled0", True)
fp.set_preference("modifyheaders.config.active", True)
fp.set_preference("modifyheaders.config.alwaysOn", True)

def invalid_val(): return 'N/A'

def clear_str( text ):
    text = str(text).replace( '\n', '' ).replace( '\r', '' ).replace( '\t', '' )
    return text

def clear_comma(text):
    return str(text).replace(',', '-')

def numeric( val, type='float' ):
    val = str(val) 
    try:
        if( type == 'int' ): val = int(val)
        else: val = float(val)
        return str(val)
    except: return invalid_val()


page = 1
pageline = []

while (page <= page_limit):
    new_url = "https://www.workana.com/freelancers/brazil_united-states/programacion-web?category=it-programming&"+"page="+str(page)
    driver.get(new_url)
    time.sleep(5)

    
    html = driver.execute_script("return document.documentElement.outerHTML")
    workana_soup = BeautifulSoup(html, 'html.parser')
    website = workana_soup.find_all('div', ['js-worker listing worker-item', 'js-worker listing worker-item hero']) 

                   
    for data in website:    
        
        soup = BeautifulSoup( str(data), 'html.parser' )

        name = ''
        for e in soup.find_all( 'span' ):
            if( e.parent.name == 'a' and e.parent.parent.name == 'h3' ):
                name = clear_str(e.text)
                print(name)
                continue    
        

        e = soup.find('span', class_='stars-bg')
        res =  str(e[ 'title' ]).replace( ' de 5.00', '' )
        res = clear_str( res )  
        res = float(res)
        rating = clear_str( res )
        print(rating)

        e = soup.find('span', class_='js-monetary-amount monetary-amount')
        hourly_rate = invalid_val()
        if( e != None ): hourly_rate = numeric(e[ 'data-amount' ], type='float')       
        print(hourly_rate)     

        e = soup.find('p', class_= 'hidden-xs')
        t_soup = BeautifulSoup( str(e), 'html.parser' )
        projects = hours = invalid_val()
        for e in t_soup.find_all( 'span' ):
            res = ''
            try:
                if( 'Projetos completados' in e.text ): projects = str(e.text).replace('Projetos completados: ', '')
                else: hours = str(e.text).replace('Horas trabalhadas em projetos por hora: ', '')
            except: pass

        e = soup.find( 'span', class_='hero-label' )
        is_pro = 0
        if( e != None ): is_pro = 1
                            
        def getByCss(selector):
            text = driver.find_element_by_css_selector(selector).text
            print(text)
            return text

                       
        link = soup.find('a')
       
        if link.has_attr('href'):
            half_link = link['href']
            user_page_link = "https://workana.com" + half_link
            print(user_page_link)
            driver.get(user_page_link)
            time.sleep(3)
                    
                    
            html = driver.execute_script("return document.documentElement.outerHTML")
            user_page_soup = BeautifulSoup(html, 'html.parser')
            
            skills = []
            e = driver.find_elements_by_css_selector(' .table-striped > tbody > tr > td:nth-child(1) > a')   
            for s in e:
                res = str(s.text)
                skills.append(res)     
            print(*skills)  


            recomendation = []
            e = user_page_soup.find_all('cite')
            for s in e:
                res = str(s.text)
                recomendation.append(res.replace('\"', ''))
            print(*recomendation)
            

        page_line = {
            "Name": name,
            "Rating": rating,
            "Salary": hourly_rate,
            "Hero": is_pro,
            "Projects": projects,
            "Hours": hours,
            "Skills": skills,
            "Recommendation": recomendation,
            "Job Page Link": user_page_link,            
        }

        pageline.append(page_line)
            
    page += 1

with open('workana_data.json', 'w') as outfile:  
    json.dump(pageline, outfile, indent=4, ensure_ascii=False)