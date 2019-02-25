# Name:                                             Renacin Matadeen
# Date:                                               02/24/2018
# Title                                    How Do I Spoof My IP Address W/ Proxies?
#
# ----------------------------------------------------------------------------------------------------------------------
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
# ----------------------------------------------------------------------------------------------------------------------

def find_fresh_proxies():
    # Append To These Lists
    IP = []
    PORT = []

    # Places With Good Proxies
    good_proxies = ["US", "CA"]

    # Path To ChromeDriver
    path = r"C:\Users\renac\Documents\Programming\Python\Selenium\chromedriver"

    # Add Basic Extensions & Settings
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")

    chrome = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)
    chrome.get("https://free-proxy-list.net/")
    time.sleep(0.5)

    # Page Counter
    counter = 1

    # While Loop To Loop Through Each Page
    while True:
        # Print Page Num
        print("Proxy Pg: " + str(counter))

        # Find All Listings
        proxy_listings = chrome.find_elements_by_xpath('//*[@id="proxylisttable"]/tbody/tr')

        # Source
        html_old = chrome.page_source

        # Append HTTPS Proxies From Canada & USA
        for listing in proxy_listings:
            listing = str(listing.text)
            listing = listing.split(" ")

            # Append Only HTTPS & CAD/US Proxies | In Headless The Page Width Is Different & As A Result The List Len
            if (listing[2] in good_proxies) and (listing[-1] == "yes"):
                IP.append(listing[0])
                PORT.append(listing[1])

            else:
                pass

        # Cycle To Next Page
        try:
            # Click Button
            button = chrome.find_element_by_xpath('//*[@id="proxylisttable_next"]/a')
            button.click()
            time.sleep(0.5)

            counter += 1

            # If Page Source Is Same, Last Page, Raise Error
            html_new = chrome.page_source

            if html_old == html_new:
                raise ValueError

            else:
                pass

        # Break Loop If No More Pages
        except:
            break

    return IP, PORT

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

    # Visit IP Tracking WebSite
    chrome.get("https://www.iplocation.net/")

    # Stall
    time.sleep(2.5)

    chrome.close()
# ----------------------------------------------------------------------------------------------------------------------

# Need Fresh Proxies
IP, PORT = find_fresh_proxies()

# Cycle Through Fresh Proxies
counter_y = 1
list_len = len(IP)

for x, y in zip(IP, PORT):
    # Print Proxy Info
    print("Proxy: {0}/{1} , IP: {2}, PORT: {3}".format(counter_y, list_len, x, y))
    set_up_chrome(x, y)
    counter_y += 1
