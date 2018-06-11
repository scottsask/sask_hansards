"""

This script requests and parses a web page containing links to all Hansard debate transcripts of the Saskatchewan Legislature.
The PDF files for each debate are then downloaded and (re)named consistently.

"""

import requests
from bs4 import BeautifulSoup
from urlparse import urlparse
from datetime import datetime
import wget
import time
import os

#There's an old ASP.net form sitting at this endpoint
#We can fill it out, submit it, and get a listing of every Saskatchewan Legislature debate on record
meetings_endpoint = 'http://www.legassembly.sk.ca/legislative-business/meetings/'

#Start a session
session = requests.Session()

#Request the page and parse its markup with BeautifulSoup
meeting_selection_page = session.get(meetings_endpoint)
soup = BeautifulSoup(meeting_selection_page.content, 'html.parser')


#Find magic values we need in the soup to make a valid form submission
#These are hidden inputs the ASP.net form requires to submit
viewstate = soup.find('input', {'name': "__VIEWSTATE"})['value']
viewstategenerator = soup.find('input', {'name': "__VIEWSTATEGENERATOR"})['value']

#Fill out the form data, setting the other form fields including...
#Start Date: Jan 1, 1947
#End date: Dec 31, 2016 
#Location: Legislative Assembly
#Type: Debate
form_body = {
    '__EVENTTARGET': '',
    '__EVENTARGUMENT': '',
    'VIEWSTATE': viewstate,
    'VIEWSTATEGENERATOR': viewstategenerator,
    '__VIEWSTATEENCRYPTED': '',
    'ctl00$ctl00$ContentContainer$MainContent$ContentBottom$ContextDropDownList': 0,
    'ctl00$ctl00$ContentContainer$MainContent$ContentBottom$CategoryDropDownList': 280140005,
    'ctl00$ctl00$ContentContainer$MainContent$ContentBottom$ddlStartMonth': 1,
    'ctl00$ctl00$ContentContainer$MainContent$ContentBottom$ddlStartDay': 1,
    'ctl00$ctl00$ContentContainer$MainContent$ContentBottom$ddlStartYear': 1947,
    'ctl00$ctl00$ContentContainer$MainContent$ContentBottom$ddlEndMonth': 12,
    'ctl00$ctl00$ContentContainer$MainContent$ContentBottom$ddlEndDay': 31,
    'ctl00$ctl00$ContentContainer$MainContent$ContentBottom$ddlEndYear': 2018,
    'ctl00$ctl00$ContentContainer$MainContent$ContentBottom$ApplyFilterButton': 'Go',
    'ctl00$ctl00$ContentContainer$MainContent$ContentBottom$txtStartYear': 1947,
    'ctl00$ctl00$ContentContainer$MainContent$ContentBottom$txtStartMonth': 1,
    'ctl00$ctl00$ContentContainer$MainContent$ContentBottom$txtStartDay': 1,
    'ctl00$ctl00$ContentContainer$MainContent$ContentBottom$txtEndYear': 2018,
    'ctl00$ctl00$ContentContainer$MainContent$ContentBottom$txtEndMonth': 12,
    'ctl00$ctl00$ContentContainer$MainContent$ContentBottom$txtEndDay': 31 
}

#TODO:  The 'type' and location' selections posted here don't appear to work -- every type of content is returned in the date range regardless of 'type' and 'location' settings.
#So for now we will just look at the path to download and rename all of the debate PDFs we need.
#TODO:  Add a way to re-run this to grab new hansards

#Post the form
response_post = session.post(url=meetings_endpoint,data=form_body)
#The response we get should be a soupy DOM with a bunch of links to the hansards we want to download 
hansard_debates_listing_soup = response_post.content
print(hansard_debates_listing_soup)
#Make that soup beautiful!
soup = BeautifulSoup(hansard_debates_listing_soup, 'html.parser')

#The debate PDFs are all links on the page, so pull them out of the beautiful soup
links = soup.find_all('a')

#The files we need look like '/legdocs/Legislative%20Assembly/Hansard/<# legislature>L<# session>S/<date>filename.pdf'
#We'll extract the legislature number and session number from the path.
#We'll also extract and fix the inconsistent date formats found in the filenames.

def parse_filename(filename):
    #Most files begin with a date like YYMMDD (e.g., 760115).
    #Some files use a different format, YY-MM-DD 
    if (filename[2] == "-"): #If it's the second case...
        #less common format YY-MM-DD detected

        year = filename[0] + filename[1]

        #Convert year from YY to YYYY to get a proper date object
        if (int(year) >= 47 and int(year) <= 99): #earliest file is 1947..
            year = "19" + year
        else:
            year = "20" + year
        month = filename[3] + filename[4]
        day = filename[6] + filename[7]
        simple_date = year + month + day
        date_object = datetime.strptime(simple_date, '%Y%m%d')

    else:
        #Otherwise if it is YYMMDD
        year = filename[0] + filename[1]
        if (int(year) >= 47 and int(year) <= 99):
            year = "19" + year
        else:
            year = "20" + year
        month = filename[2] + filename[3]
        day = filename[4] + filename[5]
        simple_date = year + month + day
        date_object = datetime.strptime(simple_date, '%Y%m%d')

    return [date_object, filename]

def parse_leg_and_session(leg_and_session):
    #Parses a string representing legislature and session, like '21L3S'.

    leg = leg_and_session[0] + leg_and_session[1]
    session = leg_and_session[3]

    parsed = [leg, session]

    return parsed



#so loop over the href of each link
for link in links:
    url = link.get('href')
    if url:
        parsed_url = urlparse(url) #parse the URL into its various components
        path = parsed_url[2] #the path is the second element returned by urlparse
        
        #We only want the Hansard debates, they have a consistent path described above
        #so check for that path
        if path.startswith("/legdocs/Legislative%20Assembly/Hansard/"):
            parsed_path = path.split("/") #split the path into it pieces
            leg_and_session = parsed_path[4] #the string indicating legislature and session should be here
            filename = parsed_path[5] #and the filename here

            #However,as it turns out  someone at the legislative library may have fat fingered a folder while FTPing one time.
            #It looks like they dropped the 20L5S folder inside the 22L2S folder...
            #so we can deal with that
            if (leg_and_session == "22L2S" and filename == "20L5S"): #FUCKERY DETECTED!!
                leg_and_session = parsed_path[5]
                filename = parsed_path[6]

            #Parse the leg and session out
            parsed_leg_and_session = parse_leg_and_session(leg_and_session)
            leg = parsed_leg_and_session[0]
            session = parsed_leg_and_session[1]

            #Parse the filename for the date
            parsed_filename = parse_filename(filename)
            date = parsed_filename[0]
            original_filename = parsed_filename[1]
            
            download_filename = str(date.year) + "_" + str(date.month) + "_" + str(date.day) + "_" + leg + "L" + session + "S" + "_" + original_filename

            data_dir = "hansard_pdfs"

            if not os.path.exists(data_dir):
                    os.makedirs(data_dir)

            #Keep trying if the download fails.  TODO: Handle it with hash/verify/retry
            while True:
                try:
                    download_file = wget.download(url,out=data_dir + '/' + download_filename)
                except:
                    continue
                break

            print("SUCCESS:")
            print(download_file)
