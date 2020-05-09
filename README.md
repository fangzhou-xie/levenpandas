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

There is only one function that has been exposed: `fuzzymerge()`; yet
there is another utility function that will give you a sample dataset to
play with.

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

The sample test data is given by the following function: `testpath()`.
This utility function will return you a test dataset.

    from levenpandas import testpath

## A Guided Example

    >>> # first load the function and test dataset
    >>> from levenpandas import fuzzymerge, testpath
    >>> import pandas as pd
    
    >>> # load test dataset
    >>> df = pd.read_csv(testpath())

After loading this file, you notice that it consist of a list of
journals in Economics. This sample dataset is, in fact, coming from two
sources, and I fuzzy-merge them together before writing this package.

    >>> df[['journal1','journal2']]
                            journal1                                           journal2
    0   Journal of Political Economy                       Journal of Political Economy
    1                            NaN                       Journal of Political Ecology
    2   The American Economic Review                       The American Economic Review
    3                Economic Theory                                    Economic Theory
    4                  Public Choice                                      Public Choice
    ..                           ...                                                ...
    82                           NaN   Journal of the American Research Center in Egypt
    83                           NaN                                  Food Microbiology
    84                           NaN               Journal of Electronics Manufacturing
    85                           NaN  International Journal of Global Environmental ...
    86                           NaN                                           Currents

You should realize that the rows are perfectly merged already, but let’s
divide the dataframe into two and test our package.

    >>> df1 = df[['journal1']]
    >>> df2 = df[['journal2']]
    >>> merged = fuzzymerge(df1, df2, left_on='journal1', right_on='journal2')
    >>> merged.dropna()
    journal1                          journal2
    0        Journal of Political Economy      Journal of Political Economy
    1        Journal of Political Economy      Journal of Political Ecology
    3        The American Economic Review      The American Economic Review
    4                     Economic Theory                Econometric Theory
    5                     Economic Theory                Econometric Theory
    ..                                ...                               ...
    70    The Review of Financial Studies       Review of Financial Studies
    71             The Journal of Finance                Journal of Finance
    72     The Journal of Law & Economics  The Journal of Law and Economics
    73  The Journal of Risk and Insurance     Journal of Risk and Insurance
    74  The Journal of Economic Education     Journal of Economic Education

Here, we need to specify on which columns should we merge. If the
columns from both side of DataFrame happens to have the same name, you
can just use ‘on’ keyword; otherwise, you have to use ‘left\_on’ and
‘right\_on’ to let the function know what is the name of the column
for each of the DataFrame. Also, you can only pass ‘str’ for these
keywords, as the `fuzzymerge` function only supports single-column
merging.

What is more, you can also choose the merge behavior by `how` keyword.
As in `pandas.DataFrame.merge`, you choose one from the following:
`['inner', 'outer', 'left', 'right']`, and its behavior is explained
[here](https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html).

    >>> merged = fuzzymerge(df1, df2, left_on='journal1', right_on='journal2', how='left')

If you have relatively large dataset that you want to merge, you can
pass positive/negative integer values for `multi` argument. A positive
value means that you are choosing that many of cores to do the merging,
while a negative integer means that you leave that many of cores **NOT**
do the merging.

What is more, there is a parameter `threshold` to control the level of
confidence you wish to restrict on the similarity between strings. This
is calculated by `python-Levenshtein` package, and should be between 0
and 1. The default value is 0.9, meaning that if two strings are
compared against each other, and they have similarity ratio over 0.9,
they will be regarded as the *same* one and they will be merged
together. If you want to use a stricter test, you should change this
paramter closer to 1; while if you want to relax it, you should use a
smaller positive value.

## License

Under MIT license.
