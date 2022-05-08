pip install virtualenv
virtualenv -v my-venv
source my-venv/bin/activate
export SETUPTOOLS_USE_DISTUTILS=stdlib
export CLOUDSDK_CORE_DISABLE_PROMPTS=1
/Users/avnitbambah/google-cloud-sdk/install.sh
gcloud auth activate-service-account --key-file servicekey.json
gcloud config set project saleswebpage
brew reinstall ta-lib
pip install -r Requirements.txt

#pip install -U git+https://github.com/twopirllc/pandas-ta
# pip install selenium
# pip install webdriver-manager statsmodels matplotlib pandas_ta
#python ta_model.py
python main.py 