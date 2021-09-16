import json

class Documents:
    """
    This class works as a generator that does os process
    and yield the document and its id

    Attributes:
        files_dict: a dictionary that uses the folder path in the json file as the key (docID) 
                    and maps it to the actual file path. id: path
    """
    def __init__(self, doc_path, json_path):
        self.files_dict = dict()

        with open(json_path) as json_file:
            try:
                data = json.load(json_file)
            except ValueError:
                data = None

            for d in data:
                file = doc_path + d
                self.files_dict[d] = file

    def __iter__(self):
        return iter(self.files_dict.items())

if __name__ == "__main__":
    test = Documents("./WEBPAGES_RAW/", "./WEBPAGES_RAW/bookkeeping.json")
    for id, path in test:
        print(f"{id}: {path}")