# SolarEdge v1 harvesting (Python)

## Description
The SolarEdge v1 Harvesting project is a Python-based tool designed to efficiently collect and process solar energy data from SolarEdge inverters.
This script interacts with the SolarEdge Monitoring API to retrieve detailed power and energy data, storing it in a structured format.
The project features functions for fetching data over specific time intervals, converting JSON data to CSV, and ensuring data consistency and accuracy.
Its primary goal is to facilitate solar energy data analysis by streamlining the data acquisition process.

## Getting Started

### Dependencies
- Python 3.6+
- `requests` for API interactions

### Installing
- Clone the repository 
```shell
git clone git@github.com:citiwave-io/solaredge-v1-harvesting--python.git
```
- Go to the repository
```shell
cd solaredge-v1-harvesting--python
```
- Create a virtual environment

```shell
python3 -m venv ./venv
```
- Activate the environment
```shell
source ./venv/bin/activate
```
Install the dependencies
```shell
pip install -r requirements.txt
```

### Executing program
- Ensure you have your SolarEdge site ID and API key.  
- Modify the script parameters with your site ID and API key where indicated.  
- Execute the script from the command line
```shell
python3 your_script_name.py
```

## Documentation
For more information on the SolarEdge API, visit the official [SolarEdge Monitoring Server API](https://knowledge-center.solaredge.com/sites/kc/files/se_monitoring_api.pdf)

## Contributing
Encourage other developers to contribute to your project.
- Briefly explain the process for submitting pull requests.
- Link to the `CONTRIBUTING.md` file if you have detailed contribution guidelines.

## Version History
- 0.0.1
    - Initial Release

## License
This project is licensed under the [GNU GENERAL PUBLIC LICENSE] - see the `LICENSE` file for details

