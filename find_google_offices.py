# This module is solving a word puzzle and finds cities of given list inside a matrix of letters.

from copy import copy
import pygtrie as trie


def get_cities(filename):
    with open(filename, 'r') as raw_data_file:
        cities = [line.strip('\n') for line in raw_data_file.readlines() if not line.startswith("<")]
    return cities


def get_words_matrix(filename):
    with open(filename, 'r') as file:
        return [list(line.strip('\n').replace(' ', '')) for line in file if not line.startswith('\n')]


def get_next_coords(matrix, this_coord=[0,0], step=1):
    res = list()
    res.append([this_coord[0], this_coord[1] + step])
    res.append([this_coord[0], this_coord[1] - step])
    res.append([this_coord[0] + step, this_coord[1]])
    res.append([this_coord[0] - step, this_coord[1]])
    return list(filter(lambda coords: len(list(filter(lambda x: 0 <= x < len(matrix), coords))) == len(coords), res))


def get_next_coords_diag(matrix, this_coord=[0, 0], step=1):
    res = list()
    res.append([this_coord[0] + step, this_coord[1] + step])
    res.append([this_coord[0] + step, this_coord[1] - step])
    res.append([this_coord[0] - step, this_coord[1] - step])
    res.append([this_coord[0] - step, this_coord[1] + step])
    return list(filter(lambda coords: len(list(filter(lambda x: 0 <= x < len(matrix), coords))) == len(coords), res))


def search_cities(search_matrix, items_trie, row_i, col_i, results=[], curr = [], seen=[]):
    curr.append(matrix[row_i][col_i])
    curr[0] = curr[0].upper()
    prefix = ''.join(curr)

    if items_trie.has_subtrie(prefix):
        for coord in get_next_coords(matrix, [row_i, col_i]):
            if coord not in seen:
                results.append(search_cities(search_matrix, items_trie, coord[0], coord[1], results, curr, seen))
        for coord in get_next_coords_diag(matrix, [row_i, col_i]):
            if coord not in seen:
                results.append(search_cities(search_matrix, items_trie, coord[0], coord[1], results, curr, seen))
    if items_trie.has_key(prefix):
        return prefix

    del curr[-1]
    return []


if __name__ == "__main__":
    office_cities = get_cities("raw.txt")
    office_cities = list(map(lambda x: x[:x.find(' ')] if ' ' in x else x, office_cities))

    oc_trie = trie.CharTrie()
    for city in office_cities:
        oc_trie[city] = True

    matrix = get_words_matrix("word_puzzle.txt")
    matrix = [[str.lower(letter) for letter in row] for row in matrix]

    matrix_str = list(map(lambda x: ' '.join(x), matrix))
    print("\n".join(matrix_str))

    res = []
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            search_cities(matrix, oc_trie, i, j, res, [])
            res = [x for x in res if x]

    print(set(res))
    print(len(set(res)))