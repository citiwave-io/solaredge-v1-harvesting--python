import json
import csv
import logging
import os
from datetime import datetime

logger = logging.getLogger('my_logger')


def get_start_date_from_filename(filename):
    # Extract the start date from the filename
    start_str = filename.split('/')[-1].split('_')[0]
    return datetime.strptime(start_str, "%Y-%m-%d %H:%M:%S")


def prepare_data_from_json(json_folder):
    all_data = []

    # Get a list of all JSON files in the folder and sort them
    json_files = [f for f in os.listdir(json_folder) if f.endswith('.json')]
    json_files.sort(key=get_start_date_from_filename)

    # Process each JSON file
    for json_file in json_files:
        json_file_path = os.path.join(json_folder, json_file)

        with open(json_file_path, 'r') as file:
            json_data = json.load(file)

            # Process the data as needed, ensuring it's a dictionary
            if isinstance(json_data, dict):
                for meter in json_data.get('powerDetails', {}).get('meters', []):
                    meter_type = meter.get('type', 'Unknown')

                    for entry in meter.get('values', []):
                        date = entry.get('date', '')
                        value = entry.get('value', 0)  # Use default value 0 if not present

                        all_data.append({
                            'date': date,
                            'value': value,
                            'meter_type': meter_type
                        })

    return all_data


def data_to_csv(data, csv_file_path):
    # Check if data is available
    if not data:
        logger.error("No data to write to CSV file.")
        return

    # Writing to CSV
    os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
    with open(csv_file_path, 'w', newline='') as csvfile:
        # Assuming all dictionaries in data have the same keys
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write headers
        writer.writeheader()

        # Write rows
        for row in data:
            writer.writerow(row)

    logger.info(f"Data successfully written to {csv_file_path}")


def json_folder_to_csv(json_folder, csv_folder, site_id):
    json_folder_path = os.path.join(json_folder, site_id, "power-details")
    csv_file_path = os.path.join(csv_folder, site_id, "power-details.csv")
    data = prepare_data_from_json(json_folder_path)
    data_to_csv(data, csv_file_path)

