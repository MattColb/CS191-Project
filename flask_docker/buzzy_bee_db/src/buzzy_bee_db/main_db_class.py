from dotenv import load_dotenv



load_dotenv()

class DBInteraction:
    self.connection_string = os.getenv("MONGODB_CONN_STRING")
    self.account_interaction = ""