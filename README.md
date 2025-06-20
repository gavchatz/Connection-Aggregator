
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
*re
*os
*json
*datetime
*bs4
*telethon


## Installation
 Windows ...

```bash
export TG_API_ID=your_api_id
export TG_API_HASH=your_api_hash
```
 
## Usage

1. **Prepare environment variables** (for Telethon session):

```bash
export TG_API_ID=your_api_id
export TG_API_HASH=your_api_hash
```

2. **Place Telegram HTML exports** in a subdirectory named: `energopoihseiw_export/`

3. **Run the script**:

```bash
python your_script.py
```

Uncomment the function calls in `__main__` to:

* Export 10-digit numbers with dates per user
* Print chat names using Telethon

## Output

* Per-user `.tsv` files like `John_Doe.tsv`
* Each file contains:

  ```
  10ψήφιος    Ημερομηνία
  1234567890  01.01.2024
  ```

## Functions Overview

* `find_10d_date_msg(dir, sender)` — Extracts 10-digit numbers with dates from sender's messages.
* `get_all_chat_users(dir)` — Lists unique senders from HTML files.
* `print_user_connection_tsv(dir)` — Generates TSVs for each sender.
* `sexy_dict_print(dict, path)` — Saves a dictionary in pretty JSON-like format.
* `excel_tsv_print(dict, path)` — Saves a dictionary as a tab-separated file.

## Notes

* The `export_connections()` function is a placeholder.
* `read_dict_from_json()` and `read_in_list()` support reuse for external input/output.

---

Let me know if you want this translated or tailored for a GitHub release.
