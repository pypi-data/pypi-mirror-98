# QRTT DATA (data.qrtt.org)

## What is this?

QRTT DATA is a side project by the developer of QRTT (Quantitative Research and Trading Tools). Our goal is to provide free, easy-to-use financial data to non-professional quantitative research/trading hobbyists for basic exploratory analysis.

## What is this not?

QRTT DATA is not a real-time data service. While we host some high-frequency data, most datasets are not updated frequently. Our goal is to update every dataset at least once a month, but there is no guarantee.

Also, data here is not meant to be used for live trading or sophisticated backtesting systems. Our data are scraped from various sources on the internet. While these sources are trustworthy, we have not done any additional checks. We only do some basic cleaning and formating. The creator of the QRTT project does not guarantee the accuracy of these data. It is highly recommended to backtest and trade using data from your broker.

## How to use this data?

All data are saved in CSV format. The basic url structure is https://data.qrtt.org/{instructment_type}/{location}/{type}/{frequency}/{symbol-period}.csv. Right now, we only have daily data for US-listed stocks. We will add more documentation once more data types are added.

We also have a simple Python package for loading datasets. It can be installed:

`pip install qrtt_data`

### Stock Data

For now, only end-of-day US-listed stocks are available. Data can be accessed through the following command:

`from qrtt_data import stock_data`
`stock_data.load_historical('SPY')`

### Futures Data

Will add later.


### Crypto Data

Will add later.


### Option Data

Will add later.