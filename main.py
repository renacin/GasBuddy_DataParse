# Name:                                             Renacin Matadeen
# Date:                                                01/30/2018
# Title                                     Collecting Data From gasbuddy.com
#
# ----------------------------------------------------------------------------------------------------------------------
from functions import find_closest_pc
from geopy.distance import geodesic
import pandas as pd
import time
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
postal_code_data_df['Latitude'] = postal_code_data_df['Latitude'].astype('float32')
postal_code_data_df['Longitude'] = postal_code_data_df['Longitude'].astype('float32')

# ----------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    find_closest_pc(centroid_data_df, postal_code_data_df)
