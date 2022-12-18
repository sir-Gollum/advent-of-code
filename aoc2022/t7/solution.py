# coding: utf-8
import os
import re
import sys
from collections import defaultdict


def main(input_file_name):
    path_sizes = defaultdict(int)
    cur_path = '/'

    with open(input_file_name) as f:
        lines = [line.strip() for line in f]

    for line in lines:
        # ignore dirs in output, ignore file names, ignore `ls` commands
        if line.startswith('$ cd '):
            target = line[5:]
            cur_path = os.path.abspath(os.path.join(cur_path, target))
        elif not line.startswith('$ ls'):
            # we're in `ls` output
            m = re.match(r'(\d+) ', line)
            if m:
                file_size = int(m.group(0))
                count_path = cur_path
                path_sizes['/'] += file_size
                while count_path != '/':
                    path_sizes[count_path] += file_size
                    count_path = os.path.dirname(count_path)

    answer1 = sum([v for v in path_sizes.values() if v <= 100000])
    answer2 = min([
        v for v in path_sizes.values()
        if 70000000 - path_sizes['/'] + v >= 30000000
    ])

    print('Answer 1:', answer1)
    print('Answer 2:', answer2)


if __name__ == '__main__':
    main(sys.argv[1])
