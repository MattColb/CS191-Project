class SubjectClass:
    def __init__(self, qtype, rating):
        self.rating=rating
        self.qtype=qtype

    def create_question(self):
        print("Create a Question!")

    def get_closest_questions(self):
        print("Get a question close to our rating!")

    def check_answer(self, user_answer, answer):
        return user_answer == answer
    
    def update_rating(self, student_id, new_rating):
        print("Updating the student rating here")

    def redirect(self):
        print("Return a redirect to create the loop")