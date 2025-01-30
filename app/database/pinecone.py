import os
from pinecone import Pinecone, ServerlessSpec


pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

INDEX_NAME = "forum-management"
# THREAD_INDEX = "threads"

if INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(name=INDEX_NAME, metric="cosine", dimension=1536,  spec=ServerlessSpec( 
            cloud='aws',       
            region='us-east-1'
        ))
    
# if THREAD_INDEX not in pc.list_indexes().names():
#     pc.create_index(name=THREAD_INDEX, metric="cosine", dimension=1536,  spec=ServerlessSpec( 
#             cloud='aws',       
#             region='us-east-1'
#         ))
    


# Connect to the index
index = pc.Index(INDEX_NAME)
# thindex = pc.Index(THREAD_INDEX)



