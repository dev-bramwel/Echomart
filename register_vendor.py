import requests

url = "http://127.0.0.1:8000/api/accounts/register/"

payload = {
    "user": {
        "username": "collins2",  # change to something unique
        "email": "collins2@example.com",
        "password": "pass123"
    },
    "shop_name": "Another Shop",
    "phone": "+254712345679"
}


headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print("Status Code:", response.status_code)  # ✅ Fixed typo here
print("Response:", response.json())
