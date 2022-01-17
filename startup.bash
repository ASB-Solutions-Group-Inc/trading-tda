pip install virtualenv
virtualenv -v my-venv
source my-venv/bin/activate
export SETUPTOOLS_USE_DISTUTILS=stdlib
brew reinstall ta-lib
pip install -r Requirements.txt

#pip install -U git+https://github.com/twopirllc/pandas-ta
# pip install selenium
# pip install webdriver-manager statsmodels matplotlib pandas_ta
#python ta_model.py
python main.py 