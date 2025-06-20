from utils import merge_jsonl_files

lst = ['d', 'o', 'r', 'rd']


for i in lst:
    merge_jsonl_files(input_dir=f'../courtlistener/search/{i}', output_file=f'../courtlistener/search/{i}/{i}_merged.jsonl')



