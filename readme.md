# dts-pavement-ops-reporting

Scripts for automatically downloading reports from the pavement management information system (PMIS) used by the City of Austin 
Transportation Public Works. The vendor's platform is called AgileAssets.

## Usage

### User Privileges

Have an account created for you in AgileAssets with admin privileges. 

### API Configuration

Add the desired report name to the list of allowed API reports under:
```
Home System > Utilities > Allowed Web API Views 
```

### AgileAssets Credentials

Copy the provided template (`.env.template`) as `.env` and populate your username and password, 
along with the base url of your agileassets instance.

```
# Base URL of the agileassets instance
BASE_URL= 

# Account with Admin privileges required
USERNAME= your_agileassets_username
PASSWORD= your_agileassets_password
```

### Request Client ID and Secret

[Official Documentation](https://docs.agileassets.com/display/PD10/REST+API+V2+Security)
1. Make a python environment and install the required packages, `pip install -r requirements.txt`
2. Supply your created `.env` file and run `python request_client.py`
3. Make note of the Client ID and Client Secret in your `.env` file. By default, the script will make your Client ID `API_VIEWER`
