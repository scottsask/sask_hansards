This project attempts to extract data from Saskatchewan Legislature Hansard debate files into a machine readable format.
The files are provided in PDF format.

There are some critical issues with the repository:

1)  Debates through 1976-1977 cannot be accessed, it looks like they are stored on Azure and have a different path than the rest of the data set.  Someone didn't maintain these links.

2)  No checksum is provided for the downloads, so files cannot be verified for integrity or authenticity.

3)  The 20th Legislature, 5th Session (20L5S) folder is sitting inside the 22nd Legislature, 2nd Session's (22L2S) folder.  This is currently accounted for when downloading and naming the files.  It was likely drag-n-dropped in a file explorer/FTP program at some time.

4)  There are two seperate, slightly different PDFs available for the some debates, I'm not sure why at this moment but haven't investigated closely.


General Overview:
The PDFs are largely self-similar between 1947-1983.  They begin to vary quite a bit after that.

Strategy:
Target a large portion of the dataset first, 1947-1983, then deal with the rest.


---
Project Files
---
download.py -- attempts to download and consistently rename every Hansard debate PDF
extract.py -- uses Tika to extract all text data from each PDF file downloaded, leaving a .txt file for each pdf
clean.py -- remove repeated page data and page numbers
normalize.py -- label subject headings, convert em dashes to double dashes
main.py -- output a machine readable format

---
Cleanup
---
Remove page header dates, page numbers
Remove prologues
Handle subject/topic headings

---
Normalizing Speaker Names
---
Normalize speaker names

---
Associate Additional Data with Speakers
---
Party Affiliation
Riding represented
Gender
Portfolios
