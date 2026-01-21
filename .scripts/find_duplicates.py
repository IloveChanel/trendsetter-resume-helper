import os
import hashlib
import json

# Configure root and excluded dirs
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
EXCLUDE_DIRS = {
    'venv', '.venv', '.git', 'node_modules', '__pycache__', '.next', 'dist', 'build', 'env'
}

hash_map = {}

for dirpath, dirnames, filenames in os.walk(ROOT):
    # Filter out excluded directories
    dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]

    for fname in filenames:
        # skip the script itself
        if os.path.abspath(__file__) == os.path.join(dirpath, fname):
            continue
        fpath = os.path.join(dirpath, fname)
        # skip if in excluded path
        if any(part in EXCLUDE_DIRS for part in fpath.split(os.sep)):
            continue
        try:
            with open(fpath, 'rb') as f:
                h = hashlib.sha256()
                while True:
                    chunk = f.read(8192)
                    if not chunk:
                        break
                    h.update(chunk)
                digest = h.hexdigest()
        except Exception as e:
            # skip unreadable files
            print(f"SKIP {fpath} ({e})")
            continue
        hash_map.setdefault(digest, []).append(fpath)

# Collect duplicates
duplicates = {h: paths for h, paths in hash_map.items() if len(paths) > 1}

if not duplicates:
    print('No duplicates found by content.')
else:
    print(f'Found {len(duplicates)} groups of duplicate files (by content):')
    for i, (h, paths) in enumerate(sorted(duplicates.items(), key=lambda x: (-len(x[1]), x[0])), 1):
        print('\n--- Group %d ---' % i)
        print('Hash:', h)
        for p in paths:
            print(p)

# Also find duplicate basenames (same filename but possibly different content)
from collections import defaultdict
name_map = defaultdict(list)
for h, paths in hash_map.items():
    for p in paths:
        name_map[os.path.basename(p)].append(p)

basename_dups = {n: ps for n, ps in name_map.items() if len(ps) > 1}
if basename_dups:
    print('\nFound filename collisions (same filename in multiple locations):')
    for n, ps in sorted(basename_dups.items(), key=lambda x: (-len(x[1]), x[0])):
        print('\nFilename:', n)
        for p in ps:
            print(p)

# Save result JSON for later actions
out = {'content_duplicates': duplicates, 'basename_collisions': basename_dups}
with open(os.path.join(ROOT, '.scripts', 'duplicate_report.json'), 'w', encoding='utf-8') as f:
    json.dump(out, f, indent=2)

print('\nReport written to .scripts/duplicate_report.json')
