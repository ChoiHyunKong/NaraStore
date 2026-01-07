import google.generativeai as genai
import sys
import os

def test_key(api_key):
    print(f"Testing API Key: {api_key[:5]}...{api_key[-5:]}")
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content("Hello, just checking my quota.")
        print("\n[SUCCESS] Key is working!")
        print(f"Response: {response.text}")
    except Exception as e:
        print("\n[ERROR] Request Failed")
        print(f"Error Details: {e}")

if __name__ == "__main__":
    key = "AIzaSyAkrVU3y9cOdOCyqdVLxRg45rWaGHNAOUw"
    test_key(key)
