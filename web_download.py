# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 15:36:22 2017

@author: Xiaojun

Download and unzip files on NSF award download page.
url: https://www.nsf.gov/awardsearch/download.jsp

"""

import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import zipfile

def to_download_ls(url='https://www.nsf.gov/awardsearch/download.jsp'):
    # get file downloading urls from the download page
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    download_content = soup.find_all(class_='downloadcontent')
    links=[]
    fnames=[]
    for i in download_content:
        for ii in i.find_all('a',href=True):
            links.append(ii['href'])
            fnames.append(ii.string.split()[0])
    return links, fnames

def download_zip(links,fnames):
    # download files to the current directory
    for ind in range(len(links)):
        urlretrieve('https://www.nsf.gov/awardsearch/'+links[ind],fnames[ind]+'.zip')

def unzip(fnames):
    # unzip files to the folder of the same name
    for f in fnames:
        with zipfile.ZipFile(f+".zip","r") as zip_ref:
            zip_ref.extractall(f)
            
if __name__ == "__main__":
    links, fnames = to_download_ls()
    download_zip(links,fnames)
    unzip(fnames)
