import os
from pinecone import Pinecone, ServerlessSpec


pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

POSTS_STORE = "forum-management"
GUIDELINES_STORE = "guidelines"

if POSTS_STORE not in pc.list_indexes().names():
    pc.create_index(name=POSTS_STORE, metric="cosine", dimension=1536,  spec=ServerlessSpec( 
            cloud='aws',       
            region='us-east-1'
        ))
    
if GUIDELINES_STORE not in pc.list_indexes().names():
    pc.create_index(name=GUIDELINES_STORE, metric="cosine", dimension=1536,  spec=ServerlessSpec( 
            cloud='aws',       
            region='us-east-1'
        ))
     


# Connect to the index
index = pc.Index(POSTS_STORE)
gindex = pc.Index(GUIDELINES_STORE)
# thindex = pc.Index(THREAD_INDEX)



