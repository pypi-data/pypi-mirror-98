import numpy as np
import re
from math import floor
import os.path
from os.path import basename, splitext
from glob import glob


def rolling_window(array, window, overlap):
    """Apply a rolling window to a 1d array"""
    # @see https://towardsdatascience.com/fast-and-robust-sliding-window-vectorization-with-numpy-3ad950ed62f5
    if overlap < 1:
        overlap = floor(window * (1 - overlap))
    offset = window - overlap if overlap != window else window
    w = np.arange(window)
    # t is a dense indices vector: we only need once every offset
    t = np.arange(len(array) - window + 1)[::offset]
    idx = (w + t.reshape((-1, 1)))
    return array[idx]


def load_folder(folder, ext="csv", delimiter=","):
    """Load data from a directory.
        Each file is a class, each line is a sample.
        :returns
            - X: matrix of samples
            - y: array of labels
            - classmap: dict {class_idx: class_name}
    """
    dataset = None
    classmap = {}
    for class_idx, filename in enumerate(glob("%s/*.%s" % (folder, ext))):
        label = splitext(basename(filename))[0]
        classmap[class_idx] = label
        X = np.loadtxt(filename, dtype=np.float, delimiter=delimiter)
        y = np.ones((len(X), 1)) * class_idx
        samples = np.hstack((X, y))
        dataset = samples if dataset is None else np.vstack((dataset, samples))
    return dataset[:, :-1], dataset[:, -1], classmap


def load_folder_streaming(folder, window, overlap, features=1, ext="csv", delimiter=","):
    """Load data from a directory.
        Each file is a class with a single line
        :returns
            - X: matrix of samples
            - y: array of labels
            - classmap: dict {class_idx: class_name}
    """
    X, y, classmap = load_folder(folder=folder, ext=ext, delimiter=delimiter)
    y_unique = np.unique(y)
    X_windowed = None
    y_windowed = None
    if overlap < 1:
        overlap = floor(window * overlap)
    for class_idx in y_unique:
        class_mask = (y == class_idx)
        X_class = X[class_mask].flatten()
        X_class = rolling_window(X_class, window=window * features, overlap=overlap * features)
        y_class = np.ones(len(X_class)) * class_idx
        X_windowed = X_class if X_windowed is None else np.vstack((X_windowed, X_class))
        y_windowed = y_class if y_windowed is None else np.concatenate((y_windowed, y_class))
    return X_windowed, y_windowed, classmap


def load_datasets_from_folder(folder, ext='csv', delimiter=None, pattern=None, **kwargs):
    """
    Load datasets from files in a folder
    :param folder:
    :param ext:
    :param delimiter:
    :param kwargs:
    :return: list of (dataset_name, (X, y)) tuples
    """
    if not os.path.exists(folder) or not os.path.isdir(folder):
        return []

    datasets = []

    for filename in glob(os.path.join(folder, '*.%s' % ext)):
        dataset_name = splitext(basename(filename))[0]

        if pattern is not None and re.search(pattern, dataset_name) is None:
            continue

        # guess delimiter if not supplied
        if delimiter is None:
            delimiters = ['\t', ',', ';', ' ']

            with open(filename) as file:
                line = file.readline()

                for delimiter_ in delimiters:
                    if delimiter_ in line:
                        break
        else:
            delimiter_ = delimiter

        data = np.loadtxt(filename, delimiter=delimiter_, **kwargs)
        X = data[:, :-1]
        y = data[:, -1]
        datasets.append((dataset_name, (X, y)))

    return datasets