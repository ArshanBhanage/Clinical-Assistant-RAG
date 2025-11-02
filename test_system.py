#!/usr/bin/env python3
"""
Test script to verify the Clinical AI Assistant is working correctly
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import config
        print("  ✓ config.py")
    except Exception as e:
        print(f"  ✗ config.py: {e}")
        return False
    
    try:
        import data_ingestion
        print("  ✓ data_ingestion.py")
    except Exception as e:
        print(f"  ✗ data_ingestion.py: {e}")
        return False
    
    try:
        import rag_pipeline
        print("  ✓ rag_pipeline.py")
    except Exception as e:
        print(f"  ✗ rag_pipeline.py: {e}")
        return False
    
    try:
        import visualizer
        print("  ✓ visualizer.py")
    except Exception as e:
        print(f"  ✗ visualizer.py: {e}")
        return False
    
    return True

def test_configuration():
    """Test that configuration is valid"""
    print("\nTesting configuration...")
    
    try:
        from config import DOMAINS, VISION_AGENT_API_KEY, OPENROUTER_API_KEY
        
        # Check domains
        if len(DOMAINS) == 3:
            print(f"  ✓ Found {len(DOMAINS)} domains")
        else:
            print(f"  ✗ Expected 3 domains, found {len(DOMAINS)}")
            return False
        
        # Check API keys
        if VISION_AGENT_API_KEY and VISION_AGENT_API_KEY != "your_key_here":
            print("  ✓ Landing AI API key configured")
        else:
            print("  ✗ Landing AI API key not configured")
            return False
        
        if OPENROUTER_API_KEY:
            if OPENROUTER_API_KEY == "your_openrouter_api_key_here":
                print("  ⚠ OpenRouter API key needs to be updated")
            else:
                print("  ✓ OpenRouter API key configured")
        else:
            print("  ✗ OpenRouter API key not set")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ✗ Configuration error: {e}")
        return False

def test_data_files():
    """Test that data directories and files exist"""
    print("\nTesting data files...")
    
    from config import DOMAINS
    
    all_good = True
    
    for domain_id, domain_config in DOMAINS.items():
        print(f"\n  Domain: {domain_id}")
        
        # Check PDF folder
        pdf_folder = domain_config['pdf_folder']
        if os.path.exists(pdf_folder):
            pdf_count = len([f for f in os.listdir(pdf_folder) if f.endswith('.pdf')])
            if pdf_count > 0:
                print(f"    ✓ PDF folder exists with {pdf_count} PDF(s)")
            else:
                print(f"    ⚠ PDF folder exists but no PDFs found")
        else:
            print(f"    ✗ PDF folder does not exist: {pdf_folder}")
            all_good = False
        
        # Check CSV files
        csv_files = domain_config.get('csv_files', [])
        for csv_file in csv_files:
            if os.path.exists(csv_file):
                print(f"    ✓ CSV file exists: {os.path.basename(csv_file)}")
            else:
                print(f"    ⚠ CSV file not found: {csv_file}")
    
    return all_good

def test_embedding_model():
    """Test that embedding model can be loaded"""
    print("\nTesting embedding model...")
    
    try:
        from sentence_transformers import SentenceTransformer
        from config import EMBEDDING_MODEL
        
        print(f"  Loading model: {EMBEDDING_MODEL}")
        model = SentenceTransformer(EMBEDDING_MODEL)
        
        # Test encoding
        test_text = "This is a test sentence."
        embedding = model.encode([test_text])
        
        print(f"  ✓ Model loaded successfully")
        print(f"  ✓ Embedding dimension: {embedding.shape[1]}")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Error loading embedding model: {e}")
        return False

def test_indexes():
    """Test if indexes exist and can be loaded"""
    print("\nTesting indexes...")
    
    from config import DOMAINS
    import os
    
    indexes_exist = False
    
    for domain_id, domain_config in DOMAINS.items():
        index_path = domain_config['index_path']
        metadata_path = domain_config['metadata_path']
        
        if os.path.exists(index_path) and os.path.exists(metadata_path):
            print(f"  ✓ {domain_id} index exists")
            indexes_exist = True
        else:
            print(f"  ⚠ {domain_id} index not found (run data_ingestion.py and rag_pipeline.py)")
    
    if not indexes_exist:
        print("\n  ℹ️  No indexes found. This is normal for first-time setup.")
        print("     Run: python backend/data_ingestion.py")
        print("     Then: python backend/rag_pipeline.py")
    
    return True  # Not a failure if indexes don't exist yet

def main():
    """Run all tests"""
    print("="*60)
    print("Clinical AI Assistant - System Test")
    print("="*60)
    print()
    
    # Change to backend directory
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    os.chdir(backend_dir)
    
    tests = [
        ("Imports", test_imports),
        ("Configuration", test_configuration),
        ("Data Files", test_data_files),
        ("Embedding Model", test_embedding_model),
        ("Indexes", test_indexes),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {test_name}")
    
    print()
    print(f"Result: {passed}/{total} tests passed")
    print()
    
    if passed == total:
        print("✓ All tests passed! System is ready.")
        print()
        print("Next steps:")
        print("  1. Add PDF files to backend/data/*/pdfs/ folders")
        print("  2. Update OpenRouter API key in backend/.env")
        print("  3. Run: ./setup.sh")
        print("  4. Start the application: ./start.sh")
        return 0
    else:
        print("⚠ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
