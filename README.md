# trading-tda
Trading application for TDA

## command history 

1. pip install virtualenv
2. virtualenv -v my-venv
3. source my-venv/bin/activate
4. pip install tda-api
5. pip install selenium
6. pip install webdriver-manager
7. python authenticate.py 

## loading data into BQ
8. python import-portfolio 
    <!-- cd output
    bq load --autodetect --replace --source_format=CSV trading.trading_data ADBE.csv

    ls | while read line; do bq load --autodetect --noreplace --source_format=CSV trading.trading_data "$line"; done; -->

## Loading files to GCS or use it from the same folder where you saved it 
## Finding ARIMA 
9. pip install statsmodels
10. python arima.py y ALL (Debug Mode) 
    Parameters :
        Debug (y or n)
        Portfolio Name : (ALL)
11.  pip install matplotlib pandas_ta
12. python import-portfolio.py 
## Reference 
1. https://tda-api.readthedocs.io/en/latest/order-templates.html
2. https://selenium-python.readthedocs.io/installation.html
