# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 20:28:12 2017

@author: Xiaojun

This script parse data from xml files and put them into csv files by year
"""

from os import listdir
import xml.etree.ElementTree as ET
import pandas as pd

def add_to_dict(record,key,val):
    if key in record:
        try:
            record[key].append(val)
        except AttributeError:
            record[key]=[record[key],val]
    else:
        record[key]=val
    return record

def from_xml(xml_dir):
    tree = ET.parse(xml_dir)
    root = tree.getroot()
    record = {}
    for child in root[0]:
        if child.text == '\n':
            for subchild in child.iter():
                if subchild.text == '\n':
                    prefix = subchild.tag+'_'
                else:
                    key = prefix+subchild.tag
                    val = subchild.text
                    record = add_to_dict(record,key,val)
        else:
            key = child.tag
            val = child.text
            record = add_to_dict(record,key,val)
    return record
        
def from_folder(folder):
    all_records = []
    for xml_dir in listdir(folder):
        try:
            record = from_xml(folder+xml_dir)
        except: 
            print(folder+xml_dir)
            continue
        all_records.append(record)
    df = pd.DataFrame(all_records)
    '''
    all columns:
    ['ARRAAmount', 'AbstractNarration', 'AwardAmount', 'AwardEffectiveDate',
   'AwardExpirationDate', 'AwardID', 'AwardInstrument_Value', 'AwardTitle',
   'Directorate_LongName', 'Division_LongName', 'Institution_CityName',
   'Institution_CountryName', 'Institution_Name',
   'Institution_PhoneNumber', 'Institution_StateCode',
   'Institution_StateName', 'Institution_StreetAddress',
   'Institution_ZipCode', 'Investigator_EmailAddress',
   'Investigator_EndDate', 'Investigator_FirstName',
   'Investigator_LastName', 'Investigator_RoleCode',
   'Investigator_StartDate', 'MaxAmdLetterDate', 'MinAmdLetterDate',
   'Organization_Code', 'ProgramElement_Code', 'ProgramElement_Text',
   'ProgramOfficer_SignBlockName', 'ProgramReference_Code',
   'ProgramReference_Text']
    '''
    select_columns = ['ARRAAmount', 'AbstractNarration', 'AwardAmount', 'AwardEffectiveDate',
   'AwardExpirationDate', 'AwardID', 'AwardInstrument_Value', 'AwardTitle',
   'Directorate_LongName', 'Division_LongName', 'Institution_CityName',
   'Institution_CountryName', 'Institution_Name', 'Institution_StateCode', 
   'Institution_StateName', 'Institution_ZipCode', 'Investigator_EndDate', 
   'Investigator_FirstName', 'Investigator_LastName', 'Investigator_RoleCode',
   'Investigator_StartDate', 'Organization_Code', 'ProgramElement_Code', 
   'ProgramElement_Text', 'ProgramReference_Code', 'ProgramReference_Text']
    selected = [i for i in df.columns if i in select_columns]
    df[selected].to_csv(folder[:-1]+'.csv',index=False)

for yr in range(1979,2018):
    folder = 'C:\\Users\\Xiaojun\\Documents\\PYTHON\\NSF\\'+str(yr)+'\\'
    print('Getting '+str(yr)+'...')
    from_folder(folder)
    print(str(yr)+' done.')
