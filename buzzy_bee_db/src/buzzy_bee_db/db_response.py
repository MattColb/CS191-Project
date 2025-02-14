class DB_Response:
    def __init__(self, success, message):
        self.success = success
        self.message = message

    def get_success(self):
        return self.success

    def get_message(self):
        return self.message

    def set_message(self, message):
        self.message = message

    def set_success(self, success):
        self.success = success