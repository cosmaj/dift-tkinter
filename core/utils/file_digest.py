from hashlib import md5, sha1
from mmap import mmap, ACCESS_READ


def calculate_hashes(file_name=None):
    if file_name:
        with open(file_name) as file, mmap(
            file.fileno(), 0, access=ACCESS_READ
        ) as file:
            return md5(file).hexdigest(), sha1(file).hexdigest()
