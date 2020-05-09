import multiprocessing as mp
import pdb
from functools import partial
from itertools import product

# Levenshtein.ratio(str1, str2)
import Levenshtein
# import numpy as np
import pandas as pd
from pandas import DataFrame

# from operator import itemgetter
# from time import time


def fuzzymerge(left, right, uselower=True, threshold=0.9, multi=0,
               how='outer', on=None, left_on=None, right_on=None,
               left_index=False, right_index=False):

    if left_index:
        left_on = left_index

    if right_index:
        right_on = right_index

    if on:
        left_on = on
        right_on = on

    left = left.reset_index(drop=True)
    right = right.reset_index(drop=True)
    df1 = left.reset_index()[['index', left_on]].dropna(subset=[left_on])
    df2 = right.reset_index()[['index', right_on]].dropna(subset=[right_on])
    # pdb.set_trace()

    if uselower:
        df1[left_on] = df1[left_on].str.lower()
        df2[right_on] = df2[right_on].str.lower()

    list1 = df1[['index', left_on]].to_numpy()
    list2 = df2[['index', right_on]].to_numpy()

    if multi < 0:
        multi = mp.cpu_count() + multi

    # TODO: longer list on right-hand side to benefit from multiprocessing

    matched = _match_by_left(list1, list2, threshold, multi)
    matched = matched.astype({'leftind': 'Int64', 'rightind': 'Int64'})

    mergeleft = (left
                 .merge(matched, how=how, left_index=True, right_on='leftind'))

    mergeright = (matched
                  .merge(right, how=how, left_on='rightind', right_index=True))

    # pdb.set_trace()
    if how == 'left' or how == 'inner':
        merge_on, delete_on = 'leftind', 'rightind'
    elif how == 'right' or how == 'outer':
        merge_on, delete_on = 'rightind', 'leftind'

    merged = (mergeleft
              .drop(columns=[delete_on])
              .merge(mergeright, how=how, on=merge_on)
              .drop_duplicates(subset=['leftind', 'rightind'])
              .drop(columns=['leftind', 'rightind'])
              .reset_index(drop=True))

    return merged


def _levenshtein(str_a, ind_str_b):
    """
    str_a: str
    ind_str_b: (ind, str_b)
    """
    # ind, str_b = ind_str_b
    return (ind_str_b[0], Levenshtein.ratio(str_a, ind_str_b[1]))


def _levenshtein_mp(list2, threshold, item1):
    matchedindices = []
    ind, x = item1
    ind_distances = [_levenshtein(x, y) for y in list2]
    # pdb.set_trace()
    rightindices = [i[0] for i in ind_distances if i[1] >= threshold]
    matchedindices += list(product([ind], rightindices))
    return matchedindices


def _match_by_left(list1, list2, threshold, multi):
    "fuzzy matching by left"
    matchedindices = []

    if multi:
        singlefunc = partial(_levenshtein_mp, list2, threshold)
        with mp.Pool(multi) as p:
            results = p.map(singlefunc, list1)

        matchedindices = [i for s in results for i in s]

    else:
        for ind, leftentry in list1:
            ind_distances = [_levenshtein(leftentry, y) for y in list2]
            # pdb.set_trace()
            rightindices = [i[0] for i in ind_distances if i[1] >= threshold]
            matchedindices += list(product([ind], rightindices))
    return DataFrame(set(matchedindices), columns=['leftind', 'rightind'])
