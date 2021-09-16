class Appearance:
    """
    This class represents the the appearance of a term in a specific document, 
    which includes stuffs like docID and word frequency

    Attributes:
        docID: Data that represents a unique document
        frequency: the frequency of this term in this document
        ranking: A number that indicates how relevant this document is
    """
    def __init__(self, docID, frequency, ranking):
        self.docID = docID
        self.frequency = frequency
        self.ranking = ranking

    def __str__(self):
        return f"{self.docID},{self.frequency},{self.ranking}"

if __name__ == "__main__":
    app = Appearance('110/1', 2, 3)
    print(app)