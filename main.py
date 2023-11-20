from equipment import download as equipment_downloader
from equipment import transform_to_csv as equipment_transformer
from power import download as power_downloader
from power import transform_to_csv as power_transformer

api_key = ""  # Replace with your actual API key
site_id = ""       # Replace with your actual site ID
inverter_id = ""  # Replace with your actual inverter ID
#max_back_days = 5*365  # 5 years ago
max_back_days = 7*2  # 2 weeks ago

# Get inverter history
# Download raw data (creates multiple json files)
equipment_downloader.fetch_and_save_solar_data(api_key, site_id, inverter_id, max_back_days)
# Transform raw data to csv (creates single file)
equipment_transformer.json_folder_to_csv("./temp", "./data", site_id, inverter_id)


# Get power details
# Download raw data
power_downloader.fetch_power_details(api_key, site_id, max_back_days)
json_folder_path = f"./temp/{site_id}/power-details"
csv_file_path = f"./data/{site_id}/power-details.csv"
data = power_transformer.prepare_data_from_json(json_folder_path)
power_transformer.data_to_csv(data, csv_file_path)
