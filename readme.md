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

Also, if you are looking to eventually upload this report to [Socrata](https://dev.socrata.com/) set up a dataset and 
supply its resource ID in `config.py`.

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
1. Make a python environment and install the required packages, `pip install -r requirements.txt` (or see Docker instructions below)
2. Supply your created `.env` file and run `python request_client.py`
3. Make note of the Client ID and Client Secret printed to the command line in your `.env` file. 
By default, the script will make your Client ID `API_VIEWER`

### etl/report_to_socrata.py

This script will download the desired report from AgileAssets and upload it to a Socrata dataset. The selected report must
be first configured in `etl/config.py`, then passed via a command line argument using `--report` or `-r`.

As an example, this command will download (then upload to socrata) the `VW_UPDATED_PROJECTS_SEGMENTS` report:

```console
python etl/report_to_socrata.py --report VW_UPDATED_PROJECTS_SEGMENTS
```

## Docker

The github actions associated with this repository will build a docker image and upload it to our dockerhub account.

The image can be pulled using the following command:
```console
docker pull atddocker/dts-pavement-ops-reporting:production
```

Or, if you would like to build it locally:
```console
docker build . -t atddocker/dts-pavement-ops-reporting:local
```

And, running commands locally:
```console
docker run --env-file .env.prod -it atddocker/dts-pavement-ops-reporting:local /bin/bash
```

Then, inside of the container, as an example:
```console
python etl/report_to_socrata.py --report VW_UPDATED_PROJECTS_SEGMENTS
```

