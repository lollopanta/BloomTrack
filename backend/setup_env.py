#!/usr/bin/env python3
"""
Environment Setup Script for BloomTracker Backend.

This script helps users set up their environment variables for the BloomTracker backend,
including DeepSeek API configuration.
"""

import os
import shutil
from pathlib import Path

def setup_environment():
    """Set up environment configuration for BloomTracker."""
    
    print("🌱 BloomTracker Environment Setup")
    print("=" * 40)
    
    # Check if .env file exists
    env_file = Path(".env")
    env_example = Path("env.example")
    
    if env_file.exists():
        print("✅ .env file already exists")
        print(f"   Location: {env_file.absolute()}")
        
        # Check if DEEPSEEK_API_KEY is set
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv('DEEPSEEK_API_KEY')
        if api_key and api_key != 'your_deepseek_api_key_here':
            print("✅ DEEPSEEK_API_KEY is configured")
            print(f"   Key: {api_key[:10]}...{api_key[-4:] if len(api_key) > 14 else '***'}")
        else:
            print("⚠️  DEEPSEEK_API_KEY needs to be configured")
            print("   Edit .env file and set your actual API key")
    else:
        print("📝 Creating .env file from template...")
        
        if env_example.exists():
            shutil.copy(env_example, env_file)
            print(f"✅ Created .env file from {env_example}")
            print("   Please edit .env file and set your DEEPSEEK_API_KEY")
        else:
            print("❌ env.example file not found")
            print("   Creating basic .env file...")
            
            # Create basic .env file
            with open(env_file, 'w') as f:
                f.write("# BloomTracker Environment Configuration\n")
                f.write("# DeepSeek AI API Configuration\n")
                f.write("DEEPSEEK_API_KEY=your_deepseek_api_key_here\n")
                f.write("\n# Application Configuration\n")
                f.write("# DEBUG=True\n")
                f.write("# LOG_LEVEL=INFO\n")
            
            print(f"✅ Created basic .env file")
            print("   Please edit .env file and set your DEEPSEEK_API_KEY")
    
    print("\n📋 Next Steps:")
    print("1. Edit .env file and set your DEEPSEEK_API_KEY")
    print("2. Get your API key from: https://platform.deepseek.com/")
    print("3. Run: python main.py")
    print("4. Test the AI endpoint: POST /plants/ai-advice")
    
    print("\n🔧 Environment Variables:")
    print("   DEEPSEEK_API_KEY - Your DeepSeek API key (required)")
    print("   DEBUG - Enable debug mode (optional)")
    print("   LOG_LEVEL - Set logging level (optional)")
    
    print("\n📚 Documentation:")
    print("   See DEEPSEEK_INTEGRATION.md for detailed API usage")

if __name__ == "__main__":
    setup_environment()
