from flask import Flask, request, jsonify

app = Flask(__name__)   

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"}), 200


@app.route('/', methods=['GET'])       
def home():
    return "Welcome to the MarketPulse API!"