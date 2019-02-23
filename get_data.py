# Name:                                             Renacin Matadeen
# Date:                                                01/31/2018
# Title                                     Collecting Data From gasbuddy.com
#
# ----------------------------------------------------------------------------------------------------------------------
import pandas as pd
from functions import *
# ----------------------------------------------------------------------------------------------------------------------

# # Import List Of Focus Postal Codes
# data_path = r"C:\Users\renac\Documents\Programming\Python\GasBuddy_DataParse\Data\GB_C_2KM\Closest_PC.csv"
# data_df = pd.read_csv(data_path)
# postal_codes = data_df["Closest_PC"].tolist()

# ----------------------------------------------------------------------------------------------------------------------

# # Instantiate WebScraper | Fuel Types Regular [1], MidGrade [2], Premium [3], Diesel [4]
# fuel_type = 1
#
# # Get All Station IDs
# ids = get_all_ids(postal_codes, fuel_type)

# Read ID Data Written To File
ids_df = pd.read_csv(r"C:\Users\renac\Documents\Programming\Python\GasBuddy_DataParse\Data\Raw_Data\Station_IDS.csv")
ids = ids_df["IDS"].tolist()

# Parse Data From Each Site
parse_data(ids)

# ----------------------------------------------------------------------------------------------------------------------
