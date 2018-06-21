# -*- coding: utf-8 -*-
import re
import os


#Take out page numbers ( per page -- count them?), sometimes coupled with...
#Take out "Hansard Saskatchewan" page headers
#Sometimes its just a date per page, so \nDate\n.  Always the date of the pub, maybe look for that.

speaker = re.compile(r'(\n(Mr\.|Mrs\.|An Hon\. Member|Premier|Hon\.|Ms\.|Some).*?:\s?(—|-{1,2}| )\s?)', re.UNICODE|re.IGNORECASE)

### REMOVING RESIDUAL PAGE HEADER/FOOTER CRUFT

#From 1991 onward, there is "1111 Saskatchewan Hansard" string on every other page
per_page_data_past_91 = r"\n\d*\sSaskatchewan Hansard.*\n"

#There is also often date like 'January 1, 2005' hanging out on a line by itself
date_regex = r"(\n)(January|February|March|April|May|June|July|August|September|October|November|December)(\s)(\d|\d\d)(,)(\s)(\d\d\d\d|\d\d\d\d)"

#There are page numbers, that often have a space after them, hanging out alone on a line by themselves sometimes as well
page_number_regex = r"(\n)(\d|\d\d|\d\d\d|\d\d\d\d)(\s?)(\n)"

data_directory = './hansard_txts/'
for filename in os.listdir(data_directory):
    if filename.startswith('19'):
        with open(data_directory + filename, 'rw+') as f:
		text = f.read()

#        text.decode("utf-8").replace(u"\u2014","--")
#        print("REPLACED!")

        for found in re.findall(speaker, text):
            print(found[0]) #the 0th element is the whole match
            #print(found[1])

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
