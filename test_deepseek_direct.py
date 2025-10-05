#!/usr/bin/env python3
"""
Test DeepSeek API directly
"""

import asyncio
import aiohttp
import os
from dotenv import load_dotenv

# Load environment variables from backend directory
load_dotenv('backend/.env')

async def test_deepseek_api():
    """Test DeepSeek API directly"""
    
    api_key = os.getenv('DEEPSEEK_API_KEY')
    if not api_key:
        print("❌ No DEEPSEEK_API_KEY found in environment")
        return
    
    print(f"🔑 API Key found: {api_key[:10]}...")
    
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "user",
                "content": "What is the growing season for chili peppers? Please be specific and concise."
            }
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as response:
                print(f"📡 Response Status: {response.status}")
                
                if response.status == 200:
                    result = await response.json()
                    print("✅ Success!")
                    print(f"🤖 AI Response: {result['choices'][0]['message']['content']}")
                else:
                    error_text = await response.text()
                    print(f"❌ Error: {response.status}")
                    print(f"Error details: {error_text}")
                    
    except Exception as e:
        print(f"❌ Exception: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_deepseek_api())
