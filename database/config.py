import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    HOST = os.getenv("DB_HOST", "localhost")
    USER = os.getenv("DB_USER", "root")
    PASSWORD = os.getenv("DB_PASSWORD", "Nguari2006")
    DATABASE = os.getenv("DB_NAME", "ticketgest")
    PORT = int(os.getenv("DB_PORT", 3306))