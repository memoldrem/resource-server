import os
# from dotenv import load_dotenv

# load_dotenv()
# implement environemnt variables

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable modification tracking
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://username:password@localhost/forum_db')
    # probably want to change username + password
    
    # MongoDB URI and other settings
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')

    # Neo4j credentials
    NEO4J_URI = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
    NEO4J_USER = os.getenv('NEO4J_USER', 'neo4j')
    NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD', 'password')
    
    # API Keys
    PINECONE_API_KEY = os.getenv('PINECONE_API_KEY', 'your-pinecone-api-key')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your-openai-api-key')
