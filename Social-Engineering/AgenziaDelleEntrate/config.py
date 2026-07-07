from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")

    FAKE_CODICE_FISCALE = os.getenv("FAKE_CODICE_FISCALE")
    FAKE_PASSWORD = os.getenv("FAKE_PASSWORD")
