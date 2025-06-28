import os
import json
import yaml

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

def merge_jsonl_files(input_dir, output_file):
    """
    Merges all .jsonl files in the input directory into a single .jsonl file.

    Args:
        input_dir (str): Path to the directory containing .jsonl files.
        output_file (str): Path to the output merged .jsonl file.
    """
    merged_data = []

    for filename in os.listdir(input_dir):
        if filename.endswith('.jsonl'):
            file_path = os.path.join(input_dir, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        json_obj = json.loads(line)
                        merged_data.append(json_obj)
                    except json.JSONDecodeError as e:
                        print(f"[WARN] Skipping invalid JSON in {filename}: {e}")

    with open(output_file, 'w', encoding='utf-8') as out_f:
        for item in merged_data:
            out_f.write(json.dumps(item) + '\n')

    print(f"[INFO] Merged {len(merged_data)} records into {output_file}")

def load_query_from_yaml(filepath):

    with open(filepath, 'r') as f:
        yaml_config = yaml.safe_load(f)
    
    query = yaml_config.get('query')
    if not query:
        raise ValueError("No 'query' key found in the YAML file.")
    
    return query  