# -*- coding: utf-8 -*-
import re
import os
from titlecase import titlecase


#To identify subjects and topics, we'll use regex to start
#but use Python string methods on the matches to determine if the line is
#all caps or title case.  For the most part, subjects are either a line in
#all caps, or title case, with no punctuation at the end.

###
### Regex for identifying titles
###

### Regex for identifying candidate subject/topics
subject = re.compile(r"\n[^\s\d\n\[\(\.\-—_\$].+\s\n", re.UNICODE)

data_directory = './cleaned_txts/'
for filename in os.listdir(data_directory):
    #if filename.startswith('19'):
        with open(data_directory + filename, 'r', encoding="utf-8") as f:
            text = f.read()

        assembly_time_flag = False
        for found in re.findall(subject, text):
            #if found.upper() == found and not found.endswith('. \n') and not found.endswith('.') and not found.endswith('. ') and not found.startswith('HON') and not found.startswith('\nYEA') and not found.startswith('\nNAY') and not found.startswith("'"):
              #print(found) #the 0th element is the whole match
            if titlecase(str(found)) == found and '.' not in found and '?' not in found and '(' not in found and 'Hon' not in found:
                print(found)
            assembly_time_flag = True

        #if not assembly_time_flag:

          #for found in re.findall(evening_session, text):
              #print(found[0])
              #print(found[1])
              #assembly_time_flag = True

          #if not assembly_time_flag:
              #print(text)
