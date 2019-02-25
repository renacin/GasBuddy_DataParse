# Name:                                             Renacin Matadeen
# Date:                                               02/24/2018
# Title                                    How Do I Spoof My IP Address W/ Proxies?
#
# ----------------------------------------------------------------------------------------------------------------------
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
# ----------------------------------------------------------------------------------------------------------------------

def set_up_chrome(IP_Address, Port):
    ext_1 = r"C:\Users\renac\Documents\Programming\Python\Selenium\Extensions\uBlock-Origin_v1.14.8.crx"
    path = r"C:\Users\renac\Documents\Programming\Python\Selenium\chromedriver"

    # Add Basic Extensions & Settings
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_extension(ext_1)
    chrome_options.add_argument("--disable-infobars")

    # Change Proxy
    chrome_options.add_argument("--proxy-server=" + str(IP_Address) + ":" + str(Port))
    chrome = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)

    return chrome

# ----------------------------------------------------------------------------------------------------------------------

# Open List Of HTTPS Proxies
df = pd.read_csv(r"C:\Users\renac\Documents\Programming\Python\GasBuddy_DataParse\Proxies\Proxies.csv")
ip_address = df["IP"].tolist()
port = df["PORT"].tolist()


# Cycle Through IP Address
for x, y in zip(ip_address, port):

    # Set Up Chrome
    chrome = set_up_chrome(x, y)
    chrome.get("https://whatismyipaddress.com/")
    time.sleep(10)
    chrome.close()
