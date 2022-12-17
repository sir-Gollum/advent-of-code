# coding: utf-8
import sys


def main(input_file_name):
    groups = []
    cur_group = []
    for line in open(input_file_name):
        v = line.strip()
        if v:
            cur_group.append(int(v))
        else:
            groups.append(cur_group)
            cur_group = []
    groups.append(cur_group)

    groups = [sum(g) for g in groups]
    print('Groups:', groups)
    print('Answer 1:', max(groups))
    print('Answer 2:', sum(sorted(groups, reverse=True)[:3]))


if __name__ == '__main__':
    main(sys.argv[1])
