import pickle
from typing import Tuple, List, Dict

import numpy as np
from numpy import array


def most_similar(mat: array, idx: int, k: int) -> Tuple[array, array]:
    vec = mat[idx]
    dists = mat.dot(vec) / (np.linalg.norm(mat, axis=1) * np.linalg.norm(vec))
    top_idxs = np.argpartition(dists, -k)[-k:]
    dist_sort_args = dists[top_idxs].argsort()[::-1]
    return top_idxs[dist_sort_args], dists[top_idxs][dist_sort_args]


def dump_nearest(puzzle_num: int, word: str, words: List[str], mat: array, k: int = 1000) \
        -> Dict[str, Tuple[str, float]]:
    # remove words that contain the solution itself (compounds and declination) from the top 1k
    ok_idxs = np.array(
        [idx for idx, w in enumerate(words) if len(word) < 7 or word == w or word.lower() not in w.lower()])
    words_a = np.array(words)[ok_idxs]
    word_idx = np.nonzero(words_a == word)[0][0]
    sim_idxs, sim_dists = most_similar(mat[ok_idxs], word_idx, k + 1)
    sort_args = np.argsort(sim_dists)[::-1]
    words_sorted = words_a[sim_idxs[sort_args]]
    dists_sorted = sim_dists[sort_args]
    result = zip(words_sorted, dists_sorted)
    closeness = dict()
    for idx, (w, d) in enumerate(result):
        closeness[w] = (idx, d)
    closeness[word] = ("Gefunden!", 1)
    with open(f'data/near/{puzzle_num}.dat', 'wb') as f:
        pickle.dump(closeness, f)
    return closeness


def get_nearest(puzzle_num: int, word: str, words: List[str], mat: array) -> Dict[str, Tuple[str, float]]:
    print(f"getting nearest words for {puzzle_num}")
    try:
        with open(f'data/near/{puzzle_num}.dat', 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return dump_nearest(puzzle_num, word, words, mat)
