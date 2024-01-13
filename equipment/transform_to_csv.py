import json
import csv
import os
import logging
from datetime import datetime

logger = logging.getLogger('my_logger')


def flatten_data(data_entry):
    # Flatten the nested L1Data, L2Data, and L3Data
    for key in ['L1Data', 'L2Data', 'L3Data']:
        if key in data_entry:
            for subkey, value in data_entry[key].items():
                data_entry[f'{key}_{subkey}'] = value
            del data_entry[key]
    return data_entry


def get_start_date_from_filename(filename):
    # Extract the start date from the filename
    start_str = filename.split('/')[-1].split('_')[0]
    return datetime.strptime(start_str, "%Y-%m-%d %H:%M:%S")


def json_folder_to_csv(json_folder, csv_folder, site_id, inverter_id):
    # Construct file paths
    json_folder_path = os.path.join(json_folder, site_id, 'inverters', inverter_id)
    csv_file_path = os.path.join(csv_folder, site_id, 'inverters', inverter_id, 'output.csv')

    # Get a list of all files in the JSON folder that end with '.json'
    json_files = [f for f in os.listdir(json_folder_path) if f.endswith('.json')]

    # Sort the files based on the start date in the filename
    json_files.sort(key=get_start_date_from_filename)

    # Check if there is at least one JSON file
    if not json_files:
        logger.error("No JSON files found in the folder.")
        return

    # Create an empty list to hold the data and a set for all field names
    all_data = []
    all_fieldnames = set()

    # Read data from each JSON file and add it to the list
    for json_file in json_files:
        json_file_path = os.path.join(json_folder_path, json_file)
        with open(json_file_path, 'r') as f:
            json_data = json.load(f)
            data = json_data.get('data', {}).get('telemetries', [])
            if data:
                # Flatten and add each data entry
                for entry in data:
                    flattened_entry = flatten_data(entry)
                    all_data.append(flattened_entry)
                    # Update fieldnames with the keys from this entry
                    all_fieldnames.update(flattened_entry.keys())

    # Check if there is data to write
    if all_data:
        # Convert the set of fieldnames to a list
        fieldnames = list(all_fieldnames)

        # Create the directory if it does not exist
        os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)

        with open(csv_file_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write CSV file headers
            writer.writeheader()

            # Write data from JSON to CSV file
            for row in all_data:
                writer.writerow(row)

        logger.info(f"Data from {len(json_files)} JSON files has been successfully written to {csv_file_path}.")
    else:
        logger.error("No data to write to CSV file.")
