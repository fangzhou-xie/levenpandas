levenpandas: merging pandas dataframes by Levenshtein distance
================
Fangzhou Xie (fangzhou\[dot\]xie\[at\]nyu\[dot\]edu)

## levenpandas

I recently needed to fuzzy-matching some relatively large datasets and
failed to find any package that would suit my need. So I ended up
writing my own.

## Installation

    pip install levenpandas

## Dependencies

There are only two packages that are imported by this `levenpandas`:
`pandas` and `python-Levenshtein`. They are listed as the requirements
of this package, and you should have them after installing
`levenpandas`.

## Description

I wish to match two columns of `pandas.DataFrame` object fuzzy matching,
and wish to do so by evaluating the Levenshtein distance between each
pair of elements in the two columns.

There are a number of good packages, including `fuzzywuzzy`,
`fuzzy-pandas`. `fuzzy-pandas` turns out to be slow in my application,
while `fuzzywuzzy` reports the similarity ratio range between 0-100, and
round it to integers.

In my case, I need something that gives me a similar sytax as `pandas`,
could work with `pandas.DataFrame`, and possibly with parallel support.
And these three features are the main building blocks of this
`levenpandas`.

There is only one function that has been exposed: `fuzzymerge()`.

Example:

    from levenpandas import fuzzymerge

    left       : dataframe 1
    right      : dataframe 2
    uselower   : bool, whether to match by the lower case, default True
    threshold  : float, threshold to determine similarity given by Levenshtein distance,
                 default 0.9
    multi      : int, processes to be used for multiprocessing, default 0
    how        : merge type, 'outer', 'inner', 'left', 'right', default 'outer'
    on         : the name of columns to be matched in both dataframes, default None
    left_on    : name of column in dataframe 1
    right_on   : name of column in dataframe 2

As you probably have notices, the syntax follows a similar usage with
that of the `pandas.DataFrame.merge`. If you are familiar with `pandas`,
you should be quite comfortable using the “fuzzy” version. You can use
`how`, `on`, `left_on`, and `right_on` just as you are using
`pandas.DataFrame.merge`.

Moreover, there is also parallel support by native
`multiprocessing.Pool`. You can choose `multi` as the number of
processes you want to run. Positive integers means that you are choose
`multi` number of processes, while negative ingeters means that you are
choosing all available but `multi` number of processes. For example, you
can choose `multi=4`, which means that there will be 4 threads running.
However, if you choose `multi=-2`, that means you will use the number of
your CPU cores minus 2 as your number of processes.

The merged result, not surprisingly, is a `pandas.DataFrame`.

## License

Under MIT license.
