# MultiCrawl (v0.1.2) 

MultiCrawl is a framework designed for running web measurements with different crawling setups across various machines, enabling near real-time website crawling with browsers like Firefox and Chrome. MultiCrawl also automates interactions with consent banners on websites and recognizes tracking requests. All measurement data is pushed to BigQuery for analysis.

**Supported Browsers**: Chrome, Firefox

**Collectable Data Types**:
- Cookies
- LocalStorage
- Requests
- Responses
- DNS Responses
- Callstacks
- JavaScript calls

## Table of Contents
- [MultiCrawl (v0.1.2)](#multicrawl-v012)
  - [Table of Contents](#table-of-contents)
  - [Getting Started](#getting-started)
  - [Installation \& Configuration](#installation--configuration)
  - [Running the Framework](#running-the-framework)
  - [Acknowledgements](#acknowledgements)

## Getting Started

Before diving into the installation process, ensure you have the prerequisites ready:
- PostgreSQL database
- Authentication JSON for Google Cloud API
- Sites to visit (e.g., Tranco list)
- A VM (e.g., Ubuntu 20.04) setup

## Installation & Configuration

1. Initialize your PostgreSQL database using the `/resources/posgres.sql` script.
2. Update the PostgreSQL connection string in the `/DBOps.py` file.
3. Save your Google Cloud API's `authentication JSON` as `google.json` in `/resources` ([Guide](https://cloud.google.com/docs/authentication/getting-started)).
4. Import your list into the `sites` table of PostgreSQL.
5. Use `/Commander_extract_Subpages.py` to extract subpages from your imported list.
6. Prepare your BigQuery dataset with the tables `requests`, `responses`, `cookies`, and `localstorage`. For column definitions, refer to `resources/bigquery.md`.

## Running the Framework

1. Set up an Ubuntu 20.04 VM.
2. Install the required packages from `/req-pip.txt` and `/req-conda.txt`.
3. Execute `install.sh` for OpenWPM installation.
4. Configure a VPN connection on your VM (if needed).
5. Name your VMs according to the `getMode()` function in `/setup.py`.
6. Adjust the crawling preferences in the `getConfig()` function  in `/setup.py`
7. Execute `restart.sh` on every VM to initiate the measurement.

## Acknowledgements

This repository incorporates files from [OpenWPM](https://github.com/openwpm/OpenWPM), utilizing OpenWPM (v0.20) for Firefox operations.
