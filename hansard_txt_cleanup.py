# -*- coding: utf-8 -*-
import re
import os


###
### Regex for identifying speakers
###

#This regex covers the majority of documents quite well, 5058/5137 total documents match this pattern corectly
speaker = re.compile(r'(\n(Mr\.|Mrs\.|An Hon\. Member|Premier|Hon\.|Ms\.|Some).*?:\s*(—|–|-{1,2}| |)\s*)', re.UNICODE|re.IGNORECASE)

#This regex is for the remaning ~100 or so documents that have a different formatting
speaker_alternative = ''

###
### Regex for cleaning up Hansard per page formatting, e.g. page numbers or redundant title information
###
#From 1991 onward, there is "1111 Saskatchewan Hansard" string on every other page
per_page_data_past_91 = r"\n\d*\sSaskatchewan Hansard.*\n"

#There is also often date like 'January 1, 2005' hanging out on a line by itself
date_regex = r"(\n)(January|February|March|April|May|June|July|August|September|October|November|December)(\s)(\d|\d\d)(,)(\s)(\d\d\d\d|\d\d\d\d)"

#There are page numbers, that often have a space after them, hanging out alone on a line by themselves sometimes as well
page_number_regex = r"(\n)(\d|\d\d|\d\d\d|\d\d\d\d)(\s?)(\n)"

data_directory = './hansard_txts/'
total_files = 0
hansards_with_speakers = 0
hansards_without_speakers = []
for filename in os.listdir(data_directory):
    #if filename.startswith('19'):
        total_files += 1
        with open(data_directory + filename, 'rw+') as f:
		text = f.read()

        found_counter = 0 #counting number of matches in a document
        for found in re.findall(speaker, text):
            found_counter += 1
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

        if (found_counter != 0):
            hansards_with_speakers += 1

        #show text of hansards that found 0 speakers with the speaker regex
        if (found_counter==0):
          hansards_without_speakers.append(filename)
          #print("Found: " + str(found_counter) + " in " + filename)
          #print(text)


print(str(hansards_with_speakers) + " out of " + str(total_files) + " have speakers in them \n")


print("These files currently have 0 speakers detected in them: \n")
print(str(hansards_without_speakers))







#def remove_page_crap():
#    remove_page_dates()
#    remove_page_numbers()
#    remove_hansard_headers()

#def remove_page_dates(lines):
