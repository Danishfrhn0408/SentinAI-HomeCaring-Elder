import requests
import os
from dotenv import load_dotenv

# Baca API Key dari fail .env
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

print(f"Sedang menguji API Key: {API_KEY[:10]}...\n")

# Tanya terus pelayan Google
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print("✅ BERJAYA! Ini senarai model rasmi yang API Key anda boleh guna:")
    for model in data.get("models", []):
        print("-", model["name"])
else:
    print("❌ ERROR PADA API KEY:")
    print(response.text)