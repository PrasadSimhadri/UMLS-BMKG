# build_nodes.py
import csv
import argparse
from collections import defaultdict

def build_nodes(mrconso_path, mrsty_path, out_csv):
    # Collect preferred names, synonyms, sources, codes
    names = defaultdict(set)
    sources = defaultdict(set)
    codes = defaultdict(set)
    preferred = {}

    with open(mrconso_path, 'r', encoding='utf-8', errors='ignore') as f:
        for i, line in enumerate(f):
            parts = line.rstrip('\n').split('|')
            if len(parts) < 15:
                continue
            cui = parts[0]
            lat = parts[1]
            ts = parts[2]
            str_name = parts[14]
            sab = parts[11]
            code = parts[13]

            if lat != 'ENG': 
                continue
            names[cui].add(str_name)
            sources[cui].add(sab)
            codes[cui].add(code)
            if ts == 'P':  # preferred term
                preferred[cui] = str_name

            if i and i % 5_000_000 == 0:
                print(f"Processed {i} MRCONSO lines...")

    # Collect semantic types
    semantic_types = defaultdict(set)
    with open(mrsty_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            parts = line.rstrip('\n').split('|')
            if len(parts) < 4:
                continue
            cui = parts[0]
            sty = parts[3]
            semantic_types[cui].add(sty)

    # Write output
    with open(out_csv, 'w', newline='', encoding='utf-8') as f_out:
        writer = csv.writer(f_out)
        writer.writerow(['cui', 'preferred_name', 'semantic_types', 'synonyms', 'sources', 'codes'])
        for cui in names:
            writer.writerow([
                cui,
                preferred.get(cui, next(iter(names[cui]))),
                ';'.join(sorted(semantic_types.get(cui, []))),
                ';'.join(sorted(names[cui])),
                ';'.join(sorted(sources[cui])),
                ';'.join(sorted(codes[cui]))
            ])

    print(f"Wrote nodes to {out_csv}")


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--mrconso', required=True, help='path to MRCONSO.RRF')
    ap.add_argument('--mrsty', required=True, help='path to MRSTY.RRF')
    ap.add_argument('--out', default='nodes.csv', help='output CSV for nodes')
    args = ap.parse_args()

    build_nodes(args.mrconso, args.mrsty, args.out)
