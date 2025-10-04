from langchain_community.utilities import SQLDatabase
from app.core.config import DATABASE_URL

db = SQLDatabase.from_uri(DATABASE_URL)
