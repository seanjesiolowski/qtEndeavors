from db import DB


# might be a "custom type"
class Endeavor():
    def __init__(self, big_idea):
        self.id = None
        self.big_idea = big_idea
        self.details = None


class Collection():
    def __init__(self):
        self.collection = []
        self.db = DB()
        list = self.db.initial_read()
        for entry in list:
            new_endeavor = Endeavor(entry[1])
            new_endeavor.index = entry[0]
            new_endeavor.details = entry[2]
            self.collection.append(new_endeavor)

    # -------------------- data to front --------------------
    def create_endeavor(self, big_idea):
        endeavor = Endeavor(big_idea)
        self.collection.append(endeavor)

    def read_endeavor(self, index):
        return self.collection[index]

    def update_endeavor(self, index, details):
        self.collection[index].details = details

    def delete_endeavor(self, index):
        self.collection.pop(index)

    # -------------------- data to back --------------------
    def data_to_db(self):
        self.db.update_db(self.collection)
