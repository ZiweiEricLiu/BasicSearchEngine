REQUIREMENTS
------------
This module requires the following modules:
beautifulsoup4 (4.9.3)
lxml (4.6.2)
nltk (3.5)
regex (2020.11.13)

Description of Each .py File
------------
-Appearance.py
This module contains a class represents the the appearance of a term in a specific document, 
which includes stuffs like docID and word frequency

-Documents.py
This module contains a class works as a generator that does os process
and yield the document and its id

-Indexer.py
This module is used to produce inverted index and term-document matrix of the documents
Index will be written to a file named "inverted_index.pickle"

-Retriever.py
This module contains codes for GUI and receival process

Setup to Run the Code
------------
Please put the WEBPAGES_RAW folder at the same directory of the .py files

If that's not possible:
You may change the directory of the document in the __init__ function of Indexer.py,
where it is currently like this

"self.Documents = Documents("./WEBPAGES_RAW/", "./WEBPAGES_RAW/bookkeeping.json")"

change the "./WEBPAGES_RAW/" to a directory at your computer

Notice: the json file has to be in this folder, otherwise the code won't work