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


def sync(source : str, dest : str):
    # Walk the source folder and build a dict of filenames and their hashes

    source_hashes = {}
    for folder, _, files in os.walk(source):
        for fn in files:
            source_hashes[hash_file(Path(folder) / fn)] = fn 

    seen = set()
    

    for folder, _, files in os.walk(dest):
        for fn in files:
            dest_path = Path(folder) / fn
            dest_hash =  hash_file(dest_path)

            seen.add(dest_hash)
            
            # Remove file if exists in dest but not in source 
            if dest_hash not in source_hashes:
                os.remove(dest_path)
            
            elif dest_hash in source_hashes and dest_path != source_hashes[dest_hash]:
                shutil.move(dest_path, Path(folder) / source_hashes[dest_hash])
    

    # Remove all seen files from source hashes
    for seen_file in seen:
        if seen_file in source_hashes:
            source_hashes.pop(seen_file)
    
    for source_hash, fn in source_hashes.items():
        shutil.copy(Path(source) / fn, Path(dest)/ fn)
        

    
                
