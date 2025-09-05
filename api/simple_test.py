from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "OpenGenNet 2.0 - Vercel Test",
        "status": "working",
        "environment_vars": {
            "GROQ_FAST_KEY": bool(os.getenv('GROQ_FAST_KEY')),
            "GROQ_CODING_KEY": bool(os.getenv('GROQ_CODING_KEY')),
            "DEEPSEEK_KEY": bool(os.getenv('DEEPSEEK_KEY')),
            "QWEN_KEY": bool(os.getenv('QWEN_KEY'))
        }
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "version": "OpenGenNet 2.0 Test",
        "platform": "Vercel"
    })

@app.route('/test', methods=['POST'])
def test_endpoint():
    data = request.get_json() or {}
    return jsonify({
        "received": data,
        "status": "success",
        "api_keys_available": {
            "groq": bool(os.getenv('GROQ_FAST_KEY')),
            "deepseek": bool(os.getenv('DEEPSEEK_KEY'))
        }
    })

# Vercel handler
def handler(request):
    return app
