#!/usr/bin/env python3
"""
🚀 OpenGenNet AI - Simplified Vercel Deployment
Python 3.13 Compatible Version - Fixed for Vercel
"""

import os
import json
from datetime import datetime
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# CORS headers manually added to avoid flask-cors dependency
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# API Keys from environment
GROQ_FAST_KEY = os.getenv('GROQ_FAST_KEY', '')
GROQ_CODING_KEY = os.getenv('GROQ_CODING_KEY', '')
DEEPSEEK_KEY = os.getenv('DEEPSEEK_KEY', '')
QWEN_KEY = os.getenv('QWEN_KEY', '')
PORT = int(os.getenv('PORT', 8080))

# Simplified expert knowledge base
EXPERT_KNOWLEDGE = {
    "networking": [
        "TCP/IP protocol suite fundamentals",
        "OSI model layers explanation",
        "Subnetting and IP addressing",
        "Routing protocols (OSPF, BGP, EIGRP)",
        "Network security best practices",
        "VPN technologies and implementation",
        "Network troubleshooting methodologies"
    ],
    "cybersecurity": [
        "Firewall configuration and management",
        "Intrusion detection and prevention systems",
        "Encryption standards and protocols",
        "Access control and authentication",
        "Security auditing and compliance",
        "Threat analysis and mitigation",
        "Zero-trust security model"
    ],
    "cloud_computing": [
        "Cloud service models (IaaS, PaaS, SaaS)",
        "Infrastructure as Code (IaC) principles",
        "Containerization with Docker and Kubernetes",
        "Serverless computing architectures",
        "Cloud security best practices",
        "Multi-cloud deployment strategies",
        "Cost optimization techniques"
    ]
}

def call_ai_api(message, provider="groq"):
    """Unified AI API caller"""
    try:
        if provider == "groq" and GROQ_FAST_KEY:
            headers = {
                "Authorization": f"Bearer {GROQ_FAST_KEY}",
                "Content-Type": "application/json"
            }
            # Use working Groq model
            data = {
                "model": "llama-3.1-8b-instant",  # Working model
                "messages": [{"role": "user", "content": message}],
                "temperature": 0.7,
                "max_tokens": 1024
            }
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                return f"Groq API error: {response.status_code} - {response.text}"
                
        elif provider == "deepseek" and DEEPSEEK_KEY:
            headers = {
                "Authorization": f"Bearer {DEEPSEEK_KEY}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "deepseek/deepseek-r1",  # Updated to working model
                "messages": [{"role": "user", "content": message}],
                "temperature": 0.7,
                "max_tokens": 1024
            }
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",  # Updated to OpenRouter
                headers=headers,
                json=data,
                timeout=30
            )
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                return f"DeepSeek API error: {response.status_code}"
                
        elif provider == "qwen" and QWEN_KEY:
            # Try OpenRouter endpoint for Qwen
            headers = {
                "Authorization": f"Bearer {QWEN_KEY}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "qwen/qwen-2.5-72b-instruct",  # Updated to working model
                "messages": [{"role": "user", "content": message}],
                "temperature": 0.7,
                "max_tokens": 1024
            }
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                return f"Qwen API error: {response.status_code} - {response.text}"
        else:
            return f"No API key available for {provider}"
            
    except Exception as e:
        return f"Error calling {provider}: {str(e)}"

def search_expert_knowledge(query):
    """Search expert knowledge base"""
    query_lower = query.lower()
    results = []
    
    for category, topics in EXPERT_KNOWLEDGE.items():
        for topic in topics:
            if query_lower in topic.lower():
                results.append({
                    "category": category,
                    "topic": topic,
                    "relevance": "high"
                })
    
    return results[:10]

@app.route('/debug')
def debug():
    """Debug endpoint to check environment"""
    return jsonify({
        "groq_key_present": bool(GROQ_FAST_KEY),
        "groq_key_length": len(GROQ_FAST_KEY) if GROQ_FAST_KEY else 0,
        "deepseek_key_present": bool(DEEPSEEK_KEY),
        "qwen_key_present": bool(QWEN_KEY),
        "environment": "vercel",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/health')
def health_check():
    """Health check endpoint with debug info"""
    providers_status = {
        "groq": bool(GROQ_FAST_KEY),
        "deepseek": bool(DEEPSEEK_KEY),
        "qwen": bool(QWEN_KEY)
    }
    
    # Debug environment variables (no sensitive data)
    env_debug = {
        'GROQ_FAST_KEY': 'present' if GROQ_FAST_KEY else 'missing',
        'GROQ_CODING_KEY': 'present' if GROQ_CODING_KEY else 'missing', 
        'DEEPSEEK_KEY': 'present' if DEEPSEEK_KEY else 'missing',
        'QWEN_KEY': 'present' if QWEN_KEY else 'missing'
    }

    return jsonify({
        "service": "OpenGenNet Expert AI Backend",
        "status": "healthy",
        "version": "1.2.0",
        "timestamp": datetime.now().isoformat(),
        "providers": sum(providers_status.values()),
        "expert_rag": "simplified",
        "platform": "vercel",
        "python_version": "3.13.5",
        "env_debug": env_debug,
        "groq_key_present": bool(GROQ_FAST_KEY)
    })

@app.route('/status', methods=['GET'])
def get_status():
    """Get system status"""
    providers_status = {
        "groq": bool(GROQ_FAST_KEY),
        "deepseek": bool(DEEPSEEK_KEY),
        "qwen": bool(QWEN_KEY)
    }

    return jsonify({
        "service": "OpenGenNet Expert AI Backend",
        "status": "operational",
        "timestamp": datetime.now().isoformat(),
        "providers": providers_status,
        "expert_knowledge_categories": list(EXPERT_KNOWLEDGE.keys()),
        "total_expert_cases": sum(len(topics) for topics in EXPERT_KNOWLEDGE.values())
    })

@app.route('/ask', methods=['POST'])
def ask_ai():
    """AI chat endpoint with provider fallback"""
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"error": "Missing message parameter"}), 400
        
        message = data['message']
        use_expert_context = data.get('use_expert_context', True)
        
        # Enhance message with expert context if requested
        enhanced_message = message
        if use_expert_context:
            # Search for relevant expert knowledge
            expert_results = search_expert_knowledge(message)
            if expert_results:
                expert_context = "\\n\\nRelevant expert knowledge:\\n"
                for result in expert_results[:3]:  # Use top 3 results
                    expert_context += f"- {result['topic']} ({result['category']})\\n"
                enhanced_message = f"{message}{expert_context}\\nPlease provide a comprehensive answer incorporating this expert knowledge."
        
        # Check if any providers are available
        if not any([GROQ_FAST_KEY, DEEPSEEK_KEY, QWEN_KEY]):
            return jsonify({
                "response": "No AI providers available. Please check API keys.",
                "provider": "none",
                "timestamp": datetime.now().isoformat()
            })
        
        # Try providers in order: groq -> deepseek -> qwen
        providers = ["groq", "deepseek", "qwen"]
        
        for provider in providers:
            if (provider == "groq" and GROQ_FAST_KEY) or \
               (provider == "deepseek" and DEEPSEEK_KEY) or \
               (provider == "qwen" and QWEN_KEY):
                
                response = call_ai_api(enhanced_message, provider)
                
                # Check if response is an error message
                if not any(error_keyword in response.lower() for error_keyword in 
                          ["error", "exception", "no api key", "technical difficulties"]):
                    return jsonify({
                        "response": response,
                        "provider": provider,
                        "enhanced_with_expert_context": use_expert_context and len(expert_results) > 0,
                        "expert_cases_used": len(expert_results) if use_expert_context else 0,
                        "timestamp": datetime.now().isoformat()
                    })
        
        # If all providers fail, return a fallback response
        fallback_response = f"I understand you're asking about: '{message}'. I'm currently experiencing connectivity issues with AI providers, but I can help you find relevant expert knowledge. Try the /search endpoint with your query."
        
        return jsonify({
            "response": fallback_response,
            "provider": "fallback",
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@app.route('/search', methods=['POST'])
def search_knowledge():
    """Expert knowledge search endpoint"""
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({"error": "Missing query parameter"}), 400
        
        query = data['query']
        results = search_expert_knowledge(query)
        
        return jsonify({
            "query": query,
            "results": results,
            "total_results": len(results),
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@app.route('/')
def root():
    """Root endpoint - Enhanced API Ready"""
    return jsonify({
        "service": "OpenGenNet Expert AI Backend",
        "status": "running",
        "version": "1.1.2",
        "enhancement": "environment_variables_ready",
        "endpoints": ["/health", "/status", "/ask", "/search", "/debug"],
        "timestamp": datetime.now().isoformat()
    })

# Handle preflight OPTIONS requests
@app.route('/ask', methods=['OPTIONS'])
@app.route('/search', methods=['OPTIONS'])
def handle_options():
    """Handle CORS preflight requests"""
    return '', 200

# For local development
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True)
