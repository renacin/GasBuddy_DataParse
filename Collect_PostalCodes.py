# Name:                                             Renacin Matadeen
# Date:                                                01/26/2018
# Title                                     Collecting Data From gasbuddy.com
#
#
# ----------------------------------------------------------------------------------------------------------------------

from geopy.distance import geodesic
import pandas as pd
import time

# ----------------------------------------------------------------------------------------------------------------------
"""
    Notes:
        + Find the postal codes closest to each centroid
        + Be wary of number of postal codes in dataset
            - Limit focus to postal codes that start with M (In Toronto Only)
            - Needed preprossesing attempt
# """
# ----------------------------------------------------------------------------------------------------------------------

# Import Centroid Data
centroid_path = r"C:\Users\renac\Documents\Programming\Python\GasBuddy_DataCollection\Data\GB_C_2KM\Spaced_Centroids.csv"
centroid_data_df = pd.read_csv(centroid_path)
centroid_data_df = centroid_data_df.copy()

# Import Postal Codes Data
postal_path = r"C:\Users\renac\Documents\Programming\Python\GasBuddy_DataCollection\Data\Postal_Codes\Ontario_PostalCodes.csv"
postal_code_data_df = pd.read_csv(postal_path)
postal_code_data_df = postal_code_data_df.copy()

# Focus On Postal Codes In Toronto Only | Make New Dataframe
pc_values = postal_code_data_df.loc[postal_code_data_df["PostalCode"].str.startswith("M"), "PostalCode"].values
lat_values = postal_code_data_df.loc[postal_code_data_df["PostalCode"].str.startswith("M"), "Latitude"].values
long_values = postal_code_data_df.loc[postal_code_data_df["PostalCode"].str.startswith("M"), "Longitude"].values

data_ = {"PostalCode": pc_values, "Latitude": lat_values, "Longitude": long_values}
toronto_postal_codes_df = pd.DataFrame(data= data_)

# ----------------------------------------------------------------------------------------------------------------------

# Store Closest Postal Codes In Simple List
closest_postal_code = []

# For Progression Monitor
centroid_df_len = len(centroid_data_df)
counter_x = 1

# Loop Through Each Centroid, and Each Postal Code | O(N Squared)
for index, row_c in centroid_data_df.iterrows():

    # This should be big, and slowly gets smaller as a closer postal code is found
    temp_values = [9999]
    centroid = (row_c["Latitude"], row_c["Longitude"])

    for index, row_p in toronto_postal_codes_df.iterrows():
        pc = row_p["PostalCode"]
        postal_code = (row_p["Latitude"], row_p["Longitude"])
        distance = geodesic(centroid, postal_code).km

        if distance < temp_values[0]:
            temp_values = []
            temp_values.append(distance)
            temp_values.append(pc)

        else:
            pass

    closest_postal_code.append(temp_values[1])
    print("Progress: " + str(counter_x) + "/" + str(centroid_df_len))
    counter_x += 1

# Append Data To Centroid Dataframe
centroid_data_df["Closest_PC"] = closest_postal_code

# Save As CSV
centroid_data_df.to_csv(r"C:\Users\renac\Documents\Programming\Python\GasBuddy_DataCollection\Data\GB_C_2KM\Closest_PC.csv")
