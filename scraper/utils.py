import os
import json

def update_api_key(api_key, env_path='.env'):
    """
    Update the COURTLISTENER_API_KEY in the .env file.
    
    Args:
        api_key (str): The new API key to set.
        env_path (str): Path to the .env file.
    """
    key_line = f"COURTLISTENER_API_KEY={api_key}\n"
    updated = False

    # If the .env file does not exist, create it
    if not os.path.exists(env_path):
        with open(env_path, 'w') as f:
            f.write(key_line)
        return

    # Otherwise, read and update
    with open(env_path, 'r') as f:
        lines = f.readlines()

    with open(env_path, 'w') as f:
        for line in lines:
            if line.startswith('COURTLISTENER_API_KEY='):
                f.write(key_line)
                updated = True
            else:
                f.write(line)

        # If key not found, append it at the end
        if not updated:
            f.write(key_line)

def save_data_jsonl(data, filepath):
    """Append each item in the results list as a separate line in a .jsonl file."""
    with open(filepath, 'a') as file:
        for record in data.get('results', []):
            json.dump(record, file)
            file.write('\n')

def load_log_file(filepath):
    try:
        with open(filepath, 'r') as f:
            return set(line.strip() for line in f.readlines())
    except FileNotFoundError:
        return set()

def append_to_log(filepath, line):
    with open(filepath, "a") as f:
        f.write(f"{line}\n")