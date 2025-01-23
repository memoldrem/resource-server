from flask import Flask, jsonify, render_template
from middleware.token_required import token_required # Import the token_required decorator

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/protected')
@token_required
def protected_route():
    return jsonify({"message": "Access granted!"})

if __name__ == '__main__':
    app.run(debug=True)
