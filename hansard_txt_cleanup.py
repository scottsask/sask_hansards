# -*- coding: utf-8 -*-
import re
import os


#Take out page numbers ( per page -- count them?), sometimes coupled with...
#Take out "Hansard Saskatchewan" page headers
#Sometimes its just a date per page, so \nDate\n.  Always the date of the pub, maybe look for that.

#HARD PROBLEMS
#Headings/subject topics in the transcripts
#normalizing/labelling speaker names, titles, riding associations, party etc

speaker = re.compile(r'(\n.*:\s?[—|\-{1,2}])', re.UNICODE | re.DOTALL)



### REMOVING RESIDUAL PAGE HEADER/FOOTER CRUFT

#From 1991 onward, there is "1111 Saskatchewan Hansard" string on every other page
per_page_data_past_91 = r"\n\d*\sSaskatchewan Hansard.*\n"

#There is also often date like 'January 1, 2005' hanging out on a line by itself
date_regex = r"(\n)(January|February|March|April|May|June|July|August|September|October|November|December)(\s)(\d|\d\d)(,)(\s)(\d\d\d\d|\d\d\d\d)"

#There are page numbers, that often have a space after them, hanging out alone on a line by themselves sometimes as well
page_number_regex = r"(\n)(\d|\d\d|\d\d\d|\d\d\d\d)(\s?)(\n)"

#Tricky part...try for subject headings...that are words that are capitalized consecutively, or all caps, on a line, usually.
#caps_subject_heading = r"\n[A-Z][A-Z]*\s+[A-Z][A-Z]*\s+"
caps_subject_heading = r"\n[A-Z][A-Z]*\s+"




data_directory = './data/cleaned_data/'
for filename in os.listdir(data_directory):
    if filename.endswith('.txt'):
        with open(data_directory + filename, 'rw+') as f:
		text = f.read()

#        text.decode("utf-8").replace(u"\u2014","--")
#        print("REPLACED!")

        for found in re.findall(caps_subject_heading, text):
            print(found)

        #Regex text cleaning pipeline, remove all that page crap
        #clean_text = re.sub(date_regex, '',  text)
        #cleaner_text = re.sub(per_page_data_past_91, '', clean_text)
        #cleanest_text = re.sub(page_number_regex, '', cleaner_text)
        #fn = filename + 'CLEANTEST.txt'
        
        #f = open(data_directory + "/cleaned_data/" + fn, 'w+')
        #f.write(cleanest_text)
        #f.write(cleanest_text)
        #f.close()




#def remove_page_crap():
#    remove_page_dates()
#    remove_page_numbers()
#    remove_hansard_headers()

#def remove_page_dates(lines):

#regex
#looks for "someone: -- "
