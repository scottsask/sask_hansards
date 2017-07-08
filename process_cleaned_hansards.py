# -*- coding: utf-8 -*-
import re
import os
from verbalexpressions import VerEx

verbal_expression = VerEx()

#Take out page numbers ( per page -- count them?), sometimes coupled with...
#Take out "Hansard Saskatchewan" page headers
#Sometimes its just a date per page, so \nDate\n.  Always the date of the pub, maybe look for that.

#HARD PROBLEMS
#Headings/subject topics in the transcripts
#normalizing/labelling speaker names, titles, riding associations, party etc

#speaker = re.compile(r'(\n.*?:\s[—|\-{1,2}])', re.UNICODE | re.DOTALL)

speaker = re.compile(r"^.:", re.UNICODE)

data_directory = './data/cleaned_data/'
for filename in os.listdir(data_directory):
    date_to_parse = filename.split("_")
    print(date_to_parse)
    if filename.endswith('.txt'):
        with open(data_directory + filename, 'r') as f:
		text = f.read()

#        text.decode("utf-8").replace(u"\u2014","--")
#        print("REPLACED!")

        for speaker_found in re.findall(speaker, text):
            print("MATCH:\n")
            print(speaker_found)

#def remove_page_crap():
#    remove_page_dates()
#    remove_page_numbers()
#    remove_hansard_headers()

#def remove_page_dates(lines):

#regex
#looks for "someone: -- "
