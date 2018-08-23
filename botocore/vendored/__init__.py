import sys
import requests
import urllib3


sys.modules['botocore.vendored.requests'] = requests
sys.modules['botocore.vendored.requests.packages.urllib3'] = urllib3
