# build_edges.py
import csv
import argparse
import sys

csv.field_size_limit(10_000_000)

def load_allowed_cuis(nodes_csv):

    allowed = set()
    with open(nodes_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            allowed.add(row['cui'])
    return allowed

def normalize_relation(rel, rela):
    text = ((rela or '') + ' ' + (rel or '')).lower()
    if 'treat' in text or 'therapy' in text or 'may_treat' in text:
        return 'TREATS'
    if 'prevent' in text or 'prophyl' in text:
        return 'PREVENTS'
    if 'cause' in text:
        return 'CAUSES'
    if 'interact' in text:
        return 'INTERACTS_WITH'
    if 'contraindicat' in text:
        return 'CONTRAINDICATED_WITH'
    if 'associate' in text or 'complic' in text or 'related' in text:
        return 'ASSOCIATED_WITH'
    # fallback to bare REL (e.g., RN, RO) or generic
    if rel:
        return rel
    return 'RELATED_TO'

def build_edges(mrrel_path, nodes_csv, out_csv):
    allowed = load_allowed_cuis(nodes_csv)
    print(f"Loaded {len(allowed)} allowed CUIs from {nodes_csv}")
    # MRREL standard indices (stream parsing)
    # columns: CUI1|AUI1|STYPE1|REL|CUI2|AUI2|STYPE2|RELA|RUI|SRUI|SAB|SL
    with open(mrrel_path, 'r', encoding='utf-8', errors='ignore') as f_in, \
         open(out_csv, 'w', newline='', encoding='utf-8') as f_out:
        writer = csv.writer(f_out)
        writer.writerow(['source','target','relation','raw_relation','source_vocab'])
        for i, line in enumerate(f_in):
            parts = line.rstrip('\n').split('|')
            if len(parts) < 5:
                continue
            c1 = parts[0]
            rel = parts[3] if len(parts) > 3 else ''
            c2 = parts[4]
            rela = parts[7] if len(parts) > 7 else ''
            sab = parts[10] if len(parts) > 10 else ''
            if c1 not in allowed or c2 not in allowed:
                continue
            norm = normalize_relation(rel, rela)
            writer.writerow([c1, c2, norm, rela if rela else rel, sab])
            if i and i % 5_000_000 == 0:
                print(f"Processed {i} MRREL lines...")

    print(f"Wrote edges to {out_csv}")

if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--mrrel', required=True, help='path to MRREL.RRF')
    ap.add_argument('--nodes', required=True, help='nodes.csv produced earlier')
    ap.add_argument('--out', default='edges.csv', help='output CSV for edges')
    args = ap.parse_args()

    build_edges(args.mrrel, args.nodes, args.out)
