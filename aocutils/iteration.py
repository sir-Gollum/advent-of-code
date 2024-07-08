# coding: utf-8


def chunkwise(iterable, chunk_size):
    for i in range(0, len(iterable), chunk_size):
        yield iterable[i:i + chunk_size]


def sliding_window(iterable, window_size):
    for i in range(len(iterable) - window_size + 1):
        yield iterable[i:i + window_size]
