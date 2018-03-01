import json
import requests

access_token = "EAAaCCjExSOwBAGwe1ZAGZAUBCqSGLz9smTVqIuYQw1NSdGQkv0uhiMXwW1iJggIZAc0xUuaEGbJAy68zxJYVErh2xZBbJ8ZA3shVoYvVgyblzikAsoOXuAmMzgjS7lHar3D5ZCvsviweJNQMqXBbDtTPDM4hx3LF46MPAZBjBMcVhRJdZA1eTI8BNiJTgedL4ygzg2aKuhncSAZDZD"
headers = {'Authorization': access_token}
params = {"permission": "accounts"}
api_url_base = "http://graph.facebook.com/v2.12/me?fields=accounts"


response = requests.get(api_url_base, headers=headers)
print(response.status_code)
print(response.json())

