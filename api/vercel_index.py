from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import random
import logging
import time
import os
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Environment variables for API keys
GROQ_FAST_KEY = os.getenv('GROQ_FAST_KEY', '')
GROQ_CODING_KEY = os.getenv('GROQ_CODING_KEY', '')
DEEPSEEK_KEY = os.getenv('DEEPSEEK_KEY', '')
QWEN_KEY = os.getenv('QWEN_KEY', '')

# Simplified Expert Knowledge Base (just a few examples for Vercel)
EXPERT_KNOWLEDGE = [
    {
        "id": 1,
        "category": "networking",
        "topic": "TCP/IP Basics",
        "question": "How does TCP/IP work?",
        "expert_answer": "TCP/IP is a suite of protocols that enables communication between devices on a network. TCP handles reliable data transmission while IP handles addressing and routing.",
        "technical_details": "TCP provides connection-oriented, reliable transmission with error checking and flow control. IP provides logical addressing with IPv4 (32-bit) or IPv6 (128-bit) addresses.",
        "best_practices": "Use proper subnetting, implement security policies, monitor network performance, and plan for scalability."
    },
    {
        "id": 2,
        "category": "cybersecurity",
        "topic": "Network Security",
        "question": "How to secure network infrastructure?",
        "expert_answer": "Implement defense in depth with firewalls, intrusion detection, access controls, encryption, and regular security audits.",
        "technical_details": "Use next-generation firewalls (NGFW), implement network segmentation, deploy SIEM solutions, and maintain security policies.",
        "best_practices": "Regular security assessments, staff training, incident response procedures, and compliance with security frameworks."
    },
    {
        "id": 3,
        "category": "cloud_computing",
        "topic": "Cloud Architecture",
        "question": "How to design scalable cloud systems?",
        "expert_answer": "Use microservices architecture, implement auto-scaling, leverage managed services, and design for fault tolerance.",
        "technical_details": "Implement containerization with Docker/Kubernetes, use cloud-native databases, implement CI/CD pipelines, and monitoring.",
        "best_practices": "Cost optimization, security by design, disaster recovery planning, and performance monitoring."
    }
]

# AI Provider configurations
AI_PROVIDERS = {
    "groq_fast": {
        "name": "GROQ Fast",
        "model": "llama-3.1-8b-instant",
        "api_key_env": "GROQ_FAST_KEY",
        "endpoint": "https://api.groq.com/openai/v1/chat/completions"
    },
    "groq_coding": {
        "name": "GROQ Coding",
        "model": "gemma2-9b-it",
        "api_key_env": "GROQ_CODING_KEY",
        "endpoint": "https://api.groq.com/openai/v1/chat/completions"
    },
    "deepseek": {
        "name": "DeepSeek R1",
        "model": "deepseek/deepseek-r1-distill-llama-70b",
        "api_key_env": "DEEPSEEK_KEY",
        "endpoint": "https://openrouter.ai/api/v1/chat/completions"
    },
    "qwen": {
        "name": "Qwen 2.5 72B",
        "model": "qwen/qwen-2.5-72b-instruct",
        "api_key_env": "QWEN_KEY",
        "endpoint": "https://openrouter.ai/api/v1/chat/completions"
    }
}

def get_api_key(provider_config):
    """Get API key from environment variables"""
    return os.getenv(provider_config["api_key_env"])

def search_expert_knowledge(query: str, category: Optional[str] = None) -> List[Dict]:
    """Search expert knowledge base"""
    query_lower = query.lower()
    results = []
    
    for item in EXPERT_KNOWLEDGE:
        if category and item["category"] != category:
            continue
            
        searchable_text = f"{item['topic']} {item['question']} {item['expert_answer']}".lower()
        
        if any(word in searchable_text for word in query_lower.split()):
            results.append(item)
    
    return results

def call_ai_provider(provider_key: str, message: str, context: str = None) -> Dict:
    """Call specific AI provider"""
    provider = AI_PROVIDERS.get(provider_key)
    if not provider:
        return {"error": f"Provider {provider_key} not found"}
    
    api_key = get_api_key(provider)
    if not api_key:
        return {"error": f"API key not found for {provider['name']}"}
    
    system_message = "You are OpenGenNet 2.0, an advanced AI assistant with deep technical expertise."
    if context:
        system_message += f"\n\nRelevant Knowledge Context:\n{context}"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": provider["model"],
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": message}
        ],
        "max_tokens": 2000,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(provider["endpoint"], headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        if 'choices' in result and len(result['choices']) > 0:
            return {
                "provider": provider["name"],
                "model": provider["model"],
                "response": result['choices'][0]['message']['content'],
                "status": "success"
            }
        else:
            return {"error": f"Invalid response format from {provider['name']}"}
            
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed for {provider['name']}: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error with {provider['name']}: {str(e)}"}

@app.route('/', methods=['GET'])
def home():
    """Home endpoint"""
    return jsonify({
        "message": "Welcome to OpenGenNet 2.0 API",
        "version": "2.0.0",
        "status": "operational",
        "environment": "vercel",
        "endpoints": ["/", "/health", "/ask", "/search", "/status"]
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "version": "OpenGenNet 2.0",
        "platform": "Vercel",
        "timestamp": time.time(),
        "providers": len(AI_PROVIDERS),
        "knowledge_base": len(EXPERT_KNOWLEDGE),
        "environment_vars": {
            "GROQ_FAST_KEY": bool(GROQ_FAST_KEY),
            "GROQ_CODING_KEY": bool(GROQ_CODING_KEY),
            "DEEPSEEK_KEY": bool(DEEPSEEK_KEY),
            "QWEN_KEY": bool(QWEN_KEY)
        }
    })

@app.route('/ask', methods=['POST'])
def ask_ai():
    """Main AI chat endpoint"""
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"error": "Message is required"}), 400
        
        message = data['message']
        preferred_provider = data.get('provider', 'groq_fast')
        use_context = data.get('use_context', True)
        
        # Search for relevant context if enabled
        context = None
        if use_context:
            knowledge_results = search_expert_knowledge(message)
            if knowledge_results:
                context_items = []
                for item in knowledge_results[:2]:
                    context_items.append(f"Topic: {item['topic']}\nAnswer: {item['expert_answer']}")
                context = "\n\n".join(context_items)
        
        # Try preferred provider first
        result = call_ai_provider(preferred_provider, message, context)
        
        # If preferred provider fails, try others
        if "error" in result:
            for provider_key in AI_PROVIDERS.keys():
                if provider_key != preferred_provider:
                    result = call_ai_provider(provider_key, message, context)
                    if "error" not in result:
                        result["fallback_used"] = True
                        break
        
        if "error" in result:
            return jsonify(result), 500
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/search', methods=['POST'])
def search_knowledge():
    """Search expert knowledge base"""
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({"error": "Query is required"}), 400
        
        query = data['query']
        category = data.get('category')
        
        results = search_expert_knowledge(query, category)
        
        return jsonify({
            "query": query,
            "category": category,
            "results": results,
            "count": len(results)
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/status', methods=['GET'])
def system_status():
    """Comprehensive system status"""
    try:
        provider_status = {}
        
        for key, provider in AI_PROVIDERS.items():
            api_key = get_api_key(provider)
            provider_status[key] = {
                "name": provider["name"],
                "model": provider["model"],
                "api_key_configured": bool(api_key),
                "endpoint": provider["endpoint"]
            }
        
        return jsonify({
            "system": "OpenGenNet 2.0",
            "version": "2.0.0",
            "platform": "Vercel",
            "status": "operational",
            "timestamp": time.time(),
            "providers": provider_status,
            "knowledge_base": {
                "total_items": len(EXPERT_KNOWLEDGE),
                "categories": ["networking", "cybersecurity", "cloud_computing"]
            }
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# For Vercel serverless functions
def handler(request):
    return app(request.environ, lambda status, headers: None)

# Also export the app directly for Vercel
if __name__ == '__main__':
    app.run(debug=True)
