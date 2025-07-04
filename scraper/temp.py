import os
import json



input_dir = f'../courtlistener/search/test'
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
            cluster_id = record.get('cluster_id')
            absolute_url = record.get('absolute_url')



            

        except json.JSONDecodeError:
            continue

print(data)
