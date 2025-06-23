import re
import sys
import json
import argparse
from pathlib import Path
from bs4 import BeautifulSoup
from typing import Dict, List
from loguru import logger

# Remove all previous handlers and configure loguru
logger.remove()

logger.add(
    "tele_parser.log",
    level="INFO",
    format=(
        "{time:YYYY-MM-DD HH:mm:ss.SSS} | "
        "{level:<4} | "
        "{function:<17} | "
        "{message}"
    ),
    rotation="10 MB"
)

logger.add(
    sys.stdout,
    level="INFO",
    format=(
        "{time:YYYY-MM-DD HH:mm:ss.SSS} | "
        "{level:<4} | "
        "{function:<17} | "
        "{message}"
    )
)


def find_10d_date_msg(directory: Path, sender_name: str) -> Dict[str, str]:
    pairs = dict()
    for html_file in directory.rglob("*.html"):
        try:
            with html_file.open("r", encoding="utf-8") as f:
                soup = BeautifulSoup(f, "html.parser")
        except Exception as e:
            logger.warning(f"Could not read {html_file}: {e}")
            continue

        for message in soup.find_all("div", class_="message"):
            sender = message.find("div", class_="from_name")
            if sender and sender.text.strip() == sender_name:
                text_div = message.find("div", class_="text")
                text_date = message.find("div", class_="pull_right date details")
                if text_div and text_date:
                    numbers = re.findall(r"\b\d{10}\b", str(text_div))
                    dates = re.findall(r"\b\d{2}\.\d{2}\.\d{4}\b", str(text_date))
                    if numbers and dates:
                        pairs[numbers[0]] = dates[0]
        logger.info(f"Processed: {html_file}, entries: {len(pairs)}")
    return pairs


def get_all_chat_users(directory: Path) -> List[str]:
    users = set()
    for html_file in directory.rglob("*.html"):
        try:
            with html_file.open("r", encoding="utf-8") as f:
                soup = BeautifulSoup(f, "html.parser")
        except Exception as e:
            logger.warning(f"Could not read {html_file}: {e}")
            continue

        for message in soup.find_all("div", class_="message"):
            sender = message.find("div", class_="from_name")
            if sender:
                users.add(sender.text.strip())

    logger.info(f"Found {len(users)} unique senders")
    return sorted(users)


def save_dict_tsv(data: Dict[str, str], output_file: Path):
    try:
        with output_file.open("w", encoding="utf-8") as f:
            f.write("ID\tDate\n")
            for key, val in data.items():
                f.write(f"{key}\t{val}\n")
        logger.info(f"Saved TSV: {output_file}")
    except Exception as e:
        logger.error(f"Error saving TSV {output_file}: {e}")


def save_dict_json(data: Dict[str, str], output_file: Path):
    try:
        with output_file.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved JSON: {output_file}")
    except Exception as e:
        logger.error(f"Error saving JSON {output_file}: {e}")


def export_all_users(directory: Path, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    users = get_all_chat_users(directory)
    for user in users:
        logger.info(f"Extracting data for user: {user}")
        data = find_10d_date_msg(directory, user)
        filename_base = user.replace(" ", "_")
        save_dict_tsv(data, output_dir / f"{filename_base}.tsv")
        save_dict_json(data, output_dir / f"{filename_base}.json")


def main():
    parser = argparse.ArgumentParser(description="Parse Telegram HTML exports for 10-digit IDs and dates.")
    parser.add_argument("--input", type=Path, required=True, help="Directory with Telegram HTML exports")
    parser.add_argument("--output", type=Path, required=True, help="Directory to save extracted TSV/JSON")

    args = parser.parse_args()
    export_all_users(args.input, args.output)


if __name__ == "__main__":
    main()
