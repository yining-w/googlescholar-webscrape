# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 16:27:44 2022

@author: Yi Ning Wong
"""
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
from datetime import date
import os

"""
Set Up
"""
# Get Relative Path
dirname = os.getcwd()
path = "\Github\googlescholar-webscrape"

# Get date of download
today = date.today() 
date_string = today.strftime("%m%d%Y")

"""
Run query
"""
def query():    
    # Get list of countries
    countries = ["Aruba", "Afghanistan", "Angola", "Albania", "Andorra", "United Arab Emirates", 
                 "Argentina", "Armenia", "American Samoa", "Antigua and Barbuda", "Australia", 
                 "Austria", "Azerbaijan", "Burundi", "Belgium", "Benin", "Burkina Faso", "Bangladesh",
                 "Bulgaria", "Bahrain", "Bahamas The", "Bosnia and Herzegovina", "Belarus", "Belize",
                 'Bermuda', "Bolivia","Brazil", "Barbados", "Brunei Darussalam", "Bhutan", "Botswana",
                 "Central African Republic", "Canada", "Switzerland", "Channel Islands", "Chile",
                 "China", "Cote d'Ivoire", "Cameroon", "Congo Dem Rep", "Congo Rep", 
                 "Colombia", "Comoros", "Cabo Verde", "Costa Rica", "Cuba", "Curacao", "Cayman Islands",
                 "Cyprus", "Czech Republic", "Germany", "Djibouti", "Dominica", "Denmark", "Dominican Republic",
                 "Algeria", "Ecuador", "Egypt, Arab Rep", "Eritrea", "Spain", "Estonia", "Ethiopia",
                 'Finland', "Fiji", "France", "Faroe Islands", "Micronesia Fed Sts", "Gabon", 
                 "United Kingdom", "Georgia", "Ghana", "Gibraltar", "Guinea", "Gambia, The", "Guinea-Bissau", 
                 "Equatorial Guinea", "Greece", "Grenada", "Greenland", "Guatemala",
                 "Guam", "Guyana", "Hong Kong SAR, China", "Honduras", "Croatia", "Haiti",
                 "Hungary", "Indonesia", "Isle of Man", "India", "Ireland", "Iran Islamic Rep",
                 "Iraq", "Iceland", "Israel", "Italy", "Jamaica", "Jordan", "Japan", 
                 "Kazakhstan", "Kenya", "Kyrgyz Republic", "Cambodia", "Kiribati",
                 "St Kitts and Nevis", "Korea Rep", "Kuwait", "Lao PDR", "Lebanon",
                 "Liberia", "Libya", "St Lucia", "Liechtenstein", "Sri Lanka",
                 "Lesotho", "Lithuania", "Luxembourg", "Latvia", "Macao SAR, China",
                 "St Martin French part", "Morocco", "Monaco", "Moldova", "Madagascar",
                 "Maldives", "Mexico", "Marshall Islands", "North Macedonia", "Mali",
                 "Malta", "Myanmar", "Montenegro", "Mongolia", "Northern Mariana Islands",
                 "Mozambique", "Mauritania", "Mauritius", "Malawi", "Malaysia", "Namibia",
                 "New Caledonia", "Niger", "Nigeria", "Nicaragua", "Netherlands",  "Norway",
                 "Nepal", "Nauru", "New Zealand", "Oman",  "Pakistan",  "Panama", "Peru", 
                 "Philippines", "Palau", "Papua New Guinea", "Poland", "Puerto Rico",
                 "Korea, Dem People's Rep", "Portugal", "Paraguay", "West Bank and Gaza",
                 "French Polynesia", "Qatar", "Romania",  "Russian Federation", "Rwanda",
                 "Saudi Arabia", "Sudan", "Senegal", "Singapore", "Solomon Islands", 
                 "Sierra Leone", "El Salvador", "San Marino","Somalia", "Serbia",
                 "South Sudan", "Sao Tome and Principe", "Suriname", "Slovak Republic",
                 "Slovenia", "Sweden", "Eswatini", "Sint Maarten Dutch part", "Seychelles",
                 "Syrian Arab Republic", "Turks and Caicos Islands", "Chad", "Togo",
                 "Thailand", "Tajikistan", "Turkmenistan", "Timor-Leste", "Tonga",
                 "Trinidad and Tobago", "Tunisia", "Turkey", "Tuvalu", "Tanzania",
                 "Uganda", "Ukraine", "Uruguay", "United States", "Uzbekistan", 
                 "St Vincent and the Grenadines","Venezuela RB", "British Virgin Islands",
                 "Virgin Islands US", "Vietnam", "Vanuatu", "Samoa", "Kosovo", "Yemen Rep",
                 "South Africa","Zambia","Zimbabwe"]
    
    # Assessment Search (To be applied to all countries)
    assessments = "+%28PIRLS+OR+TIMSS+OR+PISA+OR+PASEC+OR+AMPLB+OR+'national+learning+assessment'%29&btnG="
    url = ('https://scholar.google.com/scholar?hl=en&as_sdt=0%2C9&q=')
    
    # Use for BeautifulSoup
    headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Mobile Safari/537.36'}
    
    # Small cleaning, replace space bars to + signs
    countries_search = [s.replace(' ', '+') for s in countries] 
    
    # Loop concatenate url to countries and assessments
    search_list = []
    query_numbers=[]
    
    for country in countries_search:
        search_list.append(url+ country + assessments) 
    
    # Scrape and append results for each country
    for search in search_list:
        response = requests.get(search, headers=headers)
        soup = bs(response.text, 'lxml')
        results = soup.find_all('div', class_="gs_ab_st")
        query_numbers.append([val.text for val in results])
        
    # Turn results to a dataframe
    df_queries = pd.DataFrame(query_numbers)
    df_queries = df_queries.rename(columns={df_queries.columns[0]: 'results'})
    countrynames = pd.DataFrame(countries)
    countrynames = countrynames.rename(columns={countrynames.columns[0]: 'countryname'})
    final = pd.concat([countrynames, df_queries], axis=1)
    
    # Get date of scraping 
    final['date_scraped'] = today
    
    final_clean = final
    
    # Clean the results column (get rid of extra characters)
    final_clean['results'] = final_clean['results'].str[21:]
    final_clean['results'] = final_clean['results'].str[:-156]

    return final_clean

# Run function
final_clean = query()
# Save file
final_clean.to_csv(dirname + path+ '/googlescholar_results_' + date_string + ".csv", index=False)

