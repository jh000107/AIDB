from utils import merge_jsonl_files, save_metadata

# lst = ['d', 'o', 'r', 'rd']


# for i in lst:
#     merge_jsonl_files(input_dir=f'../courtlistener/search/{i}', output_file=f'../courtlistener/search/{i}/{i}_merged.jsonl')


lst = []

f = 'hello'
query = 'ai'
type = 'o'
timestamp = 'today'
page_count = 5

save_metadata(lst, f, query, type, timestamp, page_count)

print(lst)
