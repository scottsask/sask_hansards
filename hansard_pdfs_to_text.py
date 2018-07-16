import os
import tika
tika.initVM()

#you must have tika-server downloaded and running
#http://www.apache.org/dyn/closer.cgi/tika/tika-server-1.18.jar

#'pip install tika' will grab the library used by this script to interact with the Tika server

#once the tika server is running, you can place this script in the folder containing Hansard PDFs
#run the script to convert the PDFs to txt files

from tika import parser

data_dir = "hansard_pdfs"
output_dir = "hansard_txts"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)


for fn in os.listdir('./' + data_dir):
    if os.path.isfile(data_dir + '/' + fn) and not fn.startswith('.'):

        print("file:")
        print(fn)

        filename, file_extension = os.path.splitext(fn) 

        text = parser.from_file(data_dir + '/' + fn)

        metadata = text["metadata"]
        content = text["content"]

        to_text = filename + '.txt'

        f = open(output_dir + '/' + to_text, 'wb')
        #f.write(str(metadata))
        f.write(content.encode('utf8'))
        f.close()
