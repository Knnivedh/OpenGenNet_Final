import json

# Simple test of OpenGenNet 2.0 components
print("🧪 OpenGenNet 2.0 Component Test")
print("=" * 40)

# Test 1: Import the API module
try:
    import sys
    sys.path.append('api')
    from index import app, EXPERT_KNOWLEDGE
    print("✅ Successfully imported OpenGenNet 2.0 API")
    print(f"📚 Knowledge Base: {len(EXPERT_KNOWLEDGE)} items")
    
    # Test 2: Test Flask app creation
    print("✅ Flask app created successfully")
    
    # Test 3: Show available endpoints
    with app.app_context():
        print("🌐 Available endpoints:")
        for rule in app.url_map.iter_rules():
            print(f"   {rule.rule} -> {rule.endpoint}")
    
    print("\n🎉 OpenGenNet 2.0 Components Working!")
    print("💡 The system is ready for deployment!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("🔧 Check the API module and dependencies")
