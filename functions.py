# Name:                                             Renacin Matadeen
# Date:                                                01/27/2018
# Title                                     Functions Used To Parse Data From GasBuddy
#
# ----------------------------------------------------------------------------------------------------------------------
import geopy
from geopy.distance import VincentyDistance, geodesic
import multiprocessing
import pandas as pd
import time
# ----------------------------------------------------------------------------------------------------------------------
# This Function Will Return A DF With Values That Are Within A Bounding Box
def bounding_box_df(focus_lat, focus_long, pc_location_df, distance_):

    # Find MIN/MAX Lat/Long
    lat_range = []
    long_range = []

    bearing = [45, 225]
    for b in bearing:
        origin = geopy.Point(focus_lat, focus_long)
        destination = VincentyDistance(kilometers= distance_).destination(origin, b)
        lat_range.append(destination.latitude)
        long_range.append(destination.longitude)







    # Return A Version Of PC_Location_DF, That Extends Only To Identified Range

    # The Point That Is The Closest Is Within Both Ranges
    print(lat_range)
    print(long_range)



    pc_loc_lat = pc_location_df[pc_location_df['Latitude'].between(min(lat_range), max(lat_range), inclusive=True)]
    pc_loc_ = pc_loc_lat[pc_loc_lat['Longitude'].between(min(long_range), max(long_range), inclusive=True)]

    print(pc_loc_lat.describe())
    print(pc_loc_.describe())
    time.sleep(1000)



    return pc_loc_


# This Function Will Find The Closest Postal Code To A Centroid, And Return A List That Matches The Index Of The Centroid File
def find_closest_pc(centroid_df, pc_location_df, pc_name_df):

    closest_pc_list = []
    centroid_df_len = len(centroid_df)
    counter_x = 1
    distance_km = 2

    for index, row_c in centroid_df.iterrows():
        centroid_location = geopy.Point(row_c["Latitude"], row_c["Longitude"])

        # Find Focus Values & Add Index As A Column
        focus_df = bounding_box_df(row_c["Latitude"], row_c["Longitude"], pc_location_df, distance_km)
        focus_df["Index_Values"] = focus_df.index.tolist()

        # Find Closest Postal Code To Focus Centroid
        focus_df["D_To_C"] = focus_df.apply(lambda row: geodesic(centroid_location, geopy.Point(row["Latitude"], row["Longitude"])), axis=1)
        val_list = focus_df["D_To_C"].tolist()

        # Find The Index Value & Convert To Postal Code
        min_index = int(val_list.index(min(val_list)))
        focus_df.reset_index(inplace = True)
        min_index_index_vals = focus_df["Index_Values"][min_index]
        closest_pc_list.append(pc_name_df["PostalCode"][min_index_index_vals])

        # Monitor Progress
        print("Progress: " + str(counter_x) + "/" + str(centroid_df_len) + ", Postal Code: " + pc_name_df["PostalCode"][min_index] + ", Distance: " + str(min(val_list)))

        # Del Column Just Created
        focus_df.drop(["D_To_C"], axis=1)

        # Add To Counter
        counter_x += 1

        #time.sleep(20)

    centroid_df["Closest_PC"] = closest_postal_code

# ----------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    pass
