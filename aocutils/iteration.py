# coding: utf-8
from collections import defaultdict
import tqdm


def chunkwise(iterable, chunk_size):
    for i in range(0, len(iterable), chunk_size):
        yield iterable[i : i + chunk_size]


def sliding_window(iterable, window_size):
    for i in range(len(iterable) - window_size + 1):
        yield iterable[i : i + window_size]


def find_repeating_patterns(lst, skip_length_below=2, show_progress=False):
    patterns = defaultdict(list)
    length = len(lst)

    for start in tqdm.tqdm(range(length), disable=not show_progress):
        for end in range(start + 1, length + 1):
            if len(lst[start:end]) < skip_length_below:
                continue
            pattern = tuple(lst[start:end])
            patterns[pattern].append(start)

    repeated_patterns = {
        pattern: indices for pattern, indices in patterns.items() if len(indices) > 1
    }
    return repeated_patterns


def sequential_groups_of_numbers(numbers: list[int]) -> list[list[int]]:
    groups = []
    group = []
    for number in sorted(numbers):
        if not group or number == group[-1] + 1:
            group.append(number)
        else:
            groups.append(group)
            group = [number]

    if group:
        groups.append(group)
    return groups
