# FPLTransfers

A Python package based on the [fpl](https://github.com/amosbastian/fpl) and [pandas-fpl](https://github.com/177arc/pandas-fpl) packages which can be used to analyse a team and work out optimum transfers.

Has functions to do wildcard, single and double gameweek transfers.

Still a work in progress.

## Download FPLTransfers

FPLTransfers is available on PYPI under the package name `FPLTransfers`. It can be downloaded using pip:

`pip install FPLTransfers`

## Use Guide

FPLTransfers can be used with an existing user team or just accessing the FPL API directly. The wildcard function works without supplying user details, the single and double transfers require user details.

Initialise the connection with to the FPL API like so:

`conn = FPLTransfers.FPLTransfers()`

or, supplying user details:

`conn = FPLTransfers.FPLTransfers(email='example.email@gmail.com', password='examplepasswd')`

Each of the transfer functions can specify the number of weeks to look ahead to calculate the transfer. It is automatically set to be 5 weeks. Examples of all the transfer functions are shown below:

```
conn.wildcard(no_weeks=5)
conn.single_transfer(no_weeks=5)
conn.double_transfer(no_weeks=5)
```

This documentation is incomplete and needs further expanding on.
