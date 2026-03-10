# Docs: https://docs.agileassets.com/display/PD10/The+Q+Object
import requests
import os
import json
import argparse
import logging

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
BASE_URL = os.getenv("BASE_URL")

def make_agileassets_request(endpoint, method="GET", data=None, headers=None, params=None):
    url = f"{BASE_URL}{endpoint}"
    response = requests.request(method, url, data=data, headers=headers, params=params)
    response.raise_for_status()
    return response


def get_token():
    # Getting an access token for auth
    endpoint = "/rest/oauth2/token"

    payload = {
        "grant_type": "password",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "username": USERNAME,
        "password": PASSWORD,
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Cache-Control": "no-cache",
    }

    response = make_agileassets_request(endpoint, method="POST", data=payload, headers=headers)

    token = response.json()["access_token"]
    return token

def get_report_data(token, report_name):
    # Downloading report data using our access token
    endpoint = f"/rest/v1/lookup/view/{report_name}"

    keep_going = True
    page = 1
    output = []
    while keep_going:
        params = {
            "q": json.dumps({
                "page": {
                    "size": 1000,
                    "number": page
                },
                # "filter": [["FISCAL_YEAR", "in", "2024"]]
            })
        }

        headers = {
            "Authorization": f"Bearer {token}",
            "Cache-Control": "no-cache",
        }

        response = make_agileassets_request(endpoint, method="get", params=params, headers=headers)
        data = response.json()
        # detecting if we've reached the end of the report
        if not data:
            keep_going = False
        else:
            output += data
            page += 1
    return output

def main(args):
    report_name = args.report
    token = get_token()

    logging.info(f"Downloading Report: {report_name}")
    data = get_report_data(token, report_name)
    print(data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", "-r", required=True, help="The name of the report to download.")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    main(args)
