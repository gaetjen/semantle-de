import pickle
from random import Random

from process_vecs import only_normal_letters

rnd = Random(133742069)

early_solutions = ['eineinhalb', 'vereinbarung', 'aufeinander', 'anstieg', 'nunmehr']
april_fools = ['CD']
april_first_idxs = [14 + 365, 14 + 365 + 366]

if __name__ == '__main__':
    with open('data/frequent_words.txt', 'r', encoding='UTF-8') as f:
        file_content = f.readlines()
    words = set()
    removed = []
    for line in file_content:
        if only_normal_letters(line.strip(), True):
            words.add(line.strip())
        else:
            removed.append(line.strip())
    words = words.difference(early_solutions)
    print('removed:', len(removed), removed)
    shuffle_list = list(words)
    shuffle_list.sort()
    rnd.shuffle(shuffle_list)
    with open('data/valid_nearest.dat', 'rb') as f:
        valid_nearest_words, _ = pickle.load(f)
    valid_nearest_words = set(valid_nearest_words)
    shuffle_list = [w for w in shuffle_list if w in valid_nearest_words]
    shuffle_list = early_solutions + shuffle_list
    for word, idx in zip(april_fools, april_first_idxs):
        og_idx = shuffle_list.index(word)
        shuffle_list[og_idx], shuffle_list[idx] = shuffle_list[idx], shuffle_list[og_idx]
    print('# words:', len(shuffle_list))
    with open('data/secrets.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(shuffle_list))
