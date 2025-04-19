import dotenv
import os

def load_config():
    dotenv.load_dotenv()
    return {
        "OPENAI_API_KEY" : os.getenv("OPENAI_API_KEY"),
        "DB_CONNECTION"  : os.getenv("DB_CONNECTION")
    }