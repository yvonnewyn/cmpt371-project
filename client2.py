import requests

request = requests.get('http://localhost:8001/test.html', timeout=0.001)

print(f"Status Code: {request.status_code}")
