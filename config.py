from dotenv import load_dotenv
import os

load_dotenv()

db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")
db_port = os.getenv("DB_PORT")

redis_port = os.getenv("REDIS_PORT")
redis_host = os.getenv("REDIS_HOST")

