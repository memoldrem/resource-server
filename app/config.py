import os
from dotenv import load_dotenv

load_dotenv()
# implement environemnt variables

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable modification tracking
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    # probably want to change username + password
    

    MONGO_URI = os.getenv('MONGO_URI')

    NEO4J_URI = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
    NEO4J_USER = os.getenv('NEO4J_USER', 'neo4j')
    NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')
    

    PINECONE_API_KEY = os.getenv('PINECONE_API_KEY', 'your-pinecone-api-key')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your-openai-api-key')


    VALIDATION_ENDPOINT = os.getenv('VALIDATION_ENDPOINT', 'http://localhost:3001/validate')
