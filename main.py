# Name:                                             Renacin Matadeen
# Date:                                                01/27/2018
# Title                                     Collecting Data From gasbuddy.com
#
# ----------------------------------------------------------------------------------------------------------------------
from functions import find_closest_pc
from geopy.distance import geodesic
import multiprocessing
import pandas as pd
import time
# ----------------------------------------------------------------------------------------------------------------------

# Import Centroid Data
centroid_path = r"C:\Users\renac\Documents\Programming\Python\GasBuddy_DataParse\Data\GB_C_2KM\Spaced_Centroids.csv"
centroid_data_df = pd.read_csv(centroid_path)
centroid_data_df['Latitude'] = centroid_data_df['Latitude'].astype('float32')
centroid_data_df['Longitude'] = centroid_data_df['Longitude'].astype('float32')

# Import Postal Codes Data
postal_path = r"C:\Users\renac\Documents\Programming\Python\GasBuddy_DataParse\Data\Postal_Codes\Ontario_PostalCodes.csv"
postal_code_data_df = pd.read_csv(postal_path)

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

if __name__ == "__main__":
    find_closest_pc(centroid_data_df, toronto_pc_locations_df, toronto_pc_df)
























    # # Data For Chunking
    # num_chunks = 3
    # len_of_df = len(centroid_data_df)
    # chunk_size = int(len_of_df / num_chunks)
    # t_val = 0
    # b_val = chunk_size
    #
    # # Split Centroid Dataframe Into Multiple Chunks
    # for chunk in range(num_chunks):
    #     exec("df_" + str(chunk + 1) + " = centroid_data_df[" + str(t_val) + ":" + str(b_val) + "]")
    #     t_val += chunk_size
    #     b_val += chunk_size
    #
    # # Initialize Multiprocessing Units
    # for chunk in range(num_chunks):
    #     exec("p_" + str(chunk + 1) + " = multiprocessing.Process(target=find_closest_pc, args=(" + "df_" + str(chunk + 1) + ", toronto_pc_locations_df, toronto_pc_df," + str(chunk + 1) + ")) ")
    #
    # # Start Multiprocessing
    # for chunk in range(num_chunks):
    #     exec("p_" + str(chunk + 1) + ".start()")
