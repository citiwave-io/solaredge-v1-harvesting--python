from equipment import download as equipment_downloader
from equipment import transform_to_csv as equipment_transformer
from power import download as power_downloader
from power import transform_to_csv as power_transformer

api_key = "API_KEY"  # Replace with your actual API key
site_id = "123456"       # Replace with your actual site ID
inverter_id = "ABCDEFGH-01"  # Replace with your actual inverter ID
#max_back_days = 5*365  # 5 years ago
max_back_days = 7*2  # 2 weeks ago

# Get inverter history
# Download raw data (creates multiple json files)
equipment_downloader.fetch_and_save_solar_data(api_key, site_id, inverter_id, max_back_days)
# Transform raw data to csv (creates single file)
equipment_transformer.json_folder_to_csv("./temp", "./data", site_id, inverter_id)


# Get power details
# Download raw data (creates multiple json files)
power_downloader.fetch_power_details(api_key, site_id, max_back_days)
# Transform raw data to csv (creates single file)
power_transformer.json_folder_to_csv("./temp", "./data", site_id)
