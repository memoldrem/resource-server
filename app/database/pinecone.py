import os
from pinecone import Pinecone, ServerlessSpec


pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

INDEX_NAME = "forum-posts"

# Create or connect to an existing index
if INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(name=INDEX_NAME, metric="cosine", dimension=3072,  spec=ServerlessSpec(  # Specify the spec here
            cloud='aws',        # You can specify your cloud provider and region
            region='us-east-1'
        ))

# Connect to the index
index = pc.Index(INDEX_NAME)

