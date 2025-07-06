import requests
import argparse
import os
import json

type_field_mapper = {
    'o': 'absolute_url',
    'test': 'opinions'
}

CONFIG = {
    "BASE_URL": "https://www.courtlistener.com",   
}

def load_data(type):
    input_dir = f'../courtlistener/search/{type}'
    # Load data from the specified directory
    
    file = None
    for filename in os.listdir(input_dir):
        if filename.endswith('merged.jsonl'):
            file = os.path.join(input_dir, filename)
            break
    
    if not file:
        raise FileNotFoundError(f"No merged file found in {input_dir}")
    
    data = []

    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                record = json.loads(line)
                data.append(record)
            except json.JSONDecodeError:
                continue

    return data

def download_pdfs(data):

    output_dir_base = f'../pdfs'

    for case in data:
        try:
            opinions = case.get('opinions')
            cluster_id = str(case.get('cluster_id'))

            output_dir = os.path.join(output_dir_base, cluster_id)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)

            for opinion in opinions:
                download_url = opinion.get('download_url')
                opinion_id = opinion.get('id')

                if download_url:
                    response = requests.get(download_url)
                    if response.status_code == 200:
                        with open(os.path.join(output_dir, f"{opinion_id}.pdf"), 'wb') as f:
                            f.write(response.content)
                        print(f"Downloaded {opinion_id} to {output_dir}")
                    else:
                        print(f"Failed to download: {response.status_code}")

                # fallback to absolute_url if download_url is not available
                # else:
        except Exception as e:
            print(f"Error processing case: {e}")
            continue

    
def main():
    parser = argparse.ArgumentParser(description="Download content from CourtListener")
    parser.add_argument('--type', type=str, choices=['o', 'r', 'rd', 'd', 'p', 'test'], default='o', help='Type of search: o (Case law opinion clusters with nested Opinion documents), r (List of Federal cases (dockets) with up to three nested documents), rd (Federal filing documents from PACER), d (	Federal cases (dockets) from PACER), p (Judges)')

    args = parser.parse_args()


    print(f"Configuration: {CONFIG}")

    data = load_data(args.type)
    download_pdfs(data)

if __name__ == "__main__":
    main()