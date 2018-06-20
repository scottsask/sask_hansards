import os
import tika
tika.initVM()

#you must have tika-server downloaded and running
#https://tika.apache.org/download.html
#you can 'pip install tika'

from tika import parser


for fn in os.listdir('.'):
    if os.path.isfile(fn) and not fn.startswith('.'):

        print("file:")
        print(fn)

        text = parser.from_file(fn)

        metadata = text["metadata"]
        content = text["content"]

        for item in metadata:
            print(item)

        to_text = 'text_' + fn + '.txt'

        f = open(to_text, 'w+')
        f.write(metadata)
        f.write(content.encode('utf8'))
        f.close()
