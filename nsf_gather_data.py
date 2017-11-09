# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 20:28:12 2017

@author: Xiaojun

This script parse data from xml files and put them into csv files by year
"""

from os import listdir
from bs4 import BeautifulSoup
import pandas as pd


tag_list=['AwardTitle','AwardEffectiveDate','AwardExpirationDate','AwardAmount',
          'AwardInstrument','Directorate','Division','ProgramOfficer','AbstractNarration',
          'MinAmdLetterDate','MaxAmdLetterDate','ARRAAmount','AwardID','CityName',
          'ZipCode','PhoneNumber','StreetAddress','CountryName','StateName','StateCode']
unbounded_list=['Investigator','FoaInformation','ProgramElement','ProgramReference']

def add_to_dict(record,tag,key=None):
    if key is None:
        key = tag.name
    val = tag.text.strip()
    record[key]=val
    return record

def add_to_dict_unbounded(record,unbounded):
    tags = soup.find_all(unbounded)
    val=[]
    if tags:
        for tag in tags:
            val.append(tag.text.strip())
    record[unbounded]=val
    return record

def from_xml(xml_dir):
    with open(xml_dir) as fp:
        soup = BeautifulSoup(fp,'xml')
    record = {}   
    for tag_name in tag_list:
        tag = soup.find(tag_name)
        record = add_to_dict(record,tag)
    record = add_to_dict(record,soup.Code,key='OrganizationCode')
    record = add_to_dict(record,soup.Name,key='Institution')
    for unbounded in unbounded_list:
        record = add_to_dict_unbounded(record,unbounded)   
    return record
        
def from_folder(folder):
    all_records = []
    for xml_dir in listdir(folder):
        try:
            record = from_xml(folder+xml_dir)
        except: 
            print(folder+xml_dir)
        all_records.append(record)
    df = pd.DataFrame(all_records)
    df.to_csv(folder[:-1]+'.csv',index=False)

for yr in range(1977,2018):
    folder = 'C:\\Users\\Xiaojun\\Documents\\PYTHON\\NSF\\'+str(yr)+'\\'
    print('Getting '+str(yr)+'...')
    from_folder(folder)
    print(str(yr)+' done.')
