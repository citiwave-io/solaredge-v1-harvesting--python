import logging

import requests
import os
import json
from datetime import datetime, timedelta

logger = logging.getLogger('my_logger')


def save_json(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        json.dump(data, f)


def fetch_power_details(api_key, site_id, max_back_days=14, time_unit="QUARTER_OF_AN_HOUR"):
    base_url = "https://monitoringapi.solaredge.com/site/{}/powerDetails"
    max_back_date = datetime.now() - timedelta(days=max_back_days)  # Default 5 years ago

    # Starting from the current week
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)

    start_str = start_date.strftime("%Y-%m-%d %H:%M:%S")
    end_str = max_back_date.strftime("%Y-%m-%d %H:%M:%S")

    logger.info("Started downloading power details from %s to %s", start_str, end_str)

    while start_date > max_back_date:
        # Format dates
        start_str = start_date.strftime("%Y-%m-%d %H:%M:%S")
        end_str = end_date.strftime("%Y-%m-%d %H:%M:%S")

        # Define URL and parameters
        url = base_url.format(site_id)
        params = {
            'startTime': start_str,
            'endTime': end_str,
            'time_unit': time_unit,
            'api_key': api_key
        }

        # Make the GET request
        response = requests.get(url, params=params)

        # Check for successful response or rate limiting
        if response.status_code == 200:
            data = response.json()
            if len(data.get('powerDetails', []).get('meters', [])) == 0:
                logger.warning("No data from %s to $s. Stopping the process", start_str, end_str)
                break

            # Save the response in a JSON file
            filename = f"./temp/{site_id}/power-details/{start_str}_{end_str}.json"
            save_json(data, filename)
        elif response.status_code == 429:
            logger.error("Rate limit reached, please try again later. Can't download data from %s to $s", start_str, end_str)
            break
        else:
            logger.error("Error: %s - %s. Can't download data from %s to %s",
                         response.status_code, response.text,
                         start_str, end_str)

        # Move to the previous week
        end_date = start_date
        start_date = start_date - timedelta(days=7)

    logger.info("Finished downloading data")
