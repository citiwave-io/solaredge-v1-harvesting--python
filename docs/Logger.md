# Logger

## Overview
The SolarEdge v1 Harvesting project now includes an enhanced feature: the "Logger". This addition significantly improves the script's robustness and usability by providing detailed logging capabilities during the data harvesting process.

## Functionality
The Logger is specifically designed to track and record any errors encountered during data harvesting. This includes, but is not limited to, issues such as:

**No Data Found**: Occurs when the script attempts to fetch data for a particular interval or inverter but finds no records.
**API Call Limits**: Triggers when the script reaches the API call limits set by SolarEdge, ensuring users are aware of any potential downtime or data gaps.
**Inverter-Specific Errors**: Captures and logs any errors or issues encountered when retrieving data from a specific inverter. This is crucial for pinpointing problems related to individual hardware units.

## Log File
All errors and incidents are logged into a dedicated file. This file is structured to allow for easy review and analysis after a harvesting job is complete. The log entries include timestamps and detailed descriptions of each incident, providing a comprehensive overview of any issues encountered.