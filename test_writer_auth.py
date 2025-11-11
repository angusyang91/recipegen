"""
Test script to verify Writer API authentication format
Tests both x-api-key and Authorization: Bearer formats
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('WRITER_API_KEY')

if not API_KEY:
    print("❌ WRITER_API_KEY not found in environment")
    exit(1)

print(f"🔑 Testing with API key: {API_KEY[:10]}...")

# Writer API endpoint
url = "https://api.writer.com/v1/chat"

# Simple test payload
payload = {
    "model": "palmyra-x5",
    "messages": [
        {"content": "Say 'hello' in JSON format: {\"message\": \"hello\"}", "role": "user"}
    ]
}

print("\n" + "="*80)
print("TEST 1: Using Authorization: Bearer header")
print("="*80)

headers_bearer = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

try:
    response = requests.post(url, headers=headers_bearer, json=payload, timeout=30)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text[:500]}")

    if response.status_code == 200:
        print("✅ SUCCESS: Authorization: Bearer format works!")
    else:
        print("❌ FAILED: Authorization: Bearer format doesn't work")
except Exception as e:
    print(f"❌ ERROR: {e}")

print("\n" + "="*80)
print("TEST 2: Using x-api-key header")
print("="*80)

headers_xapi = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}

try:
    response = requests.post(url, headers=headers_xapi, json=payload, timeout=30)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text[:500]}")

    if response.status_code == 200:
        print("✅ SUCCESS: x-api-key format works!")
    else:
        print("❌ FAILED: x-api-key format doesn't work")
except Exception as e:
    print(f"❌ ERROR: {e}")

print("\n" + "="*80)
print("CONCLUSION")
print("="*80)
print("Check which test succeeded above to determine the correct auth format")
