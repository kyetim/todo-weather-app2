from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify({
        'message': 'Hello from Vercel!',
        'status': 'working'
    })

@app.route('/test')
def test():
    return jsonify({
        'message': 'Test endpoint working',
        'timestamp': '2025-10-20'
    })

# Vercel handler
handler = app