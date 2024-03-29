import requests
import os
import json
import logging
from datetime import datetime, timedelta

logger = logging.getLogger('my_logger')


def save_json(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        json.dump(data, f)


def fetch_and_save_solar_data(api_key, site_id, inverter_id, max_back_days=14):
    base_url = "https://monitoringapi.solaredge.com/equipment/{}/{}/data"
    max_back_date = datetime.now() - timedelta(days=max_back_days)

    # Starting from the current week
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)

    start_str = max_back_date.strftime("%Y-%m-%d %H:%M:%S")
    end_str = end_date.strftime("%Y-%m-%d %H:%M:%S")

    logger.info("Started downloading data for inverter %s. Range between %s and %s",
                inverter_id, start_str, end_str)

    while start_date > max_back_date:
        # Format dates
        start_str = start_date.strftime("%Y-%m-%d %H:%M:%S")
        end_str = end_date.strftime("%Y-%m-%d %H:%M:%S")

        # Define URL and parameters
        url = base_url.format(site_id, inverter_id)
        params = {
            'startTime': start_str,
            'endTime': end_str,
            'api_key': api_key
        }

        # Make the GET request
        response = requests.get(url, params=params)

        # Check for successful response or rate limiting
        if response.status_code == 200:
            data = response.json()
            if data.get('data', {}).get('count', 0) == 0:
                logger.warning("No data from %s to %s for inverter %s. Stopping the process",
                               start_str, end_str, inverter_id)
                break

            # Save the response in a JSON file
            filename = f"./temp/{site_id}/inverters/{inverter_id}/{start_str}_{end_str}.json"
            save_json(data, filename)
            logger.info("Data for inverter %s from %s to %s successfully downloaded", inverter_id, start_str,
                        end_str)
        elif response.status_code == 429:
            logger.error("Rate limit reached, please try again later. "
                         "Can't download data from %s to %s for inverter %s",
                         start_str, end_str, inverter_id)
            break
        else:
            logger.error("Error: %s - %s. Can't download data from %s to %s for inverter %s",
                         response.status_code, response.text,
                         start_str, end_str, inverter_id)

        # Move to the previous week
        end_date = start_date
        start_date = start_date - timedelta(days=7)

    logger.info("Finished downloading data for inverter %s", inverter_id)
