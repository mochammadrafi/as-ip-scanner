# AS Number IP Scanner

This repository contains a Python script that retrieves all IP addresses in the netblocks of a given AS number and scans the web services running on those IP addresses. It utilizes the RIPE Stat API to fetch the announced prefixes for the specified AS number and then generates a list of IP addresses within those netblocks.

The script makes use of the `requests` library to send HTTP requests to each IP address and port combination, checking if a web service is running. Additionally, it extracts the domain name associated with each IP address using reverse DNS lookup.

## Usage

1. Specify the AS number as a command-line argument when running the script.
2. The script will retrieve all IP addresses in the netblocks of the specified AS number and save them to `ips.txt`.
3. It will then scan the web services running on those IP addresses and print the results to the console.
4. Any open ports will be logged to `open_ports.txt` along with the associated domain names.

## Dependencies

- Python 3.x
- `requests` library

## License

This project is licensed under the [MIT License](https://github.com/mochammad/rafi/as-ip-scanner/blob/main/LICENSE).
