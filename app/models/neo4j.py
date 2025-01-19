from neo4j import GraphDatabase
from app.config import DATABASES

neo4j_driver = GraphDatabase.driver(
    DATABASES["neo4j"]["uri"], 
    auth=(DATABASES["neo4j"]["user"], DATABASES["neo4j"]["password"])
)
