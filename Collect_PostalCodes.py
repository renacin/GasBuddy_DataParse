# Name:                                             Renacin Matadeen
# Date:                                                01/27/2018
# Title                                     Collecting Data From gasbuddy.com
#
# ----------------------------------------------------------------------------------------------------------------------
from geopy.distance import geodesic
import pandas as pd
import time
# ----------------------------------------------------------------------------------------------------------------------
"""
    Notes:
        + Understand the data that you are working with!
            + What are the types, as well as subtypes
            + How much memory does your main df require?
                print(toronto_postal_codes_df.dtypes)
                print(toronto_postal_codes_df.info(memory_usage='deep'))

        + Find the postal codes closest to each centroid
        + Be wary of number of postal codes in dataset
            - Limit focus to postal codes that start with M (In Toronto Only)
            - Needed preprossesing attempt
        + Can this be sped up with better Pandas intergration / MultiProcessing?
# """
# ----------------------------------------------------------------------------------------------------------------------

# Import Centroid Data
centroid_path = r"C:\Users\renac\Documents\Programming\Python\GasBuddy_DataParse\Data\GB_C_2KM\Spaced_Centroids.csv"
centroid_data_df = pd.read_csv(centroid_path)
centroid_data_df = centroid_data_df.copy()
centroid_data_df['Latitude'] = centroid_data_df['Latitude'].astype('float32')
centroid_data_df['Longitude'] = centroid_data_df['Longitude'].astype('float32')

# Import Postal Codes Data
postal_path = r"C:\Users\renac\Documents\Programming\Python\GasBuddy_DataParse\Data\Postal_Codes\Ontario_PostalCodes.csv"
postal_code_data_df = pd.read_csv(postal_path)
postal_code_data_df = postal_code_data_df.copy()

# Focus On Postal Codes In Toronto Only | Make New Dataframe
pc_values = postal_code_data_df.loc[postal_code_data_df["PostalCode"].str.startswith("M"), "PostalCode"].values
lat_values = postal_code_data_df.loc[postal_code_data_df["PostalCode"].str.startswith("M"), "Latitude"].values
long_values = postal_code_data_df.loc[postal_code_data_df["PostalCode"].str.startswith("M"), "Longitude"].values

# Separate Coordinated & PostalCode Name
data_lat_long = {"Latitude": lat_values, "Longitude": long_values}
toronto_pc_locations_df = pd.DataFrame(data= data_lat_long)
toronto_pc_locations_df['Latitude'] = toronto_pc_locations_df['Latitude'].astype('float32')
toronto_pc_locations_df['Longitude'] = toronto_pc_locations_df['Longitude'].astype('float32')

data_pc = {"PostalCode": pc_values}
toronto_pc_df = pd.DataFrame(data= data_pc)

# ----------------------------------------------------------------------------------------------------------------------

# Loop Through Centroids
closest_pc_list = []

 # For Progression Monitor
centroid_df_len = len(centroid_data_df)
counter_x = 1

for index, row_c in centroid_data_df.iterrows():

    # Make Variable With X, Y Of Centroid
    centroid_location = (row_c["Latitude"], row_c["Longitude"])

    # Create A DF Variable With The Distances From Postal Codes To Centroid
    toronto_pc_df["D_To_C"] = toronto_pc_locations_df.apply(lambda row: geodesic(centroid_location, (row["Latitude"], row["Longitude"])), axis=1)
    val_list = toronto_pc_df["D_To_C"].tolist()

    # Get The Closest Postal Code
    min_index = val_list.index(min(val_list))
    closest_pc_list.append(toronto_pc_df["PostalCode"][min_index])

    # Del Column Just Created
    toronto_pc_df.drop(["D_To_C"], axis=1)

    print("Progress: " + str(counter_x) + "/" + str(centroid_df_len))
    counter_x += 1

# Append Data To Centroid Dataframe
centroid_data_df["Closest_PC"] = closest_postal_code

# Save As CSV
centroid_data_df.to_csv(r"C:\Users\renac\Documents\Programming\Python\GasBuddy_DataParse\Data\GB_C_2KM\Closest_PC.csv")
