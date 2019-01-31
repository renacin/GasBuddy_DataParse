# Name:                                             Renacin Matadeen
# Date:                                                01/31/2018
# Title                                     Collecting Data From gasbuddy.com
#
# ----------------------------------------------------------------------------------------------------------------------
import pandas as pd
from functions import web_scraper
# ----------------------------------------------------------------------------------------------------------------------

# Import List Of Focus Postal Codes
data_path = r"C:\Users\renac\Documents\Programming\Python\GasBuddy_DataParse\Data\GB_C_2KM\Closest_PC.csv"
data_df = pd.read_csv(data_path)
postal_codes = data_df["Closest_PC"].tolist()

# ----------------------------------------------------------------------------------------------------------------------

# Intiate WebScraper | Fuel Types Regular [1], MidGrade [2], Premium [3], Diesel [4]
fuel_type = 1
web_scraper("L6X4V6", fuel_type)

# ----------------------------------------------------------------------------------------------------------------------
