import pinecone
import os

# Get Pinecone API key from environment variables
pinecone_api_key = os.getenv("PINECONE_API_KEY", "<your-pinecone-api-key>")
pinecone.init(api_key=pinecone_api_key, environment="us-west1-gcp")  # Replace with your region

# Create and configure an index (for example, for vector search)
index_name = "forum_vectors"
pinecone.create_index(name=index_name, dimension=512)  # Assuming your vectors have 512 dimensions

# Connect to the index
index = pinecone.Index(index_name)
