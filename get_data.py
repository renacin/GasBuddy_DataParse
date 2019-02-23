# Name:                                             Renacin Matadeen
# Date:                                                01/31/2018
# Title                                     Collecting Data From gasbuddy.com
#
# ----------------------------------------------------------------------------------------------------------------------
import pandas as pd
from functions import id_scraper
# ----------------------------------------------------------------------------------------------------------------------

# Import List Of Focus Postal Codes
data_path = r"C:\Users\renac\Documents\Programming\Python\GasBuddy_DataParse\Data\GB_C_2KM\Closest_PC.csv"
data_df = pd.read_csv(data_path)
postal_codes = data_df["Closest_PC"].tolist()

# ----------------------------------------------------------------------------------------------------------------------

# Intiate WebScraper | Fuel Types Regular [1], MidGrade [2], Premium [3], Diesel [4]
fuel_type = 1

# Get Complete List Of Stations
station_list = []
for postal_code in postal_codes:

    # Print Initial Lenght
    init_len = len(station_list)

    ids = id_scraper(str(postal_code), fuel_type)
    station_list.extend(ids)

    # Print Lenght After Addition
    post_len = len(station_list)
    print("Stations Parsed: " + str(post_len) + ", Added: " + str(post_len - init_len))

# Remove Duplicates & Save Data
df_ids = pd.DataFrame({"IDS": station_list})
df_ids = df_ids.drop_duplicates()
print("Stations Parsed: " + str(len(df_ids)) + ", Removed: " + str(post_len - len(df_ids)))

df_ids.to_csv(r"C:\Users\renac\Documents\Programming\Python\GasBuddy_DataParse\Data\Raw_Data\Station_IDS.csv", index=False)
print("\n" + "File Written To Disk")
# ----------------------------------------------------------------------------------------------------------------------
