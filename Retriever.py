import json
from tkinter import *

import pickle
import heapq
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer

TOP_K = 20

def load_index(file_path):

    print("Loading inverted index from file...")
    try:
        with open(file_path, 'rb') as file:
            index = pickle.load(file)
    except:
        print("Inverted index cannot be loaded. Please check the file path.")
        raise
    print("Sucessfully loaded inverted index!")
    return index

def construct_ui():
    ui = Tk()
    ui.title("Search Engine")
    ui.geometry("800x450")
    ui.configure(background='white')

    image = PhotoImage(file="ui_logo.gif")
    logo = Label(ui, image=image)
    logo.place(x=150, y=0)

    query = Entry(ui, text='grey')
    query.place(x=330, y=270)

    index = load_index("inverted_index.pickle")
    lemmatizer = WordNetLemmatizer()
    tokenizer = RegexpTokenizer(r'\w+')

    button = Button(ui, text="Search and Print Results to Command Line", command=lambda q=query: retrieve(index, query.get(), None, lemmatizer, tokenizer))
    button.place(x=200, y=330)

    button = Button(ui, text="Search and Print Results to File", command=lambda q=query: retrieve(index, query.get(), "result_urls.txt", lemmatizer, tokenizer))
    button.place(x=500, y=330)

    ui.mainloop()

def retrieve(index, query, file, lemmatizer, tokenizer):
    query_terms = []
    for token in tokenizer.tokenize(query):
        term = token.lower()
        term = lemmatizer.lemmatize(term)
        query_terms.append(term)

    heap = []
    for doc, terms in index.items():
        score = 0
        for q in query_terms:
            try:
                score += terms[q]
            except KeyError:
                continue
        if score != 0:
            heapq.heappush(heap, MaxHeapScoreObj(doc, score))

    json_path = "./WEBPAGES_RAW/bookkeeping.json"
    with open(json_path) as json_file:
            try:
                data = json.load(json_file)
            except ValueError:
                data = None

    if file:
        with open(file, 'w') as output:
            for i in range(TOP_K):
                try:
                    output.write(data[heapq.heappop(heap).docID]+'\n')
                except IndexError:
                    break
        print("Url results have been sucessfully written to file result_urls.txt")
    else:
        print(f"-----------Here are the search results with query: {query}-----------")
        for i in range(TOP_K):
            try:
                print(data[heapq.heappop(heap).docID])
            except IndexError:
                    break
        print("----------------------------------------------------------------------")

class MaxHeapScoreObj():

    def __init__(self, docID, score):
        self.docID = docID
        self.score = score

    def __lt__(self, other):
        # This is inverted because heapq only supports min-heap
        return self.score > other.score

    def __eq__(self, other):
        return self.score == other.score

if __name__ == "__main__":
    construct_ui()