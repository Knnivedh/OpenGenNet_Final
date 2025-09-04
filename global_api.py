#!/usr/bin/env python3
"""
🌐 OpenGenNet Expert AI - Global API for 24/7 Cloud Hosting
Production-ready API for integration with frontend builders like Lovable.ai, Bolt.new, etc.
"""

import os
import sys

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
import aiohttp
import json
import time
import uuid
from datetime import datetime
from typing import Dict, List, Optional

# Import Expert RAG System
try:
    from expert_rag_system import enhance_response, get_rag_system
    RAG_AVAILABLE = True
    print("🧠 Expert RAG System loaded successfully")
except ImportError:
    RAG_AVAILABLE = False
    print("⚠️ Expert RAG System not available")

# Initialize Flask app
app = Flask(__name__)
CORS(app, origins="*")  # Enable CORS for all origins

# Working API Providers - Use environment variables for production
WORKING_PROVIDERS = {
    "groq_fast": {
        "name": "Groq LLaMA 3.1 8B",
        "api_key": os.environ.get("GROQ_FAST_KEY", "your_groq_fast_key_here"),
        "base_url": "https://api.groq.com/openai/v1",
        "model": "llama-3.1-8b-instant",
        "specialty": "Fast general responses"
    },
    "groq_coding": {
        "name": "Groq Gemma2 9B", 
        "api_key": os.environ.get("GROQ_CODING_KEY", "your_groq_coding_key_here"),
        "base_url": "https://api.groq.com/openai/v1",
        "model": "gemma2-9b-it",
        "specialty": "Coding & technical tasks"
    },
    "deepseek_reasoning": {
        "name": "DeepSeek R1",
        "api_key": os.environ.get("DEEPSEEK_KEY", "your_deepseek_key_here"),
        "base_url": "https://openrouter.ai/api/v1", 
        "model": "deepseek/deepseek-r1",
        "specialty": "Complex reasoning"
    },
    "qwen_general": {
        "name": "Qwen 2.5 72B",
        "api_key": os.environ.get("QWEN_KEY", "your_qwen_key_here"),
        "base_url": "https://openrouter.ai/api/v1",
        "model": "qwen/qwen-2.5-72b-instruct", 
        "specialty": "Comprehensive knowledge"
    }
}

# Session storage
chat_sessions = {}

class ChatSession:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.created_at = datetime.now()
        self.messages = []
        self.last_activity = datetime.now()

def get_session(session_id: str = None) -> ChatSession:
    """Get or create chat session"""
    if session_id and session_id in chat_sessions:
        session = chat_sessions[session_id]
        session.last_activity = datetime.now()
        return session
    
    new_id = session_id or f"session_{int(time.time())}_{uuid.uuid4().hex[:8]}"
    session = ChatSession(new_id)
    chat_sessions[new_id] = session
    return session

def select_provider(message: str) -> str:
    """Intelligent provider selection"""
    message_lower = message.lower()
    
    # Coding/technical keywords
    coding_keywords = ['code', 'python', 'function', 'programming', 'script', 'debug', 'algorithm', 'implement', 'api', 'sql', 'javascript', 'html', 'css']
    if any(word in message_lower for word in coding_keywords):
        return "groq_coding"
    
    # Complex reasoning keywords  
    reasoning_keywords = ['analyze', 'compare', 'explain why', 'reasoning', 'complex', 'strategy', 'philosophy', 'pros and cons', 'evaluate']
    if any(word in message_lower for word in reasoning_keywords):
        return "deepseek_reasoning"
    
    # Long-form content
    if len(message) > 200 or any(word in message_lower for word in ['detailed', 'comprehensive', 'complete guide', 'tutorial', 'step by step']):
        return "qwen_general"
    
    # Default to fast provider
    return "groq_fast"

async def call_ai_provider(provider_key: str, messages: List[Dict], max_tokens: int = 1000) -> Dict:
    """Call selected AI provider"""
    provider = WORKING_PROVIDERS[provider_key]
    
    headers = {
        "Authorization": f"Bearer {provider['api_key']}",
        "Content-Type": "application/json"
    }
    
    # OpenRouter specific headers
    if "openrouter" in provider['base_url']:
        headers.update({
            "HTTP-Referer": "https://opengennet.ai",
            "X-Title": "OpenGenNet AI API"
        })
    
    payload = {
        "model": provider['model'],
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": 0.7
    }
    
    start_time = time.time()
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                f"{provider['base_url']}/chat/completions",
                json=payload,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                
                response_time = time.time() - start_time
                
                if response.status == 200:
                    data = await response.json()
                    content = data['choices'][0]['message']['content']
                    
                    return {
                        "success": True,
                        "response": content,
                        "provider": provider['name'],
                        "model": provider['model'],
                        "response_time": response_time
                    }
                else:
                    error_text = await response.text()
                    return {
                        "success": False,
                        "error": f"API Error {response.status}: {error_text}",
                        "provider": provider['name']
                    }
                    
        except Exception as e:
            return {
                "success": False,
                "error": f"Connection error: {str(e)}",
                "provider": provider['name']
            }

def process_message_sync(message: str, session_id: str = None, max_tokens: int = 1000) -> Dict:
    """Synchronous wrapper for async AI processing with Expert RAG enhancement"""
    
    # Get or create session
    session = get_session(session_id)
    session.messages.append({"role": "user", "content": message})
    
    # Build conversation context
    messages = []
    
    # Enhanced system prompt for expert capabilities
    system_prompt = """You are OpenGenNet AI, an elite enterprise-grade AI assistant with TOP 1% expertise in:

• Advanced Networking & Infrastructure (BGP, OSPF, SD-WAN, network automation, enterprise routing/switching)
• Cybersecurity Excellence (threat hunting, incident response, security architecture, compliance frameworks)
• Cloud Computing Mastery (AWS/Azure/GCP expert configurations, containerization, infrastructure as code)
• Software Development (Python/JavaScript excellence, API design, microservices, DevOps practices)
• Enterprise IT Leadership (system design, performance optimization, disaster recovery, scalability)

Provide expert-level responses with:
- Technical accuracy and industry best practices
- Real-world implementation guidance
- Security considerations and compliance requirements
- Performance optimization recommendations
- Actionable next steps and troubleshooting approaches

Your responses should reflect the knowledge and experience of a senior technical consultant."""
    
    messages.append({"role": "system", "content": system_prompt})
    
    # Add recent conversation history (last 8 messages)
    recent_messages = session.messages[-8:] if len(session.messages) > 8 else session.messages
    for msg in recent_messages:
        messages.append({"role": msg["role"], "content": msg["content"]})
    
    # Select best provider
    selected_provider = select_provider(message)
    
    # Call AI provider (run async in sync context)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        result = loop.run_until_complete(
            call_ai_provider(selected_provider, messages, max_tokens)
        )
    finally:
        loop.close()
    
    if result["success"]:
        basic_response = result["response"]
        provider_name = result["provider"]
        response_time = result["response_time"]
        
        # 🧠 EXPERT RAG ENHANCEMENT
        if RAG_AVAILABLE:
            try:
                print(f"🚀 Enhancing response with Expert RAG system...")
                enhancement = enhance_response(message, basic_response, provider_name)
                
                if enhancement['expert_enhancement']:
                    # Use enhanced response
                    final_response = enhancement['enhanced_response']
                    
                    # Add to session
                    session.messages.append({"role": "assistant", "content": final_response})
                    
                    return {
                        "success": True,
                        "response": final_response,
                        "model_used": f"{provider_name} + Expert RAG",
                        "response_time": response_time,
                        "session_id": session.session_id,
                        "message_count": len(session.messages),
                        "expert_enhancement": True,
                        "expert_sources": enhancement['expert_sources'],
                        "confidence_boost": enhancement['confidence_boost'],
                        "enhancement_summary": enhancement['enhancement_summary']
                    }
                else:
                    print("ℹ️ No relevant expert knowledge found, using basic response")
                    
            except Exception as e:
                print(f"⚠️ RAG enhancement failed: {e}")
                # Fall back to basic response
        
        # Add basic response to session
        session.messages.append({"role": "assistant", "content": basic_response})
        
        return {
            "success": True,
            "response": basic_response,
            "model_used": provider_name,
            "response_time": response_time,
            "session_id": session.session_id,
            "message_count": len(session.messages),
            "expert_enhancement": False
        }
    else:
        return {
            "success": False,
            "error": result["error"],
            "session_id": session.session_id
        }

# 🌐 API ENDPOINTS FOR FRONTEND BUILDERS

@app.route("/", methods=["GET"])
def home():
    """API documentation and service info"""
    return jsonify({
        "service": "OpenGenNet Expert AI API",
        "version": "1.0.0",
        "description": "Global API for TOP 1% cybersecurity and networking expertise",
        "expert_rag_available": RAG_AVAILABLE,
        "endpoints": {
            "GET /": "Service information",
            "GET /health": "Health check",
            "POST /ask": "Simple chat endpoint for frontend builders",
            "POST /chat": "Alternative chat endpoint",
            "POST /search": "Expert knowledge search",
            "GET /models": "Available models",
            "GET /status": "System status"
        },
        "integration": {
            "frontend_builder": "Lovable.ai, Bolt.new, Durable, etc.",
            "endpoint": "/ask",
            "method": "POST",
            "request_body": {"query": "userMessage"},
            "response_path": "response"
        },
        "documentation": "https://docs.opengennet.ai",
        "support": "https://github.com/opengennet/api"
    })

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint - critical for deployment platforms"""
    return jsonify({
        "status": "healthy",
        "service": "OpenGenNet Expert AI Backend",
        "version": "1.0.0",
        "expert_rag": "available" if RAG_AVAILABLE else "unavailable",
        "providers": len(WORKING_PROVIDERS),
        "timestamp": datetime.now().isoformat()
    })

@app.route("/ask", methods=["POST"])  
def ask():
    """
    Main AI chat endpoint - optimized for frontend builders like Lovable.ai
    Accepts: { "query": "user question" }
    Returns: { "response": "AI answer" }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "JSON body required"}), 400
        
        query = data.get("query", "").strip()
        if not query:
            return jsonify({"error": "Query parameter required"}), 400
        
        session_id = data.get("session_id", None)
        max_tokens = data.get("max_tokens", 1000)
        
        # Process message
        result = process_message_sync(query, session_id, max_tokens)
        
        if result["success"]:
            response_data = {
                "response": result["response"],
                "session_id": result["session_id"],
                "model_used": result["model_used"],
                "response_time": result["response_time"],
                "timestamp": datetime.now().isoformat()
            }
            
            # Add expert enhancement details if available
            if result.get("expert_enhancement"):
                response_data.update({
                    "expert_enhancement": True,
                    "expert_sources": result["expert_sources"],
                    "confidence_boost": result["confidence_boost"]
                })
            
            return jsonify(response_data)
        else:
            return jsonify({
                "error": result["error"],
                "session_id": result.get("session_id", "unknown")
            }), 500
            
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/chat", methods=["POST"])
def chat():
    """Alternative chat endpoint (compatibility)"""
    try:
        data = request.get_json()
        
        message = data.get("message", "").strip()
        if not message:
            return jsonify({"error": "Message required"}), 400
        
        session_id = data.get("session_id", None)
        max_tokens = data.get("max_tokens", 1000)
        
        result = process_message_sync(message, session_id, max_tokens)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/search", methods=["POST"])
def search():
    """Expert knowledge search endpoint"""
    try:
        data = request.get_json()
        query = data.get("query", "").strip()
        
        if not query:
            return jsonify({"error": "Query required"}), 400
        
        # Direct expert knowledge search if RAG is available
        if RAG_AVAILABLE:
            try:
                rag_system = get_rag_system()
                expert_results = rag_system.search_expert_knowledge(query, top_k=5)
                
                if expert_results:
                    return jsonify({
                        "query": query,
                        "results": [
                            {
                                "title": result["title"],
                                "content": result["content"][:500] + "..." if len(result["content"]) > 500 else result["content"],
                                "category": result["category"],
                                "technology": result["technology"],
                                "relevance_score": result["relevance_score"],
                                "quality_score": result["quality_score"],
                                "source": "Expert Knowledge Base"
                            }
                            for result in expert_results
                        ],
                        "total_found": len(expert_results),
                        "search_type": "expert_knowledge"
                    })
            except Exception as e:
                print(f"⚠️ Expert search failed: {e}")
        
        # Fallback to AI response
        result = process_message_sync(f"Search knowledge about: {query}")
        
        if result["success"]:
            return jsonify({
                "query": query,
                "results": [{
                    "title": "AI Knowledge Response",
                    "content": result["response"],
                    "source": result["model_used"],
                    "relevance": 0.95
                }],
                "search_type": "ai_generated"
            })
        else:
            return jsonify({"error": result["error"]}), 500
            
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/models", methods=["GET"])
def models():
    """List available models"""
    model_list = []
    for key, provider in WORKING_PROVIDERS.items():
        model_list.append({
            "id": key,
            "object": "model",
            "created": int(time.time()),
            "owned_by": "opengennet",
            "name": provider["name"],
            "model": provider["model"],
            "specialty": provider["specialty"]
        })
    
    return jsonify({
        "object": "list",
        "data": model_list
    })

@app.route("/status", methods=["GET"])
def status():
    """System status for monitoring"""
    expert_status = "available" if RAG_AVAILABLE else "unavailable"
    
    capabilities = [
        "Multi-model AI routing",
        "Session management", 
        "Conversation memory",
        "Real-time responses",
        "Expert knowledge enhancement"
    ]
    
    if RAG_AVAILABLE:
        capabilities.extend([
            "Expert knowledge enhancement",
            "Semantic search",
            "TOP 1% cybersecurity expertise",
            "Advanced networking knowledge"
        ])
    
    return jsonify({
        "status": "operational",
        "expert_rag_system": expert_status,
        "active_sessions": len(chat_sessions),
        "providers": {
            name: {
                "model": config["model"],
                "specialty": config["specialty"], 
                "status": "active"
            }
            for name, config in WORKING_PROVIDERS.items()
        },
        "capabilities": capabilities,
        "uptime": datetime.now().isoformat()
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": {"message": "Endpoint not found", "type": "not_found"}}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": {"message": "Internal server error", "type": "internal_error"}}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    
    print("🌐 Starting OpenGenNet Expert AI - Global API")
    print("=" * 60)
    print(f"🧠 Expert RAG System: {'Available' if RAG_AVAILABLE else 'Unavailable'}")
    print(f"🌍 Global API Server: http://0.0.0.0:{port}")
    print(f"📊 Health Check: http://localhost:{port}/health")
    print(f"💬 Simple Chat: http://localhost:{port}/ask")
    print(f"🔍 Knowledge Search: http://localhost:{port}/search")
    print("🚀 Ready for global deployment and frontend integration!")
    print("=" * 60)
    
    app.run(host="0.0.0.0", port=port, debug=False)