#!/usr/bin/env python3
"""
🧪 COMPLEX CODING QUESTIONS TEST - API Accuracy Assessment
Testing OpenGenNet AI with 10 challenging coding scenarios
"""

import requests
import json
import time
from datetime import datetime

class CodingAccuracyTester:
    def __init__(self):
        self.base_url = "https://opengennet-ai.vercel.app"
        self.test_results = []
        
    def test_coding_question(self, question, expected_topics, difficulty):
        """Test a single coding question"""
        print(f"\n{'='*80}")
        print(f"🧪 TESTING: {question[:60]}...")
        print(f"🎯 Difficulty: {difficulty}")
        print(f"📚 Expected Topics: {', '.join(expected_topics)}")
        print(f"{'='*80}")
        
        try:
            # Test AI Chat Response
            chat_data = {
                "message": question,
                "use_expert_context": True
            }
            
            start_time = time.time()
            response = requests.post(f"{self.base_url}/ask", json=chat_data, timeout=30)
            response_time = round((time.time() - start_time) * 1000, 2)
            
            if response.status_code == 200:
                data = response.json()
                ai_response = data.get('response', '')
                provider = data.get('provider', 'none')
                
                print(f"✅ API Response: {response.status_code}")
                print(f"⚡ Response Time: {response_time}ms")
                print(f"🤖 Provider: {provider}")
                print(f"💬 Response Length: {len(ai_response)} characters")
                print(f"📝 Response: {ai_response}")
                
                # Test Expert Knowledge Search for related topics
                print(f"\n🔍 EXPERT KNOWLEDGE SEARCH:")
                for topic in expected_topics:
                    search_data = {"query": topic}
                    search_response = requests.post(f"{self.base_url}/search", 
                                                  json=search_data, timeout=10)
                    if search_response.status_code == 200:
                        search_results = search_response.json()
                        total_results = search_results.get('total_results', 0)
                        print(f"   📚 '{topic}': {total_results} expert cases found")
                        
                        if total_results > 0:
                            for result in search_results.get('results', [])[:2]:
                                print(f"      - {result.get('topic', 'N/A')}")
                
                # Analyze response quality
                quality_score = self.analyze_response_quality(ai_response, expected_topics)
                
                result = {
                    "question": question,
                    "difficulty": difficulty,
                    "expected_topics": expected_topics,
                    "ai_response": ai_response,
                    "provider": provider,
                    "response_time": response_time,
                    "quality_score": quality_score,
                    "status": "success"
                }
                
            else:
                print(f"❌ API Error: {response.status_code}")
                result = {
                    "question": question,
                    "difficulty": difficulty,
                    "status": "api_error",
                    "error": response.status_code
                }
        
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
            result = {
                "question": question,
                "difficulty": difficulty,
                "status": "exception",
                "error": str(e)
            }
        
        self.test_results.append(result)
        time.sleep(2)  # Delay between requests
        
    def analyze_response_quality(self, response, expected_topics):
        """Analyze the quality of AI response"""
        if "No AI providers available" in response:
            return {"score": 0, "reason": "No AI providers configured"}
        
        # Basic quality indicators
        indicators = {
            "length": len(response) > 50,
            "technical": any(word in response.lower() for word in 
                           ['function', 'algorithm', 'code', 'programming', 'syntax']),
            "structured": any(word in response for word in ['\n', '1.', '2.', '-']),
            "relevant": any(topic.lower() in response.lower() for topic in expected_topics)
        }
        
        score = sum(indicators.values()) / len(indicators) * 100
        
        return {
            "score": round(score, 1),
            "indicators": indicators,
            "response_length": len(response)
        }
    
    def run_complex_coding_tests(self):
        """Run 10 complex coding questions"""
        
        print("🧪 COMPLEX CODING QUESTIONS - ACCURACY TEST")
        print("=" * 80)
        print(f"🕒 Test Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🌐 Testing API: {self.base_url}")
        
        # 10 Complex Coding Questions
        coding_questions = [
            {
                "question": "How do you implement a distributed rate limiter using Redis for a microservices architecture? Include sliding window algorithm and fault tolerance.",
                "expected_topics": ["redis", "microservices", "algorithm", "distributed"],
                "difficulty": "Expert"
            },
            {
                "question": "Explain how to implement a custom memory allocator in C++ with garbage collection and memory pool optimization for real-time systems.",
                "expected_topics": ["memory", "cpp", "optimization", "realtime"],
                "difficulty": "Expert"
            },
            {
                "question": "Design a fault-tolerant distributed consensus algorithm similar to Raft but optimized for Byzantine failures in blockchain networks.",
                "expected_topics": ["consensus", "blockchain", "distributed", "algorithm"],
                "difficulty": "Expert"
            },
            {
                "question": "How would you implement zero-downtime database schema migrations for a high-traffic application with millions of records?",
                "expected_topics": ["database", "migration", "scalability", "performance"],
                "difficulty": "Advanced"
            },
            {
                "question": "Create a machine learning pipeline that can handle real-time feature engineering and model serving with sub-millisecond latency.",
                "expected_topics": ["machine learning", "pipeline", "realtime", "performance"],
                "difficulty": "Expert"
            },
            {
                "question": "Implement a custom HTTP/2 server from scratch with multiplexing, flow control, and header compression (HPACK).",
                "expected_topics": ["http", "networking", "protocol", "compression"],
                "difficulty": "Expert"
            },
            {
                "question": "Design a lock-free concurrent data structure for a high-performance trading system that handles millions of transactions per second.",
                "expected_topics": ["concurrency", "trading", "performance", "data structure"],
                "difficulty": "Expert"
            },
            {
                "question": "How do you implement end-to-end encryption for a chat application with perfect forward secrecy and post-quantum cryptography?",
                "expected_topics": ["encryption", "cryptography", "security", "protocol"],
                "difficulty": "Advanced"
            },
            {
                "question": "Build a custom container runtime similar to Docker but optimized for serverless functions with sub-second cold start times.",
                "expected_topics": ["containers", "serverless", "runtime", "optimization"],
                "difficulty": "Expert"
            },
            {
                "question": "Implement a distributed graph database query optimizer that can handle complex traversals across petabyte-scale datasets.",
                "expected_topics": ["graph database", "optimizer", "distributed", "scalability"],
                "difficulty": "Expert"
            }
        ]
        
        # Run all tests
        for i, test in enumerate(coding_questions, 1):
            print(f"\n🔬 TEST {i}/10")
            self.test_coding_question(
                test["question"],
                test["expected_topics"],
                test["difficulty"]
            )
        
        # Generate comprehensive report
        self.generate_accuracy_report()
    
    def generate_accuracy_report(self):
        """Generate detailed accuracy and performance report"""
        print("\n" + "=" * 80)
        print("📊 COMPLEX CODING QUESTIONS - ACCURACY REPORT")
        print("=" * 80)
        
        # Calculate statistics
        successful_tests = [r for r in self.test_results if r.get("status") == "success"]
        total_tests = len(self.test_results)
        success_rate = (len(successful_tests) / total_tests) * 100 if total_tests > 0 else 0
        
        print(f"📈 Overall Success Rate: {success_rate:.1f}% ({len(successful_tests)}/{total_tests})")
        
        if successful_tests:
            # Calculate average response time
            avg_response_time = sum(r.get("response_time", 0) for r in successful_tests) / len(successful_tests)
            print(f"⚡ Average Response Time: {avg_response_time:.1f}ms")
            
            # Calculate quality scores
            quality_scores = [r.get("quality_score", {}).get("score", 0) for r in successful_tests]
            avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0
            print(f"🎯 Average Quality Score: {avg_quality:.1f}/100")
            
            # Provider distribution
            providers = [r.get("provider", "unknown") for r in successful_tests]
            provider_counts = {p: providers.count(p) for p in set(providers)}
            print(f"🤖 Provider Distribution: {provider_counts}")
        
        print(f"\n📋 DETAILED TEST RESULTS:")
        print("-" * 80)
        
        for i, result in enumerate(self.test_results, 1):
            status_icon = "✅" if result.get("status") == "success" else "❌"
            difficulty = result.get("difficulty", "Unknown")
            
            print(f"{status_icon} Test {i}: {result['question'][:50]}...")
            print(f"   🎯 Difficulty: {difficulty}")
            
            if result.get("status") == "success":
                quality = result.get("quality_score", {})
                response_time = result.get("response_time", 0)
                provider = result.get("provider", "unknown")
                
                print(f"   ⚡ Response Time: {response_time}ms")
                print(f"   🤖 Provider: {provider}")
                print(f"   📊 Quality Score: {quality.get('score', 0)}/100")
                
                # Show response preview
                response = result.get("ai_response", "")
                preview = response[:100] + "..." if len(response) > 100 else response
                print(f"   💬 Response: {preview}")
                
            else:
                error = result.get("error", "Unknown error")
                print(f"   ❌ Error: {error}")
            
            print()
        
        # Generate recommendations
        print("🚀 RECOMMENDATIONS:")
        print("-" * 80)
        
        if success_rate >= 80:
            print("✅ EXCELLENT: API handles complex coding questions well")
            print("✅ Ready for advanced technical chatbot frontend")
            print("✅ Expert knowledge integration is effective")
        elif success_rate >= 60:
            print("🟡 GOOD: API shows solid performance with room for improvement")
            print("🔧 Consider optimizing response times and quality")
        else:
            print("🔴 NEEDS IMPROVEMENT: Low success rate on complex questions")
            print("🔧 Check API configuration and expert knowledge integration")
        
        # API Key Status Check
        if any("No AI providers available" in str(r.get("ai_response", "")) for r in successful_tests):
            print("\n⚠️  IMPORTANT: AI Providers Need API Keys")
            print("🔑 Add GROQ, DEEPSEEK, or QWEN API keys to Vercel for full AI functionality")
            print("📋 Current status: Expert knowledge search works, AI chat needs keys")
        
        print(f"\n🕒 Test Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    tester = CodingAccuracyTester()
    tester.run_complex_coding_tests()
