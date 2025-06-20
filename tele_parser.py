import re, os, json, datetime
from bs4 import BeautifulSoup
from telethon import TelegramClient
from telethon.sessions import StringSession



def export_connections(api_id,api_hash):
    print(api_id,api_hash)

def find_10d_date_msg(directory, sender_name):
    pairs = dict()
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith(".html"):
                full_path = os.path.join(dirpath, filename)
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        soup = BeautifulSoup(f, "html.parser")
                except (IOError, OSError) as e:
                    print(f"Error opening file {full_path}: {e}")
                    continue

                messages = soup.find_all("div", class_="message")
                for message in messages:
                    sender = message.find("div", class_="from_name")
                    if sender and sender.text.strip() == sender_name:
                        text_div = message.find("div", class_="text")
                        text_date = message.find(
                            "div", class_="pull_right date details"
                        )
                        if text_date and text_div:
                            numbers = re.findall(r"\b\d{10}\b", str(text_div))
                            date_pattern = r"\b\d{2}\.\d{2}\.\d{4}\b"
                            msg_date = re.findall(date_pattern, str(text_date))
                            if numbers and msg_date and len(str(text_div)) > 6:
                                pairs[numbers[0]] = msg_date[0]
                print(f"Processed file: {full_path}, pairs count: {len(pairs)}")
    return pairs


def read_in_list(columnfile):
    try:
        with open(columnfile, "r", encoding="utf-8") as f:
            lines = f.readlines()
        return lines
    except (IOError, OSError) as e:
        print(f"Error reading file {columnfile}: {e}")
        return []


def sexy_dict_print(ugly_dict, pretty_dirname):
    try:
        max_key_len = max(len(k) for k in ugly_dict) if ugly_dict else 0
        with open(pretty_dirname, "w", encoding="utf-8") as f:
            f.write("{\n")
            for i, (k, v) in enumerate(ugly_dict.items()):
                comma = "," if i < len(ugly_dict) - 1 else ""
                f.write(f'  "{k}"{" " * (max_key_len - len(k))} : {v}{comma}\n')
            f.write("}\n")
    except Exception as e:
        print(f"Error writing to file {pretty_dirname}: {e}")


def excel_tsv_print(ugly_dict, fname):
    try:
        with open(fname, "w", encoding="utf-8") as f:
            f.write("10ψήφιος\tΗμερομηνία\n")
            for k, v in ugly_dict.items():
                f.write(f"{k}\t{v}\n")
    except Exception as e:
        print(f"Error writing TSV file {fname}: {e}")


def read_dict_from_json(json_fname):
    try:
        with open(json_fname, encoding="utf-8") as f:
            new_data = json.load(f)
        return new_data
    except FileNotFoundError:
        print(f"JSON file not found: {json_fname}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in {json_fname}: {e}")
    except Exception as e:
        print(f"Error reading JSON file {json_fname}: {e}")
    return {}


def get_all_chat_users(directory):
    list_of_users = []
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith(".html"):
                full_path = os.path.join(dirpath, filename)
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        soup = BeautifulSoup(f, "html.parser")
                except (IOError, OSError) as e:
                    print(f"Error opening file {full_path}: {e}")
                    continue

                messages = soup.find_all("div", class_="message")
                for message in messages:
                    sender = message.find("div", class_="from_name")
                    if sender:
                        sender_text = sender.text.strip()
                        if sender_text not in list_of_users:
                            list_of_users.append(sender_text)
    print(f"Found {len(list_of_users)} senders:")
    print(list_of_users)
    return list_of_users


def print_user_connection_tsv(connection_export_directory):

    userlist = get_all_chat_users(connection_export_directory)
    for name in userlist:
        print(f"Processing user: {name}")
        connections = find_10d_date_msg(connection_export_directory, name)
        print(f"Number of entries for {name}: {len(connections)}")
        excel_tsv_print(connections, name.replace(" ", "_") + ".tsv")

def export_telegram_energopoihseis():

    with TelegramClient(StringSession(), os.getenv("TG_API_ID"), os.getenv("TG_API_HASH")) as client:

        print("✅ Login successful!")

        for dialog in client.iter_dialogs():
            print(dialog.name)



if __name__ == "__main__":
    

    connection_export_directory = os.getcwd()+"/energopoihseiw_export"    
    
    export_connections(int(os.getenv("TG_API_ID")),os.getenv("TG_API_HASH"))
    
    print_user_connection_tsv(connection_export_directory)

