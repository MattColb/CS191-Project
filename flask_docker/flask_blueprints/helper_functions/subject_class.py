class SubjectClass:
    def __init__(self, qtype, rating):
        self.rating=rating
        self.qtype=qtype

    def create_question(self):
        print("Create a Question!")