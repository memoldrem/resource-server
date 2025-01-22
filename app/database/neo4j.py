from neo4j import GraphDatabase
from flask import Flask, request, jsonify
import os

# Get Neo4j connection details from environment variables
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "forum_management")

# Create a Neo4j driver instance
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))


# Helper function to run Cypher queries
def run_query(query, parameters=None):
    with driver.session() as session:
        result = session.run(query, parameters or {})
        return result

try:
    with driver.session() as session:
        result = session.run("MATCH (n) RETURN n LIMIT 1")
        print("Connected successfully!")
        for record in result:
            print(record)
except Exception as e:
    print(f"Failed to connect: {e}")


    # User model
class User:
    @staticmethod
    def create(username, role):
        query = """
        CREATE (u:User {username: $username, role: $role})
        RETURN u
        """
        result = run_query(query, {"username": username, "role": role})
        return result.single()

    @staticmethod
    def follow(username, follow_username):
        query = """
        MATCH (u1:User {username: $username}), (u2:User {username: $follow_username})
        CREATE (u1)-[:FOLLOWS]->(u2)
        RETURN u1, u2
        """
        run_query(query, {"username": username, "follow_username": follow_username})

    @staticmethod
    def get_posts(username):
        query = """
        MATCH (u:User {username: $username})-[:POSTED]->(p:Post)
        RETURN p
        """
        result = run_query(query, {"username": username})
        return [record["p"] for record in result]

    @staticmethod
    def create_post(username, content, created_at):
        query = """
        MATCH (u:User {username: $username})
        CREATE (p:Post {content: $content, created_at: $created_at})
        CREATE (u)-[:POSTED]->(p)
        RETURN p
        """
        result = run_query(query, {"username": username, "content": content, "created_at": created_at})
        return result.single()

# Post model
class Post:
    @staticmethod
    def relate_posts(content1, content2):
        query = """
        MATCH (p1:Post {content: $content1}), (p2:Post {content: $content2})
        CREATE (p1)-[:RELATED_TO]->(p2)
        RETURN p1, p2
        """
        run_query(query, {"content1": content1, "content2": content2})

# Flask Routes
@app.route('/user', methods=['POST'])
def create_user():
    username = request.json.get('username')
    role = request.json.get('role')
    user = User.create(username, role)
    return jsonify({"message": f"User {user['u']['username']} created successfully!"})

@app.route('/user/follow', methods=['POST'])
def follow_user():
    username = request.json.get('username')
    follow_username = request.json.get('follow_username')
    User.follow(username, follow_username)
    return jsonify({"message": f"{username} now follows {follow_username}!"})

@app.route('/user/posts', methods=['GET'])
def get_user_posts():
    username = request.args.get('username')
    posts = User.get_posts(username)
    return jsonify({"posts": posts})

@app.route('/post', methods=['POST'])
def create_post():
    username = request.json.get('username')
    content = request.json.get('content')
    created_at = request.json.get('created_at')
    post = User.create_post(username, content, created_at)
    return jsonify({"message": "Post created successfully!", "post": post["p"]})

@app.route('/post/relate', methods=['POST'])
def relate_posts():
    content1 = request.json.get('content1')
    content2 = request.json.get('content2')
    Post.relate_posts(content1, content2)
    return jsonify({"message": f"Posts '{content1}' and '{content2}' are now related!"})

if __name__ == '__main__':
    app.run(debug=True)