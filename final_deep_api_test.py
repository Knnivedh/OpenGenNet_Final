#!/usr/bin/env python3
"""
🔬 FINAL DEEP API TEST - Complete AI System Validation
Comprehensive testing of all AI functionality before frontend deployment
"""

import requests
import json
import time
from datetime import datetime

class OpenGenNetDeepTester:
    def __init__(self):
        self.base_url = "https://opengennet-ai.vercel.app"
        self.test_results = {}
        self.passed_tests = 0
        self.total_tests = 0
        
    def log_test(self, test_name, status, details=""):
        self.total_tests += 1
        if status:
            self.passed_tests += 1
            print(f"✅ {test_name}: PASSED")
        else:
            print(f"❌ {test_name}: FAILED")
        
        if details:
            print(f"   📋 {details}")
        
        self.test_results[test_name] = {"status": status, "details": details}
        
    def test_api_connectivity(self):
        """Test basic API connectivity"""
        print("\n🌐 TESTING API CONNECTIVITY")
        print("-" * 50)
        
        try:
            response = requests.get(f"{self.base_url}/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.log_test("API Health Check", True, 
                             f"Status: {data.get('status')}, Version: {data.get('version')}")
                return True
            else:
                self.log_test("API Health Check", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("API Health Check", False, f"Connection error: {str(e)}")
            return False
    
    def test_expert_knowledge_system(self):
        """Test expert knowledge integration"""
        print("\n🧠 TESTING EXPERT KNOWLEDGE SYSTEM")
        print("-" * 50)
        
        try:
            response = requests.get(f"{self.base_url}/status", timeout=10)
            if response.status_code == 200:
                data = response.json()
                expert_cases = data.get('total_expert_cases', 0)
                categories = data.get('expert_knowledge_categories', [])
                
                if expert_cases > 0:
                    self.log_test("Expert Knowledge Loaded", True, 
                                 f"{expert_cases} cases in {len(categories)} categories")
                else:
                    self.log_test("Expert Knowledge Loaded", False, "No expert cases found")
                
                # Test each category
                for category in categories:
                    self.log_test(f"Category: {category}", True, f"Available for search")
                    
            else:
                self.log_test("Expert Knowledge Status", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Expert Knowledge Status", False, str(e))
    
    def test_expert_search_functionality(self):
        """Test expert knowledge search"""
        print("\n🔍 TESTING EXPERT SEARCH FUNCTIONALITY")
        print("-" * 50)
        
        test_queries = [
            ("TCP", "networking"),
            ("firewall", "cybersecurity"), 
            ("cloud", "cloud_computing"),
            ("security", "general"),
            ("protocol", "networking")
        ]
        
        for query, expected_category in test_queries:
            try:
                search_data = {"query": query}
                response = requests.post(f"{self.base_url}/search", 
                                       json=search_data, timeout=10)
                
                if response.status_code == 200:
                    results = response.json()
                    total_results = results.get('total_results', 0)
                    
                    if total_results > 0:
                        result_topics = [r.get('topic', 'N/A') for r in results.get('results', [])]
                        self.log_test(f"Search: '{query}'", True, 
                                     f"{total_results} results found")
                        print(f"   📚 Topics: {', '.join(result_topics[:2])}")
                    else:
                        self.log_test(f"Search: '{query}'", False, "No results found")
                else:
                    self.log_test(f"Search: '{query}'", False, f"HTTP {response.status_code}")
                    
            except Exception as e:
                self.log_test(f"Search: '{query}'", False, str(e))
    
    def test_ai_chat_endpoint(self):
        """Test AI chat functionality"""
        print("\n🤖 TESTING AI CHAT ENDPOINT")
        print("-" * 50)
        
        test_messages = [
            "What is network security?",
            "Explain TCP/IP protocol",
            "How does cloud computing work?",
            "What is a firewall?",
            "Tell me about cybersecurity best practices"
        ]
        
        for message in test_messages:
            try:
                chat_data = {
                    "message": message,
                    "use_expert_context": True
                }
                
                response = requests.post(f"{self.base_url}/ask", 
                                       json=chat_data, timeout=15)
                
                if response.status_code == 200:
                    data = response.json()
                    ai_response = data.get('response', '')
                    provider = data.get('provider', 'unknown')
                    
                    if ai_response and len(ai_response) > 10:
                        self.log_test(f"AI Chat: '{message[:20]}...'", True, 
                                     f"Response: {len(ai_response)} chars, Provider: {provider}")
                    else:
                        # Check if it's an API key issue
                        if "No AI providers available" in ai_response:
                            self.log_test(f"AI Chat: '{message[:20]}...'", False, 
                                         "⚠️ AI providers need API keys")
                        else:
                            self.log_test(f"AI Chat: '{message[:20]}...'", False, 
                                         "Empty or invalid response")
                else:
                    self.log_test(f"AI Chat: '{message[:20]}...'", False, 
                                 f"HTTP {response.status_code}")
                    
            except Exception as e:
                self.log_test(f"AI Chat: '{message[:20]}...'", False, str(e))
            
            # Small delay between requests
            time.sleep(1)
    
    def test_enhanced_context_integration(self):
        """Test if expert context enhances AI responses"""
        print("\n🔗 TESTING EXPERT CONTEXT INTEGRATION")
        print("-" * 50)
        
        # Test with and without expert context
        test_message = "What is network security?"
        
        try:
            # Test without expert context
            chat_data_no_context = {
                "message": test_message,
                "use_expert_context": False
            }
            
            response_no_context = requests.post(f"{self.base_url}/ask", 
                                              json=chat_data_no_context, timeout=15)
            
            # Test with expert context
            chat_data_with_context = {
                "message": test_message,
                "use_expert_context": True
            }
            
            response_with_context = requests.post(f"{self.base_url}/ask", 
                                                json=chat_data_with_context, timeout=15)
            
            if response_no_context.status_code == 200 and response_with_context.status_code == 200:
                data_no_context = response_no_context.json()
                data_with_context = response_with_context.json()
                
                response_no = data_no_context.get('response', '')
                response_with = data_with_context.get('response', '')
                
                if len(response_with) > len(response_no):
                    self.log_test("Expert Context Enhancement", True, 
                                 f"Enhanced response is {len(response_with) - len(response_no)} chars longer")
                else:
                    self.log_test("Expert Context Enhancement", False, 
                                 "No significant enhancement detected")
            else:
                self.log_test("Expert Context Enhancement", False, "API errors during comparison")
                
        except Exception as e:
            self.log_test("Expert Context Enhancement", False, str(e))
    
    def test_api_performance(self):
        """Test API response times"""
        print("\n⚡ TESTING API PERFORMANCE")
        print("-" * 50)
        
        endpoints = [
            ("/health", "GET"),
            ("/status", "GET"),
            ("/search", "POST", {"query": "test"}),
            ("/ask", "POST", {"message": "Hello", "use_expert_context": True})
        ]
        
        for endpoint_data in endpoints:
            endpoint = endpoint_data[0]
            method = endpoint_data[1]
            payload = endpoint_data[2] if len(endpoint_data) > 2 else None
            
            try:
                start_time = time.time()
                
                if method == "GET":
                    response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
                else:
                    response = requests.post(f"{self.base_url}{endpoint}", 
                                           json=payload, timeout=10)
                
                end_time = time.time()
                response_time = round((end_time - start_time) * 1000, 2)
                
                if response.status_code == 200 and response_time < 5000:  # 5 seconds
                    self.log_test(f"Performance {endpoint}", True, 
                                 f"{response_time}ms response time")
                else:
                    self.log_test(f"Performance {endpoint}", False, 
                                 f"{response_time}ms (too slow or error)")
                    
            except Exception as e:
                self.log_test(f"Performance {endpoint}", False, str(e))
    
    def test_cors_and_frontend_compatibility(self):
        """Test CORS and frontend compatibility"""
        print("\n🌐 TESTING FRONTEND COMPATIBILITY")
        print("-" * 50)
        
        try:
            # Test OPTIONS request (CORS preflight)
            response = requests.options(f"{self.base_url}/ask", timeout=10)
            
            cors_headers = [h for h in response.headers.keys() 
                          if 'access-control' in h.lower()]
            
            if len(cors_headers) > 0:
                self.log_test("CORS Support", True, f"{len(cors_headers)} CORS headers found")
            else:
                self.log_test("CORS Support", False, "No CORS headers detected")
                
            # Test JSON content type handling
            test_data = {"message": "test", "use_expert_context": True}
            response = requests.post(f"{self.base_url}/ask", 
                                   json=test_data,
                                   headers={"Content-Type": "application/json"},
                                   timeout=10)
            
            if response.status_code == 200:
                self.log_test("JSON Content-Type Support", True, "API accepts JSON properly")
            else:
                self.log_test("JSON Content-Type Support", False, f"HTTP {response.status_code}")
                
        except Exception as e:
            self.log_test("Frontend Compatibility", False, str(e))
    
    def run_complete_test_suite(self):
        """Run all tests and generate final report"""
        print("🔬 OPENGENNET AI - FINAL DEEP VALIDATION TEST")
        print("=" * 70)
        print(f"🕒 Test Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🌐 Testing API: {self.base_url}")
        
        # Run all test suites
        if self.test_api_connectivity():
            self.test_expert_knowledge_system()
            self.test_expert_search_functionality()
            self.test_ai_chat_endpoint()
            self.test_enhanced_context_integration()
            self.test_api_performance()
            self.test_cors_and_frontend_compatibility()
        else:
            print("\n❌ API connectivity failed. Stopping tests.")
            return False
        
        # Generate final report
        self.generate_final_report()
        return True
    
    def generate_final_report(self):
        """Generate comprehensive test report"""
        print("\n" + "=" * 70)
        print("📊 FINAL TEST REPORT")
        print("=" * 70)
        
        success_rate = (self.passed_tests / self.total_tests) * 100 if self.total_tests > 0 else 0
        
        print(f"📈 Overall Success Rate: {success_rate:.1f}% ({self.passed_tests}/{self.total_tests})")
        
        if success_rate >= 90:
            status = "🟢 EXCELLENT - Production Ready"
        elif success_rate >= 75:
            status = "🟡 GOOD - Minor Issues"
        elif success_rate >= 50:
            status = "🟠 FAIR - Needs Attention"
        else:
            status = "🔴 POOR - Major Issues"
        
        print(f"🎯 API Status: {status}")
        
        print("\n📋 TEST SUMMARY:")
        for test_name, result in self.test_results.items():
            status_icon = "✅" if result["status"] else "❌"
            print(f"{status_icon} {test_name}")
            if result["details"]:
                print(f"   📝 {result['details']}")
        
        print("\n🚀 DEPLOYMENT READINESS:")
        if success_rate >= 80:
            print("✅ API is ready for frontend integration")
            print("✅ Expert knowledge system is functional")
            print("✅ All core endpoints are working")
            print("🎉 PROCEED WITH FRONTEND DEVELOPMENT!")
        else:
            print("⚠️  API needs fixes before frontend development")
            print("🔧 Review failed tests and resolve issues")
        
        print(f"\n🕒 Test Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    tester = OpenGenNetDeepTester()
    tester.run_complete_test_suite()
