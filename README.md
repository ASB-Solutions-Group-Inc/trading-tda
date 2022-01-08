# trading-tda
Trading application for TDA

## command history 

1. pip install virtualenv
2. virtualenv -v my-venv
3. source my-venv/bin/activate
4. export SETUPTOOLS_USE_DISTUTILS=stdlib
5. pip install -r Requirements.txt
6. python authenticate.py 

## loading data into BQ
7. python import-portfolio 
    <!-- cd output
    bq load --autodetect --replace --source_format=CSV trading.trading_data ADBE.csv

    ls | while read line; do bq load --autodetect --noreplace --source_format=CSV trading.trading_data "$line"; done; -->

## Loading files to GCS or use it from the same folder where you saved it 
## Finding ARIMA 
8. pip install statsmodels
9. python arima.py y ALL (Debug Mode) 
    * Parameters :
        - Debug (y or n)
        - Portfolio Name : (ALL)
10.  pip install matplotlib pandas_ta
11. python import-portfolio.py 
## Reference 
1. https://tda-api.readthedocs.io/en/latest/order-templates.html
2. https://selenium-python.readthedocs.io/installation.html
