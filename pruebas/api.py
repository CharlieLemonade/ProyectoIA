import requests

url = "http://127.0.0.1:5000/recommend"
payload = {
    "prompt": "I want a sushi restaurant with good reviews",
    "top_n": 5
}
response = requests.post(url, json=payload)
print(response.json())