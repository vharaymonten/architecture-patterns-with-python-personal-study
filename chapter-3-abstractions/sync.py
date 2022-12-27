"""
• If a file exists in the source but not in the destination, copy the file over.
• If a file exists in the source, but it has a different name than in the destination,
rename the destination file to match.
• If a file exists in the destination but not in the source, remove it.
"""


import hashlib
import os 
import shutil
from pathlib import Path
from typing import Dict
BLOCKSIZE = 65536

# Get File Hash
def hash_file(path):
    hasher = hashlib.sha1()
    with path.open("rb") as file:
        buf = file.read(BLOCKSIZE)

        while buf:
            hasher.update(buf)
            buf = file.read(BLOCKSIZE)
    return hasher.hexdigest()


def create_files_hashes(source : str) -> Dict[str, str]:
    sources_hashes = dict()
    
    for folder, _, files in os.walk(source):
        for fn in files:
            sources_hashes[hash_file(Path(folder) / fn)] = fn
    return sources_hashes

def get_actions_for_sync(source_hashes : Dict[str, str], dest_hashes, src, dest):
    seen = set()
    for dest_hash, fn in dest_hashes.items():
        seen.add(dest_hash)
        if dest_hash not in source_hashes:
            yield ("REMOVE", "", dest / fn)
        elif dest_hash in source_hashes and fn != source_hashes[dest_hash]:
            yield  ("MOVE", dest / fn, dest / source_hashes[dest_hash])
        
    for src_hash, fn in source_hashes.items():
        if src_hash not in seen:
            yield ("COPY", src / fn, dest / fn)
        