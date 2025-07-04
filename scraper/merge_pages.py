import argparse
from utils import merge_jsonl_files

def main():
    parser = argparse.ArgumentParser(description="Merge JSONL files from CourtListener search directories")
    parser.add_argument('--type', type=str, choices=['o', 'r', 'rd', 'd', 'p', 'test'], default='o', help='Type of search: o (Case law opinion clusters with nested Opinion documents), r (List of Federal cases (dockets) with up to three nested documents), rd (Federal filing documents from PACER), d (	Federal cases (dockets) from PACER), p (Judges)')

    args = parser.parse_args()

    merge_jsonl_files(input_dir=f'../courtlistener/search/{args.type}', output_file=f'../courtlistener/search/{args.type}/{args.type}_merged.jsonl')


if __name__ == "__main__":
    main()