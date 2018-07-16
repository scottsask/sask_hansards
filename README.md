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
Quick Start -- Just download an archive of already renamed PDFs and converted texts
---
All PDF files downloaded as of June 6th, 2018 using the get_hansards.py script:
https://hansards.nyc3.digitaloceanspaces.com/2018-Jun-06-hansard_pdfs.tar.gz

All plain text files extracted from the above PDFs using Apache Tika and the hansard_pdfs_to_txt.py script:
https://hansards.nyc3.digitaloceanspaces.com/2018-Jun-06-hansard_txts.tar.gz


Note:  The above primary source PDFs and corresponding .txt files are up to date as of June 6th, 2018.


---
From Scratch -- Scrape the Saskatchewan Legislative Assembly site for the Hansard PDFs, convert them to text with Apache Tika
---
To get started:
```
git clone https://github.com/scottsask/sask_hansards.git

cd sask_hansards

python3 -m venv venv

source venv/bin/activate

pip3 install -r requirements.txt

```

Next, download all the Hansard PDF files to a folder hansard_pdfs/ and consistently rename each one.  This can take a while.
```
python3 get_hansards.py
```

Once all the Hansards are downloaded, we need to convert the PDFs to plaintext files.
Download and and start running Apache Tika Server (http://www.apache.org/dyn/closer.cgi/tika/tika-server-1.18.jar):
```
wget http://mirror.csclub.uwaterloo.ca/apache/tika/tika-server-1.18.jar
java -jar tika-server1.18.jar
```

With Tika running, in a new terminal window we can convert the Hansard PDFs to plaintext files now (again, this can take a while):
```
python3 hansard_pdfs_to_txt.py
```

We'll remove repeated per-page data and other data we won't be using:
```
python3 hansard_txt_cleanup.py
```


identify_speakers.py -- regular expressions and loops for identifying speaking parts in sask hansards

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


---
Handy Tricks
---
Create a diff file showing changes between original and clean up

```for file in hansard_txts/*.txt; do diff "$file" "cleaned_txts/${file##*/}"; done > diffs.txt```
