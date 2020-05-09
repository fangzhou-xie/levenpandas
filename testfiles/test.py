import pdb
from time import time

import pandas as pd

from levenpandas import fuzzymerge


def main():
    test = pd.read_csv('testbig.csv')
    # test = test.dropna(subset=['displayname', 'journal_jstor'])
    print(test)
    df1 = test.copy()[['journal_jstor', 'issn']]
    df2 = test.copy()[['displayname', 'journalid']]
    matched = fuzzymerge(df1, df2, how='inner',  # multi=6,
                         left_on='journal_jstor', right_on='displayname')
    # pdb.set_trace()
    print('test results')
    print(matched)
    matched.to_csv('testresult.csv', index=False)

    N = 1

    print('measure time: multiprocessing (20 cores)')
    start = time()
    for _ in range(N):
        fuzzymerge(df1, df2, how='outer', multi=20,
                   left_on='journal_jstor', right_on='displayname')
    end = time()
    print('total time:', end - start)
    print('average time:', (end - start) / N)

    # print('measure time: multiprocessing (6 cores)')
    # start = time()
    # for _ in range(N):
    #     fuzzymerge(df2, df1, how='outer', multi=20,
    #                right_on='journal_jstor', left_on='displayname')
    # end = time()
    # print('total time:', end - start)
    # print('average time:', (end - start) / N)

    print('measure time: serial processing')
    start = time()
    for _ in range(N):
        fuzzymerge(df1, df2, how='outer', multi=0,
                   left_on='journal_jstor', right_on='displayname')
    end = time()
    print('total time:', end - start)
    print('average time:', (end - start) / N)
    pass


if __name__ == '__main__':
    main()
