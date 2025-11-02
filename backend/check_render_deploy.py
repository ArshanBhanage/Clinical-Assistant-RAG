#!/usr/bin/env python3
"""
Render deployment validation script
Checks if all required files and environment variables are present
"""
import os
import sys

def check_environment():
    """Check if deployment environment is properly configured"""
    print("🔍 Checking Render Deployment Environment")
    print("=" * 60)
    
    issues = []
    warnings = []
    
    # Check Python version
    print(f"\n✅ Python version: {sys.version.split()[0]}")
    
    # Check environment variables
    print("\n📋 Environment Variables:")
    required_vars = ["OPENROUTER_API_KEY"]
    optional_vars = ["PORT", "OPENROUTER_MODEL"]
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"  ✅ {var}: {'*' * 20} (set)")
        else:
            print(f"  ❌ {var}: NOT SET")
            issues.append(f"Missing required environment variable: {var}")
    
    for var in optional_vars:
        value = os.getenv(var)
        if value:
            print(f"  ✅ {var}: {value}")
        else:
            print(f"  ⚠️  {var}: Not set (using default)")
            warnings.append(f"Optional variable not set: {var}")
    
    # Check indexes directory
    print("\n📁 Indexes Directory:")
    index_paths = ["/app/indexes", "./indexes"]
    index_dir = None
    
    for path in index_paths:
        if os.path.exists(path):
            index_dir = path
            print(f"  ✅ Found: {path}")
            break
    
    if not index_dir:
        print(f"  ❌ No indexes directory found!")
        print(f"     Checked: {', '.join(index_paths)}")
        issues.append("Indexes directory not found")
    else:
        # Check required files
        print(f"\n📊 Index Files in {index_dir}:")
        required_files = [
            "covid_index.faiss",
            "covid_metadata.pkl",
            "diabetes_index.faiss",
            "diabetes_metadata.pkl",
            "heart_attack_index.faiss",
            "heart_attack_metadata.pkl",
            "knee_injuries_index.faiss",
            "knee_injuries_metadata.pkl",
            "all_documents.pkl"
        ]
        
        for filename in required_files:
            filepath = os.path.join(index_dir, filename)
            if os.path.exists(filepath):
                size_mb = os.path.getsize(filepath) / (1024 * 1024)
                print(f"  ✅ {filename}: {size_mb:.2f} MB")
            else:
                print(f"  ❌ {filename}: NOT FOUND")
                issues.append(f"Missing index file: {filename}")
        
        # Calculate total size
        if os.path.exists(index_dir):
            total_size = 0
            for root, dirs, files in os.walk(index_dir):
                for file in files:
                    filepath = os.path.join(root, file)
                    total_size += os.path.getsize(filepath)
            
            total_mb = total_size / (1024 * 1024)
            print(f"\n  📊 Total index size: {total_mb:.2f} MB")
            
            if total_mb < 200:
                warnings.append(f"Index size ({total_mb:.0f}MB) seems small. Expected ~293MB")
    
    # Check dependencies
    print("\n📦 Required Python Packages:")
    required_packages = [
        "fastapi",
        "uvicorn",
        "faiss-cpu",
        "sentence-transformers",
        "requests"
    ]
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package}")
            issues.append(f"Missing Python package: {package}")
    
    # Print summary
    print("\n" + "=" * 60)
    print("📋 VALIDATION SUMMARY")
    print("=" * 60)
    
    if not issues and not warnings:
        print("✅ All checks passed! Deployment ready.")
        return 0
    
    if warnings:
        print(f"\n⚠️  {len(warnings)} Warning(s):")
        for warning in warnings:
            print(f"   • {warning}")
    
    if issues:
        print(f"\n❌ {len(issues)} Issue(s) Found:")
        for issue in issues:
            print(f"   • {issue}")
        print("\n🔧 Fix these issues before deployment will work properly.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = check_environment()
    sys.exit(exit_code)
