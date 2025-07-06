import os
import argparse
import requests
import datetime
import time
import json

from utils import update_api_key, save_data_jsonl, load_log_file, append_to_log, load_query_from_yaml
from dotenv import load_dotenv
load_dotenv()
  



def main():
    parser = argparse.ArgumentParser(description="CourtListener API CLI")
    parser.add_argument('--mode', type=str, choices=['dev', 'prod'], default='dev', help='Mode of operation: dev (development) or prod (production)')
    parser.add_argument('--api_key', type=str, required=True, help='CourtListener API Key (overrides .env)')
    parser.add_argument('--env_path', type=str, default='.env', help='Path to the .env file (default: .env)')
    parser.add_argument('--type', type=str, choices=['o', 'r', 'rd', 'd', 'p'], default='o', help='Type of search: o (Case law opinion clusters with nested Opinion documents), r (List of Federal cases (dockets) with up to three nested documents), rd (Federal filing documents from PACER), d (	Federal cases (dockets) from PACER), p (Judges)')
    parser.add_argument('--output_dir', type=str, default='.', help='Output directory for saving the data')

    args = parser.parse_args()

    update_api_key(api_key=args.api_key, env_path=args.env_path)

    

    CONFIG = {
        "API_KEY": os.getenv("COURTLISTENER_API_KEY"),
        "BASE_URL": 'https://www.courtlistener.com/api/rest/v4/search/',
        "METADATA_FILEPATH": '../metadata.jsonl'
    }

    # Ensure output directory exists
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    ERROR_LOG_PATH = os.path.join(args.output_dir, 'error_log.txt')

    api_key = CONFIG['API_KEY']

    if not api_key:
        raise ValueError("No API key provided. Use --api_key argument or set COURTLISTENER_API_KEY in .env")

    if args.mode == 'dev':
        query = f"({load_query_from_yaml('./config.yml')}) AND dateFiled:[2025-04-30 TO *]"
    else:
        print("🔍 Enter search terms one by one. Type DONE when finished.")
        terms = []
        while True:
            term = input("Enter a keyword: ").strip()
            if term.upper() == 'DONE':
                break
            if term:
                if " " in term:
                    term = f'"{term}"'
                terms.append(term)
        
        if not terms:
            raise ValueError("No search terms provided. Please enter at least one term.")
    
        query = " OR ".join(terms)

        print(f"[INTERACTIVE MODE] Final query: {query}")

    type = args.type
    
    headers = {
        'Authorization': f'Token {api_key}'
    }

    params = {
        'q': query,
        'type': type,
    }

    today = datetime.date.today().strftime('%Y-%m-%d')

    next_url = CONFIG['BASE_URL']
    more_pages = True
    page_count = 1
    retries = 0

    while more_pages:
        print(f"Fetching page {page_count}...")

        if next_url == CONFIG['BASE_URL']:
            response = requests.get(next_url, headers=headers, params=params)
        else:
            response = requests.get(next_url, headers=headers)

        if response.status_code == 200:
            retries = 0
            data = response.json()
            
            output_filename = f"{today}_courtlistener_search_type-{type}_page_{page_count}.jsonl"
            output_filepath = os.path.join(args.output_dir, output_filename)

            save_data_jsonl(data, output_filepath)

            # save metadata

            record = {
                "file": output_filename,
                "query": query,
                "type": type,
                "timestamp": today,
                "page": page_count,
                "next_page": data.get('next')
            }

            with open(CONFIG['METADATA_FILEPATH'], 'a') as meta_f:
                json.dump(record, meta_f)
                meta_f.write('\n')

            next_url = data.get('next')
            if next_url:
                page_count += 1
            else:
                more_pages = False
                print("All pages fetched.")
        else:
            if retries >= 3:
                print("Max retries reached. Exiting.")
                break
            
            print(f"Error fetching page {page_count}: {response.status_code} - {response.text}")
            append_to_log(ERROR_LOG_PATH, f"{page_count} | {next_url} | {response.status_code}")

            # Sleep to avoid hitting API rate limits
            time.sleep(5)
            retries += 1



if __name__ == "__main__":
    main()
