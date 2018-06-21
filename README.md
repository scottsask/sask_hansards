---
Toward Machine Readable Saskatchewan Hansards
---

This project attempts to convert all Saskatchewan Legislature Hansard debate transcripts, which are provided in PDF format, into a machine readable format.

After submitting a form on this page http://www.legassembly.sk.ca/legislative-business/meetings/ a complete listing of Hansard PDFs available for download is generated.  The file get_hansards.py attempts to submit this form, retrieve all download links, then consistently rename and download each PDF.

There are some major issues with the source repository:

1)  No checksum is provided for the downloads, so files cannot be verified for integrity or authenticity.

2)  The 20th Legislature, 5th Session (20L5S) folder is sitting inside the 22nd Legislature, 2nd Session's (22L2S) folder.  This is currently accounted for when downloading and naming the files.  It was likely drag-n-dropped in a file explorer/FTP program at some time.

3)  There are two seperate, slightly different PDFs available for the some debates, I'm not sure why.

General Overview:
The PDFs are largely self-similar between 1947-1983.  They begin to vary quite a bit after that.

Strategy:
Target a large portion of the dataset first, 1947-1983, then deal with the rest.

---
Working Files (quick start)
---
All PDF files downloaded as of June 6th, 2018 using the get_hansards.py script:
https://hansards.nyc3.digitaloceanspaces.com/2018-Jun-06-hansard_pdfs.tar.gz

All plain text files extracted from the above PDFs using Apache Tika and the hansard_pdfs_to_txt.py script:
https://hansards.nyc3.digitaloceanspaces.com/2018-Jun-06-hansard_txts.tar.gz


Note:  The above primary source PDFs and corresponding .txt files are up to date as of June 6th, 2018.


---
Project Files
---
get_hansards.py -- attempts to download and consistently rename every Hansard debate PDF

hansard_pdfs_to_txt.py -- uses Tika to extract all text data from each PDF file downloaded, leaving a .txt file for each pdf

hansard_txt_cleanup.py -- remove repeated page data and page numbers

---
Todo: Cleanup
---
Remove page header dates, page numbers, misc cruft leftover from the PDF to text conversion process

---
Todo: Data Augmentation
---
Create basic document hierarchy using Hansard sections, e.g. "ORDERS OF THE DAY"

Normalize speaker names

Label all subject/topic headings

Extract prologues, tables of contents, etc

The goal is to produce a structured document for each Hansard, maybe something like:
```
<Hansard>
  <Section>
  ORDERS OF THE DAY
    <Speaker>Mr. Douglas</Speaker><SpokenWords>Things Mr. Douglas said</SpokenWords>

    <Topic>Universal Healthcare
      <Speaker>Mr. Douglas</Speaker><SpokenWords>Some words about healthcare</SpokenWords>
    </Topic>

  </Section>
</Hansard>
```
    
  


---
Todo: Create a database enabling us to associate additional data with all speakers
---
Party Affiliation

Riding represented

Gender

Portfolios
