from Documents import Documents
from Appearance import Appearance
from collections import defaultdict
import pickle
import math

from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer


# Words that will not be included in the inverted indexing
STOP_WORDS = open('stop_words.txt', 'r').read().split()

# A dict that indicates how many frequency and rankings will be added based on the html tag
# (tags): (freq, rank)
HTML_RANK = {'body':(1,0), ('strong', 'b'):(1,2), ('h1','h2','h3'):(1,4)}

class Indexer:
    """
    This class is used to produce inverted index of the documents.

    Attributes:
        index: a dictionary that maps the token to the Apperarance class which contains
               the information of the token in a specific file. str: <Appearance>
    """
    def __init__(self):
        self.index = defaultdict(list)
        self.Documents = Documents("./WEBPAGES_TEST/", "./WEBPAGES_RAW/bookkeeping.json")
        self.tdMatrix = defaultdict(dict)

    def construct_index(self):
        for docID, path in self.Documents:
            try:
                with open(path, encoding="utf-8") as data:
                    soup = BeautifulSoup(data.read(), "html.parser")
                    tokenizer = RegexpTokenizer(r'\w+')
                    lemmatizer = WordNetLemmatizer()
            except IOError:
                # Ignoring path that not exists
                continue
            for tag in HTML_RANK.keys():
                self._extract_content(soup, tokenizer, lemmatizer, tag, docID)
        # self.index = dict(sorted(self.index.items(), key = lambda x: x[0]))
        self._construct_tdMatrix()
        self._index_to_file("inverted_index.pickle")

        # documents_set = set()
        # for posting in self.index.values():
        #     for app in posting:
        #         documents_set.add(app.docID)

        print("Finished constructing inverted index on all documents.")
        print(f"Total number of valid documents is {len(self.tdMatrix.keys())}.")
        print(f"Total number of unique words is {len(self.index.keys())}.\n")

    def _extract_content(self, soup, tokenizer, lemmatizer, tag, docID):

        global STOP_WORDS

        print(f"PROCESSING INVERTED INDEX ON DOCUMENT {docID}...")

        temp_dict = {}

        for content in soup.find_all(tag):
            for token in tokenizer.tokenize(content.text):
                token = token.lower()
                token = lemmatizer.lemmatize(token)

                if token in STOP_WORDS:
                    continue

                if token not in temp_dict:
                    temp_dict[token] = [HTML_RANK[tag][0], HTML_RANK[tag][1]]
                else:
                    temp_dict[token][0] += HTML_RANK[tag][0]
                    temp_dict[token][1] += HTML_RANK[tag][1]

        for term, info in temp_dict.items():
            self.index[term].append(Appearance(docID, info[0], info[1]))

    def _construct_tdMatrix(self):
        num_doc = len(self.Documents.files_dict)
        rank_normalizer = 20.0
        for term, posting in self.index.items():
            df = len(posting)
            for app in posting:
                gd = app.ranking / rank_normalizer if app.ranking <= 20 else 1
                weight = (1+math.log10(app.frequency))*math.log10(num_doc/df) + gd if app.frequency != 0 else 0
                self.tdMatrix[app.docID][term] = weight
        # Normalization
        for doc, terms in self.tdMatrix.items():
            factor = math.sqrt(math.fsum(w*w for w in terms.values()))
            for t, w in terms.items():
                terms[t] = w / factor

    def _index_to_file(self, file_path):
        with open(file_path, 'wb') as file:
            pickle.dump(dict(self.tdMatrix), file, protocol=pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":
    indexer = Indexer()
    indexer.construct_index()
