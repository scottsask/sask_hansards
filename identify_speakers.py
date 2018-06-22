# -*- coding: utf-8 -*-
import re
import os
import pprint


###
### Regex for identifying speakers
###

#finds speakers in the majorityy of documents, 5058/5137 total documents have at least 1 match
speaker = re.compile(r'(\n(Mr\.|Mrs\.|An Hon\. Member|Premier|Hon\.|Ms\.|Some).*?:\s*(—|–|-{1,2}| |)\s*)', re.UNICODE|re.IGNORECASE)


#for the remaning ~100 or so documents that have a different formatting for speakers
#e.g.:
#MR. A. THIBAULT: (Melfort-Kinistino)
#SOME HON. MEMBERS:
speaker_alternative = re.compile(r'((\n(mr|some|hon|mrs|ms).*?:\s*)(\(*.+\))?)', re.UNICODE|re.IGNORECASE)

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

        if (found_counter != 0):
            hansards_with_speakers += 1

        #second pass using alternative regex
        #show text of hansards that found 0 speakers with the speaker regex
        if (found_counter==0):
          for found in re.findall(speaker_alternative, text):
            found_counter += 1
            print(found[0])
            #print("Found: " + str(found_counter) + " in " + filename)
          if (found_counter != 0):
            hansards_with_speakers += 1
          if (found_counter == 0):
            #print(text)
            hansards_without_speakers.append(filename)


print("\n" + str(hansards_with_speakers) + " out of " + str(total_files) + " have speakers in them \n")

print("These " + str(len(hansards_without_speakers)) + " files currently have 0 speakers detected in them: \n")

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(hansards_without_speakers)
print("\n")

#Really odd formatting:
#1955_3_28_12L3S_550328Debates.txt
