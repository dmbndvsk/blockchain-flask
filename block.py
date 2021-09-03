import json
import os
import hashlib

# os.curdir - The constant string used by the operating system to refer to the current directory.
blockchain_dir = os.curdir + '/blockchain/'


def get_hash(filename):
    file = open(blockchain_dir + filename, 'rb').read()
    return hashlib.md5(file).hexdigest()


def get_files():
    # os.listdir - Return a list containing the names of the entries in the directory given by path.
    files = os.listdir(blockchain_dir)
    return sorted([int(i) for i in files])


def check_integrity():
    # 1. Read the hash of previous block.
    # 2. Calculate the hash of previous block.
    # 3. Compare received data.
    files = get_files()  # [1, 2, 3, 4, 5]

    results = []

    for file in files[1:]:  # [2, 3, 4, 5]
        f = open(blockchain_dir + str(file))  # '2'
        h = json.load(f)['hash']

        prev_file = str(file - 1)
        actual_hash = get_hash(str(prev_file))

        if h == actual_hash:
            res = 'OK'
        else:
            res = 'Corrupted'

        results.append({'Block': prev_file, 'result': res})

    return results


def write_block(name, amount, to_whom, prev_hash=''):
    files = get_files()
    prev_file = files[-1]

    filename = str(prev_file + 1)

    prev_hash = get_hash(str(prev_file))

    data = {'name': name,
            'amount': amount,
            'to_whom': to_whom,
            'hash': prev_hash,
            }
    with open(blockchain_dir + filename, 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def main():
    print(check_integrity())


# Check if script runs from terminal or not
if __name__ == '__main__':
    main()
