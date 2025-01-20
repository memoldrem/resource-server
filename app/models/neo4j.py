from neo4j import GraphDatabase
import os

# Get Neo4j connection details from environment variables
NEO4J_URI = os.getenv("NEO4J_URI", "neo4j://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "<your-neo4j-password>")

# Create a Neo4j driver instance
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

# Example of querying the graph database
def query_neo4j(query):
    with driver.session() as session:
        result = session.run(query)
        return result.data()
