#!/usr/bin/env python3
"""
Test LiteLLM embeddings API
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

print("=" * 60)
print("LiteLLM Embeddings API Test")
print("=" * 60)

# Test 1: Check environment variables
print("\n[Test 1] Checking environment variables...")
litellm_key = os.getenv("LITELLM_API_KEY")
litellm_url = os.getenv("LITELLM_BASE_URL")
openai_key = os.getenv("OPENAI_API_KEY")
openai_url = os.getenv("OPENAI_BASE_URL")

print(f"LITELLM_API_KEY: {litellm_key[:20] if litellm_key else 'Not set'}...")
print(f"LITELLM_BASE_URL: {litellm_url}")
print(f"OPENAI_API_KEY: {openai_key[:20] if openai_key else 'Not set'}...")
print(f"OPENAI_BASE_URL: {openai_url}")

# Test 2: Try calling embedding API
print("\n[Test 2] Testing embedding API call...")

try:
    from openai import OpenAI

    # Use OpenAI client pointing to LiteLLM
    client = OpenAI(
        api_key=openai_key,
        base_url=openai_url
    )

    print(f"Calling API: {openai_url}/embeddings")
    print("Model: text-embedding-3-small")
    print("Input: 'Hello, world!'")

    import time
    start_time = time.time()

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input="Hello, world!",
        dimensions=256,
        encoding_format="float"
    )

    end_time = time.time()
    elapsed = end_time - start_time

    print(f"\n✅ Success! Took {elapsed:.2f} seconds")
    print(f"Embedding dimension: {len(response.data[0].embedding)}")
    print(f"First 5 values: {response.data[0].embedding[:5]}")
    print(f"Usage: {response.usage}")

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ Test completed successfully!")
print("=" * 60)
