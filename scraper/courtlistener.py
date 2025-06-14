import os
import argparse
import requests
import json
import datetime
from dotenv import load_dotenv

load_dotenv()

CONFIG = {
    "API_KEY": os.getenv("COURTLISTENER_API_KEY"),
    "BASE_URL": 'https://www.courtlistener.com/api/rest/v4/search/'
}

def save_data_jsonl(data, filepath):
    """Append each item in the results list as a separate line in a .jsonl file."""
    with open(filepath, 'a') as file:
        for record in data.get('results', []):
            json.dump(record, file)
            file.write('\n')

def main():
    parser = argparse.ArgumentParser(description="CourtListener API CLI")
    parser.add_argument('--api_key', type=str, help='CourtListener API Key (overrides .env)')
    parser.add_argument('--query', type=str, required=True, help='Search query string')
    parser.add_argument('--type', type=str, choices=['o', 'r', 'rd', 'd', 'p'], default='o', help='Type of search: o (Case law opinion clusters with nested Opinion documents), r (List of Federal cases (dockets) with up to three nested documents), rd (Federal filing documents from PACER), d (	Federal cases (dockets) from PACER), p (Judges)')
    parser.add_argument('--output_dir', type=str, default='.', help='Output directory for saving the data')

    args = parser.parse_args()

    api_key = args.api_key if args.api_key else CONFIG['API_KEY']
    if not api_key:
        raise ValueError("No API key provided. Use --api_key argument or set COURTLISTENER_API_KEY in .env")

    query = args.query
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

    while more_pages:
        print(f"Fetching page {page_count}...")

        if next_url == CONFIG['BASE_URL']:
            response = requests.get(next_url, headers=headers, params=params)
        else:
            response = requests.get(next_url, headers=headers)

        if response.status_code == 200:
            data = response.json()

            
            output_filename = f"{today}_courtlistener_search_{query.replace(' ', '-')}_page_{page_count}.jsonl"
            output_filepath = os.path.join(args.output_dir, output_filename)

            save_data_jsonl(data, output_filepath)

            next_url = data.get('next')
            if next_url:
                page_count += 1
            else:
                more_pages = False
                print("All pages fetched.")
        else:
            print(f"Error fetching page {page_count}: {response.status_code} - {response.text}")
            more_pages = False

if __name__ == "__main__":
    main()
