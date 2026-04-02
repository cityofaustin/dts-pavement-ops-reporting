import requests
import os
import json
import argparse
import logging
from sodapy import Socrata

from config import REPORTS

# AgileAssets API
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
BASE_URL = os.getenv("BASE_URL")

# Socrata Data Portal API
SO_WEB = os.getenv("SO_WEB")
SO_TOKEN = os.getenv("SO_TOKEN")
SO_KEY = os.getenv("SO_KEY")
SO_SECRET = os.getenv("SO_SECRET")


def make_agileassets_request(
    endpoint, method="GET", data=None, headers=None, params=None
):
    """
    A wrapper function around Requests for making http requests to the AgileAssets API.
    :param endpoint: The endpoint to make the request to (e.g. /rest/v1/lookup/view/my_report)
    :param method: GET, POST, PUT, DELETE
    :param data: Request body
    :param headers: Request headers
    :param params: Request url parameters
    :return: requests.Response
    """
    url = f"{BASE_URL}{endpoint}"
    response = requests.request(method, url, data=data, headers=headers, params=params)
    response.raise_for_status()
    return response


def get_token():
    """
    Get a temporary access token for authentication with AgileAssets API
    Docs: https://docs.agileassets.com/display/PD10/REST+API+V2+Security
    :return: str access token
    """
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

    response = make_agileassets_request(
        endpoint, method="POST", data=payload, headers=headers
    )

    token = response.json()["access_token"]
    return token


def get_report_data(token, report_name, report):
    """
    :param token: access token for AgileAssets API
    :param report_name: name of the report to download
    :param report: dict of report metadata from config.py
    :return: list of dicts containing the report data
    """
    # Downloading report data using our access token
    endpoint = f"/rest/v1/lookup/view/{report_name}"

    keep_going = True
    page = 1
    output = []
    while keep_going:
        params = {"q": json.dumps({"page": {"size": 1000, "number": page}})}
        if report["filters"]:
            params = {
                "q": json.dumps(
                    {
                        "page": {"size": 1000, "number": page},
                        "filter": report["filters"],
                    }
                )
            }

        headers = {
            "Authorization": f"Bearer {token}",
            "Cache-Control": "no-cache",
        }

        response = make_agileassets_request(
            endpoint, method="get", params=params, headers=headers
        )
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
    assert report_name in REPORTS, f"Report {report_name} not found in config.py"
    report = REPORTS[report_name]

    soda = Socrata(
        SO_WEB,
        SO_TOKEN,
        username=SO_KEY,
        password=SO_SECRET,
        timeout=180,
    )

    logging.info(f"Downloading Report from AgileAssets: {report_name}")
    data = get_report_data(token, report_name, report)

    logging.info(f"Uploading Report to Socrata: {report_name}")
    soda_reply = soda.replace(report["resource_id"], data)
    logging.info(f"Report {report_name} successfully uploaded to Socrata")
    logging.info(f"Socrata Response: {soda_reply}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--report",
        "-r",
        required=True,
        choices=REPORTS.keys(),
        help=f"The name of the report to download. Options: {', '.join(REPORTS.keys())}",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    main(args)
