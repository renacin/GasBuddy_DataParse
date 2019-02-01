# Name:                                             Renacin Matadeen
# Date:                                               01/30/2018
# Title                                     Functions Used To Parse Data From GasBuddy
#
# ----------------------------------------------------------------------------------------------------------------------
import geopy
from geopy.distance import VincentyDistance, geodesic

from bs4 import BeautifulSoup
import urllib3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import re
import pandas as pd
import time
import math
# ----------------------------------------------------------------------------------------------------------------------

# This Function Will Return A DF With Values That Are Within A Bounding Box
def bounding_box_df(focus_lat, focus_long, pc_df, distance_):

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
    pc_loc_long = pc_df[pc_df['Longitude'].between(min(long_range), max(long_range), inclusive=True)]
    pc_loc_ = pc_loc_long[pc_loc_long['Latitude'].between(min(lat_range), max(lat_range), inclusive=True)]
    return pc_loc_


# This Function Will Find The Closest Postal Code To A Centroid, And Return A List That Matches The Index Of The Centroid File
def find_closest_pc(centroid_df, pc_df):

    start_time = time.time()

    # Data To Be Collected
    closest_pc_list = []
    focus_lat_list = []
    focus_long_list = []

    # Needed Hyperparametres
    centroid_df_len = len(centroid_df)
    counter_x = 1

    initial_min_distance = 1
    min_distance = initial_min_distance
    initial_distance = min_distance / (math.cos(45)) # Related To The Bearing! [45, 225]
    distance_km = initial_distance

    for index, row_c in centroid_df.iterrows():
        centroid_location = geopy.Point(row_c["Latitude"], row_c["Longitude"])

        # Keep Trying Until A Good Distance Value Is Found & Utilized
        while True:
            try:
                # Find Focus Values & Add Index As A Column
                focus_df = bounding_box_df(row_c["Latitude"], row_c["Longitude"], pc_df, distance_km)
                focus_df["Index_Values"] = focus_df.index.tolist()

                # Find Closest Postal Code To Focus Centroid
                focus_df["D_To_C"] = focus_df.apply(lambda row: geodesic(centroid_location, geopy.Point(row["Latitude"], row["Longitude"])), axis=1)
                val_list = focus_df["D_To_C"].tolist()

                # Find Min Distance
                place_holder = str(min(val_list))
                place_holder = place_holder.split(" ")
                min_distance_value = float(place_holder[0])

                # To Solve Bounding Box Issue Only Take Answers That Are Smaller Than The Min Distance
                if min_distance_value > min_distance:
                    raise ValueError
                else:
                    pass

                # If Everything Checks Out Break This While Loop
                break

            # If A Value Error Is Detected Iteratively Increase Distance By 1 KM Until Code Works
            except ValueError:
                distance_km += 1.5
                min_distance += 1.5

        # Reset The Value Of distance_km
        distance_km = initial_distance
        min_distance = initial_min_distance

        # Find The Index Value & Convert To Postal Code
        min_index = int(val_list.index(min_distance_value))
        focus_df.reset_index(inplace = True)
        min_index_index_vals = focus_df["Index_Values"][min_index]

        # Append The Needed Information
        closest_pc_list.append(pc_df["PostalCode"][min_index_index_vals])
        focus_lat_list.append(pc_df["Latitude"][min_index_index_vals])
        focus_long_list.append(pc_df["Longitude"][min_index_index_vals])

        # Monitor Progress
        print("Progress: " + str(counter_x) + "/" + str(centroid_df_len) + ", Postal Code: " + pc_df["PostalCode"][min_index_index_vals] + ", Distance: " + str(round(min_distance_value, 4)) + " km")

        # Del Column Just Created
        focus_df.drop(["D_To_C"], axis=1)

        # Add To Counter
        counter_x += 1

    centroid_df["Closest_PC"] = closest_pc_list
    centroid_df["P_Latitude"] = focus_lat_list
    centroid_df["P_Longitude"] = focus_long_list

    # Save As CSV
    centroid_df.to_csv(r"C:\Users\renac\Documents\Programming\Python\GasBuddy_DataParse\Data\GB_C_2KM\Closest_PC.csv", index=False)

    # Total Time
    print("Total Time: " + str(round((time.time() - start_time), 4)) + " Seconds")

# # This Function Will Parse Data From GasBuddy.com
# def web_scraper(postal_code, fuel_grade):
#     path = r"C:\Users\renac\Documents\Programming\Python\Selenium\chromedriver"
#     web_url = "https://www.gasbuddy.com/home?search=" + postal_code + "&fuel=" + str(fuel_grade)
#
#     # opts = Options()
#     # opts.set_headless()
#     # assert opts.headless
#
#     # Access WebPage
#     chrome = webdriver.Chrome(executable_path=path) #, options=opts
#     chrome.get(web_url)
#
#     # Access HTML For BS4
#     html = chrome.page_source
#     soup = BeautifulSoup(html, features="lxml")
#
#     # Parse The Search Radius Of The List
#     max_distance = 1.5
#     data = soup.find_all("div", class_="styles__stationListItem___xKFP_")
#     last_result = data[-1]
#     result = str(last_result)
#     distance = re.search('class=\"styles__distanceContainer___3BcX0\">(.*)km', result).group(1)
#
#         if float(distance) > max_distance:
#             max_distance = distance
#
#         else:
#             # Find Load More & Click
#
#     print(distance)
#     time.sleep(10)
#
#     time.sleep(10)
#     chrome.close()

# ----------------------------------------------------------------------------------------------------------------------
