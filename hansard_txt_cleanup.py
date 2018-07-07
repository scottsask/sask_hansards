# -*- coding: utf-8 -*-
import re
import os


#start by removing newlines from strings
#just so we dont run them over when removing per-page data like page numbers
bills = re.compile(r'((\nBill No.\s[0-9]{1,4}.*,\s?\n+[0-9]{4}?))')
def remove_newlines_from_bills(match):
    match = match.group()
    match = match.replace("\r","")
    match = match.replace("\n","")
    return match

###
### Regex for cleaning up repeated Hansard per page formatting, e.g. page numbers, publication information, etc
###


###
### From 1991 onward
###


#The following two strings occur, alternating, one per page on hansards past 1991
#190 Saskatchewan Hansard December 10, 1991
#December 10, 1991 Saskatchewan Hansard 191

per_page_data_one = re.compile(r'([0-9]{1,5}\sSaskatchewan Hansard\s(January|February|March|April|May|June|July|August|September|October|November|December).*)')
per_page_data_two = re.compile(r'((January|February|March|April|May|June|July|August|September|October|November|December)\s[0-9]{1,2},\s[0-9]{1,4}\sSaskatchewan Hansard\s[0-9]{1,5})')

#A date like 'January 1, 2005' occurs often on a line by itself
date_regex = re.compile(r'\n((January|February|March|April|May|June|July|August|September|October|November|December)\s[0-9]{1,2},\s[0-9]{4}\s?\n)')

#There are page numbers, that often have a space after them
page_number_regex = re.compile(r'\n[0-9]{1,4}\s?\n')


data_directory = '/home/scott/Hansard/sask_hansards/'
for filename in os.listdir(data_directory + "hansard_txts/"):
    if filename.endswith('txt'):
        with open(data_directory + 'hansard_txts/' + filename, 'rw+') as f:

            text = f.read()

            text = re.sub(bills, remove_newlines_from_bills, text) 
            text = re.sub(per_page_data_one, '', text)
            text = re.sub(per_page_data_two, '', text)
            text = re.sub(page_number_regex, '', text)

            if filename.startswith('19'):
                text = re.sub(date_regex, '', text)

        fn = filename
        new_file = open(data_directory + "cleaned_txts/" + fn, 'w')
        new_file.write(text)
        new_file.close()
