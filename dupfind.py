#author unknown

import os
import hashlib

def find_duplicate_files(starting_directory='F:\Books'):
    files_seen_already = {}
    queue = [starting_directory]

    # we'll track tuples of (duplicate_file, original_file)
    duplicates = []

    while len(queue) > 0:

        current_path = queue.pop()

        # if it's a directory,
        # put the contents in our queue
        if os.path.isdir(current_path):
            for path in os.listdir(current_path):
                full_path = os.path.join(current_path, path)
                queue.append(full_path)

        # if it's a file:
        else:

            # get its contents
            file_hash = sample_hash_file(current_path)

            # get its last edited time
            current_last_edited_time = os.path.getmtime(current_path)

            # if we've seen it before:
            if file_hash in files_seen_already:

                existing_last_edited_time, existing_path = files_seen_already[file_hash]

                if current_last_edited_time > existing_last_edited_time:
                    # current file is the dupe!
                    duplicates.append((current_path, existing_path))

                else:
                    # old file is the dupe!
                    duplicates.append((existing_path, current_path))

                    # but also update the hash to have the new file's info:
                    files_seen_already[file_hash] = \
                        (current_last_edited_time, current_path)

            # if it's a new file, throw it in the hash and
            # record its path and its last edited time,
            # so we can tell later if it's a dupe
            else:
                files_seen_already[file_hash] = \
                    (current_last_edited_time, current_path)

    return duplicates


def sample_hash_file(path):

    num_bytes_to_read_per_sample = 4000
    total_bytes = os.path.getsize(path)

    hasher = hashlib.sha512()

    # (this "with" block ensures that our file gets closed when we're done)
    with open(path, 'rb') as file:

        # first bytes
        sample = file.read(num_bytes_to_read_per_sample)
        hasher.update(sample)

        # middle bytes
        file.seek(total_bytes / 2)
        sample = file.read(num_bytes_to_read_per_sample)
        hasher.update(sample)

        # last bytes
        # but only if our file is big enough
        if total_bytes > num_bytes_to_read_per_sample * 3:
                file.seek(-num_bytes_to_read_per_sample, os.SEEK_END)
                sample = file.read(num_bytes_to_read_per_sample)
                hasher.update(sample)

    return hasher.hexdigest()
def main():
    tel = {'jack': 4098, 'sape': 4139}
    for value in tel.values():
        print(value)
    dup = find_duplicate_files() 
    for value in dup: 
        print(value);
    
if __name__=="__main__":main()    
