import atexit
import datetime
import dateutil
import httpx
import sys
import tda

from tda.auth import easy_client
from tda.client import Client

API_KEY = 'VXAAOMGXTLGR30JJ2UIOSVAUYARPC39H@AMER.OAUTHAP'
REDIRECT_URI = 'https://127.0.0.1:8080'
TOKEN_PATH = 'ameritrade-credentials.json'
YOUR_BIRTHDAY = datetime.datetime(year=1981, month=1, day=25)
SP500_URL = "https://tda-api.readthedocs.io/en/latest/_static/sp500.txt"
ACCOUNT_ID = "279378043"



def make_webdriver():
    # Import selenium here because it's slow to import
    from selenium import webdriver
    from webdriver_manager.chrome import ChromeDriverManager

    driver = webdriver.Chrome(ChromeDriverManager().install())
    # driver = webdriver.Chrome("/home/USER_NAME/FOLDER/chromedriver")
    # driver = webdriver.Chrome()
    # atexit.register(lambda: driver.quit())
    return driver

c = tda.auth.easy_client(
    API_KEY,
    REDIRECT_URI,
    TOKEN_PATH,
    make_webdriver)

account_information = c.get_account(ACCOUNT_ID, fields=positions )
print(account_information)

resp = c.get_price_history('AAPL',
        period_type=Client.PriceHistory.PeriodType.YEAR,
        period=Client.PriceHistory.Period.TWENTY_YEARS,
        frequency_type=Client.PriceHistory.FrequencyType.DAILY,
        frequency=Client.PriceHistory.Frequency.DAILY)
assert resp.status_code == httpx.codes.OK
history = resp.json()
print(history)
# tda.auth.client_from_login_flow(webdriver, "VXAAOMGXTLGR30JJ2UIOSVAUYARPC39H", "http://localhost", "/", redirect_wait_time_seconds=0.1, max_waits=3000, asyncio=False, token_write_func=None)