"""
OpenGenNet AI - Expert RAG System
Transforms basic AI responses into TOP 1% cybersecurity and networking expertise
by integrating scraped expert knowledge with semantic search and intelligent ranking.
"""

import json
import os
import re
import logging
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import hashlib

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExpertRAGSystem:
    """
    Advanced RAG system that integrates scraped cybersecurity and networking
    expert knowledge to enhance AI responses to top 1% expert level.
    """
    
    def __init__(self, data_directory: str = "data/expert_knowledge"):
        """Initialize the Expert RAG System with knowledge base loading."""
        self.data_directory = data_directory
        self.knowledge_base = []
        self.embeddings_model = None
        self.tfidf_vectorizer = TfidfVectorizer(max_features=10000, stop_words='english')
        self.tfidf_matrix = None
        self.embeddings_cache = {}
        
        # Initialize semantic model (graceful fallback)
        try:
            # Try offline first, then skip if unavailable
            import os
            os.environ['TRANSFORMERS_OFFLINE'] = '1'
            from sentence_transformers import SentenceTransformer
            self.embeddings_model = SentenceTransformer('all-MiniLM-L6-v2', local_files_only=True)
            logger.info("✅ Semantic embeddings model loaded from cache")
        except Exception as e:
            logger.info("ℹ️ Semantic model not available offline - using TF-IDF only")
            self.embeddings_model = None
        
        # Load expert knowledge
        self._load_expert_knowledge()
        self._build_search_index()
        
        logger.info(f"🧠 Expert RAG System initialized with {len(self.knowledge_base)} expert cases")
    
    def _load_expert_knowledge(self) -> None:
        """Load all expert knowledge from the data directory."""
        logger.info("📚 Loading expert knowledge base...")
        
        # Load from all JSON files in the expert knowledge directory
        for root, dirs, files in os.walk(self.data_directory):
            for file in files:
                if file.endswith('.json'):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            self._extract_expert_cases(data, filepath)
                    except Exception as e:
                        logger.warning(f"⚠️ Could not load {filepath}: {e}")
        
        logger.info(f"✅ Loaded {len(self.knowledge_base)} expert knowledge cases")
    
    def _extract_expert_cases(self, data: Dict, source_file: str) -> None:
        """Extract expert cases from various JSON data structures."""
        try:
            # Handle different JSON structures
            if 'expert_training_cases' in data:
                # Master expert training format
                for case in data['expert_training_cases']:
                    self._add_expert_case(case, source_file)
            
            elif 'expert_knowledge' in data:
                # Expert knowledge format
                for category, cases in data['expert_knowledge'].items():
                    if isinstance(cases, list):
                        for case in cases:
                            case['category'] = category
                            self._add_expert_case(case, source_file)
            
            elif 'data' in data and isinstance(data['data'], list):
                # Generic data list format
                for case in data['data']:
                    self._add_expert_case(case, source_file)
            
            elif isinstance(data, list):
                # Direct list of cases
                for case in data:
                    self._add_expert_case(case, source_file)
            
            else:
                # Try to extract from any dictionary with relevant keys
                for key, value in data.items():
                    if isinstance(value, list) and len(value) > 0:
                        if isinstance(value[0], dict) and ('content' in value[0] or 'title' in value[0]):
                            for case in value:
                                case['category'] = key
                                self._add_expert_case(case, source_file)
        
        except Exception as e:
            logger.warning(f"⚠️ Error extracting cases from {source_file}: {e}")
    
    def _add_expert_case(self, case: Dict, source_file: str) -> None:
        """Add a single expert case to the knowledge base."""
        try:
            # Ensure required fields
            if not isinstance(case, dict):
                return
            
            # Extract content
            content = case.get('content', case.get('description', ''))
            title = case.get('title', case.get('name', 'Untitled'))
            
            if not content and not title:
                return
            
            # Create standardized expert case
            expert_case = {
                'id': case.get('case_id', case.get('id', self._generate_id(title, content))),
                'title': title,
                'content': content,
                'category': case.get('category', 'general'),
                'technology': case.get('technology', case.get('topic', '')),
                'level': case.get('level', case.get('expert_level', 'expert')),
                'quality_score': case.get('quality_score', case.get('confidence', 85)),
                'source_file': source_file,
                'keywords': self._extract_keywords(title + ' ' + content),
                'full_text': f"{title}. {content}"
            }
            
            self.knowledge_base.append(expert_case)
            
        except Exception as e:
            logger.warning(f"⚠️ Error adding expert case: {e}")
    
    def _generate_id(self, title: str, content: str) -> str:
        """Generate a unique ID for an expert case."""
        text = f"{title}_{content}"[:100]
        return hashlib.md5(text.encode()).hexdigest()[:12]
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from text."""
        # Common cybersecurity and networking keywords
        tech_keywords = [
            'firewall', 'vpn', 'network', 'security', 'encryption', 'aws', 'azure',
            'cisco', 'routing', 'switching', 'tcp', 'ip', 'ssl', 'tls', 'dns',
            'dhcp', 'vlan', 'bgp', 'ospf', 'ipsec', 'vulnerability', 'penetration',
            'malware', 'phishing', 'ddos', 'intrusion', 'authentication',
            'authorization', 'compliance', 'incident', 'forensics', 'monitoring'
        ]
        
        text_lower = text.lower()
        found_keywords = [kw for kw in tech_keywords if kw in text_lower]
        
        # Add regex-extracted technical terms
        tech_patterns = [
            r'\b\d+\.\d+\.\d+\.\d+\b',  # IP addresses
            r'\b[A-Z]{2,10}\b',          # Acronyms
            r'\b\w*[Pp]ort\s*\d+\b',    # Port references
        ]
        
        for pattern in tech_patterns:
            matches = re.findall(pattern, text)
            found_keywords.extend(matches)
        
        return list(set(found_keywords))
    
    def _build_search_index(self) -> None:
        """Build search indexes for fast retrieval."""
        if not self.knowledge_base:
            logger.warning("⚠️ No knowledge base to index")
            return
        
        logger.info("🔍 Building search indexes...")
        
        # Build TF-IDF index
        texts = [case['full_text'] for case in self.knowledge_base]
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(texts)
        
        logger.info("✅ Search indexes built successfully")
    
    def search_expert_knowledge(self, query: str, top_k: int = 5, min_score: float = 0.1) -> List[Dict]:
        """
        Search expert knowledge using hybrid semantic + keyword approach.
        
        Args:
            query: Search query
            top_k: Number of top results to return
            min_score: Minimum relevance score threshold
            
        Returns:
            List of expert knowledge cases with relevance scores
        """
        if not self.knowledge_base:
            return []
        
        results = []
        
        # Method 1: TF-IDF keyword search
        if self.tfidf_matrix is not None:
            query_vector = self.tfidf_vectorizer.transform([query])
            tfidf_scores = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
            
            for i, score in enumerate(tfidf_scores):
                if score >= min_score:
                    case = self.knowledge_base[i].copy()
                    case['relevance_score'] = score
                    case['search_method'] = 'tfidf'
                    results.append(case)
        
        # Method 2: Semantic search (if available)
        if self.embeddings_model:
            try:
                query_embedding = self.embeddings_model.encode([query])
                
                for i, case in enumerate(self.knowledge_base):
                    case_text = case['full_text']
                    case_embedding = self.embeddings_model.encode([case_text])
                    
                    semantic_score = cosine_similarity(query_embedding, case_embedding)[0][0]
                    
                    if semantic_score >= min_score:
                        case_copy = case.copy()
                        case_copy['relevance_score'] = semantic_score
                        case_copy['search_method'] = 'semantic'
                        results.append(case_copy)
                        
            except Exception as e:
                logger.warning(f"⚠️ Semantic search error: {e}")
        
        # Method 3: Keyword matching
        query_lower = query.lower()
        for case in self.knowledge_base:
            keyword_matches = sum(1 for kw in case['keywords'] if kw.lower() in query_lower)
            if keyword_matches > 0:
                keyword_score = min(keyword_matches / 10.0, 1.0)  # Normalize
                
                if keyword_score >= min_score:
                    case_copy = case.copy()
                    case_copy['relevance_score'] = keyword_score
                    case_copy['search_method'] = 'keywords'
                    results.append(case_copy)
        
        # Deduplicate and rank results
        seen_ids = set()
        unique_results = []
        for result in results:
            if result['id'] not in seen_ids:
                seen_ids.add(result['id'])
                unique_results.append(result)
        
        # Sort by relevance score and quality
        unique_results.sort(
            key=lambda x: (x['relevance_score'] * 0.7 + (x['quality_score'] / 100) * 0.3),
            reverse=True
        )
        
        return unique_results[:top_k]
    
    def enhance_ai_response(self, user_query: str, ai_response: str, provider: str = "unknown") -> Dict[str, Any]:
        """
        Enhance AI response with expert knowledge context.
        
        Args:
            user_query: Original user question
            ai_response: Basic AI response to enhance
            provider: AI provider name
            
        Returns:
            Enhanced response with expert context
        """
        logger.info(f"🚀 Enhancing response for query: {user_query[:100]}...")
        
        # Search for relevant expert knowledge
        expert_cases = self.search_expert_knowledge(user_query, top_k=3)
        
        if not expert_cases:
            return {
                'enhanced_response': ai_response,
                'expert_enhancement': False,
                'expert_sources': 0,
                'confidence_boost': 0,
                'enhancement_summary': "No relevant expert knowledge found"
            }
        
        # Build expert context
        expert_context = self._build_expert_context(expert_cases)
        
        # Enhance the response
        enhanced_response = self._integrate_expert_knowledge(
            user_query, ai_response, expert_context, expert_cases
        )
        
        # Calculate confidence boost
        avg_quality = sum(case['quality_score'] for case in expert_cases) / len(expert_cases)
        avg_relevance = sum(case['relevance_score'] for case in expert_cases) / len(expert_cases)
        confidence_boost = (avg_quality * avg_relevance) / 100
        
        return {
            'enhanced_response': enhanced_response,
            'expert_enhancement': True,
            'expert_sources': len(expert_cases),
            'confidence_boost': round(confidence_boost * 100, 1),
            'enhancement_summary': f"Enhanced with {len(expert_cases)} expert sources (avg quality: {avg_quality:.1f}%)",
            'expert_cases_used': [
                {
                    'title': case['title'],
                    'category': case['category'],
                    'relevance': round(case['relevance_score'], 3),
                    'quality': case['quality_score']
                }
                for case in expert_cases
            ],
            'original_response': ai_response,
            'provider': provider
        }
    
    def _build_expert_context(self, expert_cases: List[Dict]) -> str:
        """Build expert context from relevant cases."""
        context_parts = []
        
        for i, case in enumerate(expert_cases, 1):
            context_parts.append(
                f"Expert Source {i} ({case['category']}):\n"
                f"Title: {case['title']}\n"
                f"Content: {case['content'][:500]}{'...' if len(case['content']) > 500 else ''}\n"
                f"Quality Score: {case['quality_score']}%\n"
            )
        
        return "\n".join(context_parts)
    
    def _integrate_expert_knowledge(self, query: str, ai_response: str, expert_context: str, expert_cases: List[Dict]) -> str:
        """Integrate expert knowledge into the AI response."""
        
        # Build enhanced response
        enhanced_parts = []
        
        # Start with improved AI response
        enhanced_parts.append("📋 **Enhanced Expert Response:**\n")
        enhanced_parts.append(ai_response)
        
        # Add expert insights
        enhanced_parts.append("\n\n🎯 **Expert Knowledge Integration:**")
        
        # Add specific expert insights
        categories = set(case['category'] for case in expert_cases)
        for category in categories:
            category_cases = [case for case in expert_cases if case['category'] == category]
            
            enhanced_parts.append(f"\n**{category.replace('_', ' ').title()} Expertise:**")
            
            for case in category_cases[:2]:  # Limit to top 2 per category
                # Extract key insights
                content = case['content']
                if len(content) > 300:
                    # Try to extract key sentences
                    sentences = content.split('. ')
                    key_sentences = [s for s in sentences if any(kw in s.lower() for kw in ['expert', 'best practice', 'recommendation', 'critical', 'important'])]
                    if key_sentences:
                        content = '. '.join(key_sentences[:2]) + '.'
                    else:
                        content = content[:300] + '...'
                
                enhanced_parts.append(f"• {content}")
        
        # Add technical recommendations
        enhanced_parts.append("\n\n💡 **Expert Recommendations:**")
        
        # Extract actionable insights
        recommendations = []
        for case in expert_cases:
            content = case['content'].lower()
            if 'best practice' in content or 'recommendation' in content:
                # Extract recommendation sentences
                sentences = case['content'].split('.')
                for sentence in sentences:
                    if any(word in sentence.lower() for word in ['recommend', 'should', 'best practice', 'ensure']):
                        if len(sentence.strip()) > 10:
                            recommendations.append(sentence.strip())
                            break
        
        for i, rec in enumerate(recommendations[:3], 1):
            enhanced_parts.append(f"{i}. {rec}")
        
        if not recommendations:
            enhanced_parts.append("• Implement industry best practices for security and performance")
            enhanced_parts.append("• Follow vendor-specific configuration guidelines")
            enhanced_parts.append("• Regular monitoring and maintenance recommended")
        
        # Add source attribution
        enhanced_parts.append(f"\n\n📊 **Sources:** Based on {len(expert_cases)} expert knowledge sources with average quality score of {sum(case['quality_score'] for case in expert_cases) / len(expert_cases):.1f}%")
        
        return "\n".join(enhanced_parts)
    
    def get_knowledge_stats(self) -> Dict[str, Any]:
        """Get statistics about the knowledge base."""
        if not self.knowledge_base:
            return {"error": "No knowledge base loaded"}
        
        categories = {}
        technologies = {}
        quality_scores = []
        
        for case in self.knowledge_base:
            # Count categories
            cat = case['category']
            categories[cat] = categories.get(cat, 0) + 1
            
            # Count technologies
            tech = case['technology']
            if tech:
                technologies[tech] = technologies.get(tech, 0) + 1
            
            # Collect quality scores
            quality_scores.append(case['quality_score'])
        
        return {
            'total_cases': len(self.knowledge_base),
            'categories': dict(sorted(categories.items(), key=lambda x: x[1], reverse=True)),
            'top_technologies': dict(sorted(technologies.items(), key=lambda x: x[1], reverse=True)[:10]),
            'quality_stats': {
                'average': sum(quality_scores) / len(quality_scores),
                'min': min(quality_scores),
                'max': max(quality_scores)
            },
            'search_capabilities': {
                'tfidf_available': self.tfidf_matrix is not None,
                'semantic_available': self.embeddings_model is not None
            }
        }

# Global RAG system instance
_rag_system = None

def get_rag_system() -> ExpertRAGSystem:
    """Get or create the global RAG system instance."""
    global _rag_system
    if _rag_system is None:
        # Use the correct data directory path
        import os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        correct_data_dir = os.path.join(current_dir, "data", "organized_expert_knowledge")
        _rag_system = ExpertRAGSystem(correct_data_dir)
    return _rag_system

def enhance_response(user_query: str, ai_response: str, provider: str = "unknown") -> Dict[str, Any]:
    """
    Main function to enhance AI responses with expert knowledge.
    
    Args:
        user_query: Original user question
        ai_response: Basic AI response to enhance
        provider: AI provider name
        
    Returns:
        Enhanced response with expert context
    """
    rag_system = get_rag_system()
    return rag_system.enhance_ai_response(user_query, ai_response, provider)

if __name__ == "__main__":
    # Test the RAG system
    print("🧠 Testing OpenGenNet Expert RAG System")
    print("=" * 50)
    
    # Initialize system
    rag = ExpertRAGSystem()
    
    # Show knowledge stats
    stats = rag.get_knowledge_stats()
    print(f"📊 Knowledge Base Stats:")
    print(f"   Total Cases: {stats['total_cases']}")
    print(f"   Categories: {len(stats['categories'])}")
    print(f"   Avg Quality: {stats['quality_stats']['average']:.1f}%")
    print()
    
    # Test search
    test_query = "How to configure AWS VPC for enterprise security?"
    print(f"🔍 Testing search for: {test_query}")
    
    results = rag.search_expert_knowledge(test_query, top_k=3)
    print(f"   Found {len(results)} relevant expert cases")
    
    for i, result in enumerate(results, 1):
        print(f"   {i}. {result['title']} (score: {result['relevance_score']:.3f})")
    
    print()
    
    # Test enhancement
    basic_response = "AWS VPC provides network isolation in the cloud with subnets and security groups."
    enhanced = rag.enhance_ai_response(test_query, basic_response, "test")
    
    print("🚀 Enhancement Test:")
    print(f"   Expert Enhancement: {enhanced['expert_enhancement']}")
    print(f"   Sources Used: {enhanced['expert_sources']}")
    print(f"   Confidence Boost: {enhanced['confidence_boost']}%")
    print()
    print("Enhanced Response Preview:")
    print(enhanced['enhanced_response'][:300] + "...")
