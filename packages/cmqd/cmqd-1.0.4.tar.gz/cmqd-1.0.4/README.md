# ClearMacro <!-- omit in toc -->

The ClearMacro Python library provides convenient access to the ClearMacro API from applications written in the Python language. It includes a pre-defined set of methods that make it simple to start interacting with the API.

- [Installation](#installation)
- [Examples](#examples)
- [Full Python Docstrings](#full-python-docstrings)

## Installation

To use the package, run:

```sh
pip install --upgrade cmqd
```

## Examples

Selection of examples; a reference point of getting started.

```
// Instantiate a client
>>> from clearmacro import Client
>>> config = {'url': '<HOST HERE>', 'username': '<EMAIL HERE>', 'password': '<PASSWORD HERE>'}
>>> client = Client(**config)

// Get the catalogue
>>> catalogue = client.get_signals_catalogue()

// Consume it as a DataFrame
>>> client.json_to_df(catalogue)
     signalId                                    name                             description   universe   category
0           8                        Crossborder Flow                        Crossborder Flow  Economics     Credit
1           9           Crossborder Private Liquidity           Crossborder Private Liquidity  Economics     Credit
2          10               Crossborder Policy Sector               Crossborder Policy Sector  Economics     Credit
3          11           Crossborder Monetized Savings           Crossborder Monetized Savings  Economics  Inflation
...
```

```
// Get the markets for which a certain signal is available.
>>> markets_for_my_signal = client.get_markets_for_signal('Bond Valuation Score IHS')

// Consume as DataFrame
>>> client.json_to_df(markets_for_my_signal)
    classId              name marketCategory
0        86         Australia        Country
1        87           Austria        Country
2        88           Belgium        Country
3        89            Brazil        Country
4        90            Canada        Country
...
```

```
// Request a certain signal series
>>> series = client.get_signal_series(signal='Crossborder Flow', market='US', research_type='Back-test Level', last_date_only=False, start_date='2016-1-1', end_date='2020-10-16')

// Consume it as a DataFrame
>>> client.json_to_df(series)
                 dateTimes    values
0   2016-01-29T23:59:59.99  5.485577
1   2016-02-29T23:59:59.99  5.974441
2   2016-03-31T23:59:59.99  6.388535
3   2016-04-29T23:59:59.99  6.714286
4   2016-05-31T23:59:59.99  6.340190
5   2016-06-30T23:59:59.99  5.599369
6   2016-07-29T23:59:59.99  4.792453
7   2016-08-31T23:59:59.99  3.793103
8   2016-09-30T23:59:59.99  3.207812
9   2016-10-31T23:59:59.99  3.046729
10  2016-11-30T23:59:59.99  3.375776
11  2016-12-30T23:59:59.99  3.981424
...

// If there is no such series, get an exception which can be handled:
>>> client.get_signal_series('Random signal', 'Random market', 'Random research type')
ValueError: Invalid input.

```

```
// Request data with a certain frequency e.g. weekly data on Wednesdays.
>>> wedDataSeries = client.get_signal_series('Country Valuation Score TR', 'Germany', 'Back-test Momentum', frequency_key = 'W-WED')

// Consume it as a DataFrame
>>> client.json_to_df(wedDataSeries)
                   dateTimes    values
0     1995-02-15T23:59:59.99  4.449885
1     1995-02-22T23:59:59.99  5.507832
2     1995-03-01T23:59:59.99  5.042825
3     1995-03-08T23:59:59.99  6.214902
4     1995-03-15T23:59:59.99  6.647544
...
```

## Full Python Docstrings

Documentation for each method of the `Client` class:

```
get_signals_catalogue()
"""
Function to retrieve the list of all signals.

Returns:
    JSON list of signal objects.
"""
```

```
get_all_markets()
"""
Function to retrieve the list of all markets.

Returns:
    JSON list of market objects.
"""
```

```
get_signal_universes()
"""
Function to retrieve the signal universes.

Returns:
    JSON list of universe objects.
"""
```

```
get_categories_for_universe(universe: str)
"""
Function to retrieve the list of categories corresponding to the passed universe.

Args:
    universe (str): One of the signal universes. Available options are the "name" fields from the list of universe objects obtained by calling the get_signal_universes method.

Returns:
    JSON list of category objects.
"""
```

```
get_categories_for_universe_id(universe_id: int)
"""
Function to retrieve the list of categories corresponding to the passed universe id.

Args:
    universe_id (int): One of the signal universes. Available options are the "universeId" fields from the list of universe objects obtained by calling the get_signal_universes method.

Returns:
    JSON list of category objects.
"""
```

```
get_signals_for_universe_cat_pair(universe: str, category: str)
"""
Function to retrieve all signals belonging to the given universe, category pair.

Args:
    universe (str): One of the signal universes. Available options are the "name" fields from the list of universe objects obtained by calling the get_signal_universes method.
    category (str): One of the categories of the above universe. Available options are the "name" fields from the list of category objects obtained by calling get_categories_for_universe(universe).

Returns:
    JSON list of signal objects.
"""
```

```
get_signals_for_universe_cat_pair_id(universe_id: int, category_id: int)
"""
Function to retrieve all signals belonging to the given universe, category pair by id.

Args:
    universe_id (int): One of the signal universes. Available options are the "universeId" fields from the list of universe objects obtained by calling the get_signal_universes method.
    category_id (int): One of the categories of the above universe. Available options are the "categoryId" fields from the list of category objects obtained by calling get_categories_for_universe_id(universe_id).

Returns:
    JSON list of signal objects.
"""
```

```
get_market_categories()
"""
Function to retrieve the list of all market categories.

Returns:
    JSON list of market category objects.
"""
```

```
get_markets_for_market_cat(market_category: str)
"""
Function to retrieve the list of markets corresponding to the passed market category.

Args:
    market_category (str): One of the market categories. Available options are the "name" fields from the list of market category objects obtained by calling the get_market_categories method.

Returns:
    JSON list of market objects.
"""
```

```
get_markets_for_market_cat_id(market_category_id: int)
"""
Function to retrieve the list of markets corresponding to the passed market category id.

Args:
    market_category_id (int): One of the market categories. Available options are the "marketCategoryId" fields from the list of market category objects obtained by calling the get_market_categories method.

Returns:
    JSON list of market objects.
"""
```

```
get_markets_for_signal(signal: str)
"""
Function to retrieve the list of markets corresponding to the passed signal.

Args:
    signal (str): One of the signals. Available options are the "name" fields from the list of signals objects obtained by calling the get_signals_catalogue method.

Returns:
    JSON list of market objects.
"""
```

```
get_markets_for_signal_id(signal_id: int)
"""
Function to retrieve the list of markets corresponding to the passed signal id.

Args:
    signal_id (int): One of the signals. Available options are the "signalId" fields from the list of signals objects obtained by calling the get_signals_catalogue method.

Returns:
    JSON list of market objects.
"""
```

```
get_signals_for_market(market: str)
"""
Function to retrieve the list of signals available for the given market.

Args:
    market (str): One of the valid markets. Available options are the "name" fields from the list of market objects obtained by calling the get_all_markets method.

Returns:
    JSON list of signal objects.
"""
```

```
get_signals_for_market_id(class_id: int)
"""
Function to retrieve the list of signals available for the given market.

Args:
    class_id (int): One of the valid markets. Available options are the "classId" fields from the list of market objects obtained by calling the get_all_markets method.

Returns:
    JSON list of signal objects.
"""
```

```
get_research_types_for_signal_market_pair(signal: str, market: str)
"""
Function to retrieve the list of research types corresponding to the passed signal and market.

Args:
    signal (str): One of the signals. Available options are the "name" fields from the list of signal objects obtained by calling the get_signals_catalogue method.
    market (str): One of the valid markets for the above signal. Available options are the "name" fields from the list of market objects obtained by calling the get_markets_for_signal(signal) method.

Returns:
    JSON list of research type objects.
"""
```

```
get_research_types_for_signal_market_pair_id(signal_id: int, market_id: int)
"""
Function to retrieve the list of research types corresponding to the passed signal id and market id.

Args:
    signal_id (int): One of the signals. Available options are the "signalId" fields from the list of signal objects obtained by calling the get_signals_catalogue method.
    market_id (int): One of the valid markets for the above signal. Available options are the "classId" fields from the list of market objects obtained by calling the get_markets_for_signal_id(signal_id) method.

Returns:
    JSON list of research type objects.
"""
```

```
get_signal_series(
    signal: str,
    market: str,
    research_type: str,
    last_date_only=False,
    start_date=None,
    end_date=None,
    frequency_key=None,
    )
"""
Function to retrieve a signal time series.

Args:
    signal (str): Options are "name" fields from list of signal objects returned by get_signals_catalogue.
    market (str): Options are "name" fields from list of market objects returned by get_markets_for_signal(signal).
    research_type (str): Options are "name" fields from list of research type objects returned by get_research_types_for_signal_market_pair(signal, market).
    last_date_only (bool, optional): Flag indicating if only the last date of the time series is desired.
    start_date (str, optional): Start date of the series in ISO format YYYY-MM-DD.
    end_date (str, optional): End date of the series in ISO format YYYY-MM-DD.
    frequency_key (str): One of the desired frequencies (None is for all values available, undetermined frequency):

    D, (Daily - all days)
    WD, (Weekdays)
    W_MON, (Weekly data on Mondays)
    W_TUE, (Weekly data on Tuesdays)
    W_WED, (Weekly data on Wednesdays)
    W_THU, (Weekly data on Thursdays)
    W_FRI, (Weekly data on Fridays)
    W_SAT, (Weekly data on Saturdays)
    W_SUN, (Weekly data on Sundays)
    M, (Monthly data - end of month)
    MS, (Monthly data - start of month)
    Q, (Quarterly data - end of quarter)
    QS (Quarterly data - start of quarter)

Examples:
    >>> client.get_signal_series('Crossborder Flow', 'US', 'Back-test Level', last_date_only=False, start_date='2016-1-1', end_date='2020-10-16')

Returns:
    Time series object.
"""
```

```
get_signal_series_id(
signal_id: int,
market_id: int,
research_type_id: int,
last_date_only=False,
start_date=None,
end_date=None,
frequency_key=None
)
"""
Function to retrieve a signal time series by ids.

Args:
    signal_id (int): Options are "signalId" fields from list of signal objects returned by get_signals_catalogue.
    market_id (int): Options are "classId" fields from list of market objects returned by get_markets_for_signal_id(signal_id).
    research_type_id (int): Options are "researchTypeId" fields from list of research type objects returned by get_research_types_for_signal_market_pair_id(signal_id, market_id).
    last_date_only (bool): Flag indicating if only the last date of the time series is desired.
    start_date (str): Start date of the series in ISO format YYYY-MM-DD.
    end_date (str): End date of the series in ISO format YYYY-MM-DD.
    frequency_key (str): One of the desired frequencies (None is for all values available, undetermined frequency):

    D, (Daily - all days)
    WD, (Weekdays)
    W_MON, (Weekly data on Mondays)
    W_TUE, (Weekly data on Tuesdays)
    W_WED, (Weekly data on Wednesdays)
    W_THU, (Weekly data on Thursdays)
    W_FRI, (Weekly data on Fridays)
    W_SAT, (Weekly data on Saturdays)
    W_SUN, (Weekly data on Sundays)
    M, (Monthly data - end of month)
    MS, (Monthly data - start of month)
    Q, (Quarterly data - end of quarter)
    QS (Quarterly data - start of quarter)

Examples:
    >>> client.get_signal_series_id(8, 137, 94, last_date_only=False, start_date='2016-1-1', end_date='2020-10-16')

Returns:
    Time series object.
"""
```

```
json_to_df(json)
"""
Function to convert JSON/JSON list to a pandas.DataFrame object.

Args:
    json: The JSON to be converted - this is the format all methods return.

Returns:
    The data contained in the JSON cast as a DataFrame.

    If the data is a time series, the dataframe will be indexed by datetimes and there
    will be a 'values' column containing the value corresponding to each DateTimeIndex.
"""
```
