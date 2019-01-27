# Name:                                             Renacin Matadeen
# Date:                                                01/27/2018
# Title                                     Collecting Data From gasbuddy.com
#
# ----------------------------------------------------------------------------------------------------------------------
from geopy.distance import geodesic
import multiprocessing
import pandas as pd
import time
# ----------------------------------------------------------------------------------------------------------------------

def find_closest_pc(centroid_df, pc_location_df, pc_name_df, num):
    closest_pc_list = []
    centroid_df_len = len(centroid_df)
    counter_x = 1

    for index, row_c in centroid_df.iterrows():
        centroid_location = (row_c["Latitude"], row_c["Longitude"])
        pc_name_df["D_To_C"] = pc_location_df.apply(lambda row: geodesic(centroid_location, (row["Latitude"], row["Longitude"])), axis=1)
        val_list = pc_name_df["D_To_C"].tolist()

        min_index = val_list.index(min(val_list))
        closest_pc_list.append(pc_name_df["PostalCode"][min_index])

        pc_name_df.drop(["D_To_C"], axis=1)

        print("Worker " + str(num) + " Progress: "+ str(counter_x) + "/" + str(centroid_df_len))
        counter_x += 1

    centroid_df["Closest_PC"] = closest_postal_code

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
if __name__ == "__main__":
    # Data For Chunking
    num_chunks = 9
    len_of_df = len(centroid_data_df)
    chunk_size = int(len_of_df / num_chunks)
    t_val = 0
    b_val = chunk_size

    # Split Centroid Dataframe Into Multiple Chunks
    for chunk in range(num_chunks):
        exec("df_" + str(chunk + 1) + " = centroid_data_df[" + str(t_val) + ":" + str(b_val) + "]")
        t_val += chunk_size
        b_val += chunk_size

    # Initialize Multiprocessing Units
    for chunk in range(num_chunks):
        exec("p_" + str(chunk + 1) + " = multiprocessing.Process(target=find_closest_pc, args=(" + "df_" + str(chunk + 1) + ", toronto_pc_locations_df, toronto_pc_df," + str(chunk + 1) + ")) ")

    # Start Multiprocessing
    for chunk in range(num_chunks):
        exec("p_" + str(chunk + 1) + ".start()")
