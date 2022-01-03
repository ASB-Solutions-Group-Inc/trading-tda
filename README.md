# trading-tda
Trading application for TDA

## command history 

1 pip install virtualenv
2 virtualenv -v my-venv
3 source my-venv/bin/activate
4 pip install tda-api
5 pip install selenium
6 pip install webdriver-manager
7 python authenticate.py 

## loading data into BQ
cd output
bq load --autodetect --replace --source_format=CSV trading.trading_data ADBE.csv

ls | while read line; do bq load --autodetect --noreplace --source_format=CSV trading.trading_data "$line"; done;

## Reference 
1. https://tda-api.readthedocs.io/en/latest/order-templates.html
2. https://selenium-python.readthedocs.io/installation.html
