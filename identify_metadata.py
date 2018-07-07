#hansard_colon -*- coding: utf-8 -*-
import re
import os

##
##Creates an XML object from the cleaned Hansard text files
##tagging all metadata including things like front page information
##and table of contents at the end.
##


soup = BeautifulSoup(features='xml')


#Regex for identifying metadata such as front page, table of contents

#usually everything above this regex is frontmatter
leg_assembly_header = re.compile(r'(\n\s?LEGISLATIVE ASSEMBLY OF.*\n)', re.UNICODE)

#'assembly/house' resumed can appear anywhere, but usually when they met appears at the start
assembly_met = re.compile(r'(\n\[?the (assembly|house) (met|resumed|adjourned|recessed) (at|until))', re.UNICODE|re.IGNORECASE)

#this occurs in most Hansards, in a few its one of the only frontmatter elements:
hansard_colon = re.compile(r'((\nHansard:\s?(January|February|March|April|May|June|July|August|September|October|November|December)))')

#When no "the assembly met at" is found, it's likely an evening session
#About 967 of these
evening_session = re.compile(r'(\nEVENING (SESSION|SITTING))', re.UNICODE)

#this occurs at the end of the document
table_of_contents = re.compile(r'((\n\s?TABLE OF CONTENTS\s?\n))')

#many documents have a timestamp written as (0000)
#24hr format
timestamp_regex = r"\n\(?[0-9]{1,4}\)?\s\n"

data_directory = './hansard_txts/'
files_read = 0
for filename in os.listdir(data_directory):
    #if filename.startswith('19'):
        files_read += 1
        with open(data_directory + filename, 'rw+') as f:
		text = f.read()

        found_flag = False
        for found in re.findall(assembly_met, text):
            #print(found)
            print(found[0]) #the 0th element is the whole match
            found_flag = True
            #assembly_time_flag = True


        #if not found_flag:
            #print(filename)

          #for found in re.findall(evening_session, text):
              #print(found[0])
              #print(found[1])
              #assembly_time_flag = True

          #if not assembly_time_flag:
              #print(text)
