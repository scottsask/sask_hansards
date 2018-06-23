# -*- coding: utf-8 -*-
import re
import os

###
### Regex for identifying frontmatter
###

#4201 documents have some form of "the assembly met at" indicating start time
assembly_met = re.compile(r'(\n\[?the (assembly|house) met at)', re.UNICODE|re.IGNORECASE)

#When no "the assembly met at" is found, it's likely an evening session
#About 967 of these
evening_session = re.compile(r'(\nEVENING (SESSION|SITTING))', re.UNICODE)

data_directory = './hansard_txts/'
for filename in os.listdir(data_directory):
    #if filename.startswith('19'):
        with open(data_directory + filename, 'rw+') as f:
		text = f.read()

        assembly_time_flag = False
        for found in re.findall(assembly_met, text):
            #print(found)
            print(found[0]) #the 0th element is the whole match
            assembly_time_flag = True

        if not assembly_time_flag:

          for found in re.findall(evening_session, text):
              print(found[0])
              #print(found[1])
              assembly_time_flag = True

          #if not assembly_time_flag:
              #print(text)
