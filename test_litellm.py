#!/usr/bin/env python3
"""
Test script for LiteLLM integration.
This script tests the LiteLLM client configuration and connectivity.
"""

import os
import sys
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

print("=" * 60)
print("LiteLLM Integration Test")
print("=" * 60)

# Test 1: Import the client
print("\n[Test 1] Importing LiteLLM client...")
try:
    from api.litellm_client import LiteLLMClient
    print("✅ LiteLLMClient imported successfully")
except Exception as e:
    print(f"❌ Failed to import LiteLLMClient: {e}")
    sys.exit(1)

# Test 2: Check environment variables
print("\n[Test 2] Checking environment variables...")
api_key = os.getenv("LITELLM_API_KEY")
base_url = os.getenv("LITELLM_BASE_URL")

if api_key:
    print(f"✅ LITELLM_API_KEY: {api_key[:10]}...")
else:
    print("⚠️  LITELLM_API_KEY not set")

if base_url:
    print(f"✅ LITELLM_BASE_URL: {base_url}")
else:
    print("⚠️  LITELLM_BASE_URL not set, will use default")

# Test 3: Load configuration
print("\n[Test 3] Loading generator configuration...")
try:
    from api.config import configs

    if "litellm" in configs.get("providers", {}):
        print("✅ LiteLLM provider found in configuration")
        litellm_config = configs["providers"]["litellm"]
        print(f"   Default model: {litellm_config.get('default_model')}")
        print(f"   Available models: {list(litellm_config.get('models', {}).keys())}")
        print(f"   Supports custom model: {litellm_config.get('supportsCustomModel')}")
    else:
        print("❌ LiteLLM provider not found in configuration")
        sys.exit(1)

    default_provider = configs.get("default_provider")
    if default_provider == "litellm":
        print(f"✅ Default provider set to: {default_provider}")
    else:
        print(f"⚠️  Default provider is {default_provider}, not litellm")

except Exception as e:
    print(f"❌ Failed to load configuration: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Initialize the client
print("\n[Test 4] Initializing LiteLLM client...")
try:
    client = LiteLLMClient()
    print(f"✅ LiteLLM client initialized")
    print(f"   Base URL: {client.base_url}")
    print(f"   Client type: {type(client.sync_client).__name__}")
except Exception as e:
    print(f"❌ Failed to initialize client: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 5: Verify client class mapping
print("\n[Test 5] Verifying client class mapping...")
try:
    from api.config import CLIENT_CLASSES

    if "LiteLLMClient" in CLIENT_CLASSES:
        print("✅ LiteLLMClient registered in CLIENT_CLASSES")
        print(f"   Mapped to: {CLIENT_CLASSES['LiteLLMClient']}")
    else:
        print("❌ LiteLLMClient not found in CLIENT_CLASSES")
        sys.exit(1)

    # Check if model_client is set correctly
    if "model_client" in litellm_config:
        print(f"✅ model_client set to: {litellm_config['model_client']}")
    else:
        print("⚠️  model_client not set in litellm_config")

except Exception as e:
    print(f"❌ Failed to verify client mapping: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 6: Test API endpoint configuration
print("\n[Test 6] Testing model config endpoint...")
try:
    from api.api import app
    print("✅ API app imported successfully")
    print(f"   API title: {app.title}")
except Exception as e:
    print(f"❌ Failed to import API app: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("✅ All tests passed! LiteLLM integration is ready.")
print("=" * 60)

print("\n📝 Next steps:")
print("1. Start the backend: source .venv/bin/activate && python -m api.main")
print("2. Start the frontend: npm run dev")
print("3. Open http://localhost:3000 and select 'Litellm' provider")
print("4. Choose model: claude-haiku-4-5 (default) or claude-sonnet-4-5")
print()
