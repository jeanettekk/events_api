import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# Set the SQLALCHEMY_DATABASE_URI from the .env file
class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Enables SQL query logging for debugging
    SQLALCHEMY_ECHO = True
