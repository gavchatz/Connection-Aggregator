
# Telegram HTML Export Parser

This script processes Telegram HTML export files to extract specific user message patterns—namely 10-digit numeric IDs paired with dates—and outputs the data into TSV files. It also provides helper utilities to explore users in the export and structure the data cleanly.

## Features

* Extracts messages with **10-digit numbers** and **dates** from HTML exports.
* Filters by sender name.
* Outputs data as TSV or prettified dictionaries.
* Lists all users present in the Telegram export.
* Supports interactive session using `telethon` to view available chats.

## Requirements

(Python 3.7+)

### Python libraries
-re
-os
-json
-datetime
-bs4
-telethon


## Installation
### Windows 
```cmd
setx TG_API_ID your_api_id_value /M
setx TG_API_HASH your_api_hash_value /M
```
### Linux
```bash
export TG_API_ID=your_api_id
export TG_API_HASH=your_api_hash
```
 
## Usage

## Output

## Functions Overview

## Notes
