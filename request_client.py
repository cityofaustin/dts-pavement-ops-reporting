# Only for requesting a client ID and secret, should only need to be run once.
# docs: https://docs.agileassets.com/display/PD10/REST+API+V2+Security
import os
import requests
import base64


USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
BASE_URL = os.getenv("BASE_URL")

endpoint = "/rest/oauth2/secret"
url = f"{BASE_URL}{endpoint}"

payload = {
    "redirect_uri": BASE_URL,
    "client_id": "API_VIEWER",
    "grant_type": "authorization_code,password,refresh_token",
}

# Encoding user/password into a base64 string for auth
login_string = f"{USERNAME}:{PASSWORD}"
bytes_data = login_string.encode("utf-8")
encoded_bytes = base64.b64encode(bytes_data)
encoded_string = encoded_bytes.decode("utf-8")

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Authorization": encoded_string,
    "Cache-Control": "no-cache",
}

session = requests.Session()

response = session.post(
    url,
    data=payload,
    headers=headers,
)
response.raise_for_status()

print(response.status_code)
# Grab Client ID and Client Secret from here:
print(response.text)
