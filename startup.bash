pip install virtualenv
virtualenv -v my-venv
source my-venv/bin/activate
export SETUPTOOLS_USE_DISTUTILS=stdlib
pip install -r Requirements.txt
# pip install selenium
# pip install webdriver-manager statsmodels matplotlib pandas_ta
python authenticate.py 