import requests

endpoints = [
    "http://localhost:8000/api/models",
    "http://localhost:8000/api/models/groq"
]

for url in endpoints:
    try:
        print(f"Testing {url}...")
        response = requests.get(url, timeout=5)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {list(response.json().keys())}")
        else:
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    print("-" * 20)
