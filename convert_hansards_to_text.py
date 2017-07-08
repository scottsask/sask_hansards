import os
import tika
tika.initVM()

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

        to_text = fn + '_to_text.txt'

        #f = open(to_text, 'w+')
        #f.write(metadata)
        #f.write(content.encode('utf8'))
        #f.close()
