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

# ----------------------------------------------------------------------------------------------------------------------

# This Function Will Set Up Chrome
def set_up_chrome():
    ext_1 = r"C:\Users\renac\Documents\Programming\Python\Selenium\Extensions\uBlock-Origin_v1.14.8.crx"
    path = r"C:\Users\renac\Documents\Programming\Python\Selenium\chromedriver"

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_extension(ext_1)
    chrome_options.add_argument("--disable-infobars")
    chrome = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)

    return chrome

# This Function Will Parse Station IDs From GasBuddy.com
def id_scraper(postal_code, fuel_grade):

    chrome = set_up_chrome()
    web_url = "https://www.gasbuddy.com/home?search=" + postal_code + "&fuel=" + str(fuel_grade)
    chrome.get(web_url)

    while True:

        try:
            # Access HTML For BS4
            chrome.implicitly_wait(20)

            # Need To Wait For Page To Load Properly
            time.sleep(5)

            # Parse WebPage Data
            html = chrome.page_source
            soup = BeautifulSoup(html, features="lxml")

            # Find Search Radius
            distances = re.findall('>(.{3,4})km', str(soup))

            # If Search Distance Smaller Than 3.0KM Increase Search Distance
            if float(distances[-1]) >= float(3):

                # Get Station IDs, Append To List
                station_ids = re.findall('station/(\d{1,8})">', str(soup))

                # Check To See If Correct Number Parsed
                if len(station_ids) == len(distances):
                    pass

                else:
                    print("Not All Station IDs Parsed")
                    raise ValueError

                # Break Out Of While Loop With Data
                break

            else:
                # Find & Click Button
                try:
                    load_more_button = chrome.find_element_by_xpath('//*[@id="container"]/div/div[3]/div/div/div[1]/a')
                    load_more_button.click()

                except:
                    pass

        except:
            print("Error")
            break

    chrome.close()

    try:
        return station_ids
    except:
        station_ids = []
        return station_ids

# This Function Will Parse Data From The Station List Provided
def get_all_ids(postal_codes, fuel_type):

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
    df_ids_list = df_ids["IDS"].tolist()

    print("Stations Parsed: " + str(len(df_ids)) + ", Removed: " + str(post_len - len(df_ids)))

    df_ids.to_csv(r"C:\Users\renac\Documents\Programming\Python\GasBuddy_DataParse\Data\Raw_Data\Station_IDS.csv", index=False)
    print("\n" + "File Written To Disk")

    return df_ids_list

# This Function Will Parse The Data From Each Station Webpage
def parse_data(station_ids):

    # Set Up Chrome Driver
    chrome = set_up_chrome()
    general_path = "https://www.gasbuddy.com/station/"

    # Loop Through Each Station In Station_IDs List
    for station in station_ids:
        # Get Path
        url = general_path + str(station)
        chrome.get(url)

        # Wait For Page To Load
        time.sleep(0.5)

        # Parse General Desc Info
        station_desc = chrome.find_element_by_xpath('//*[@id="container"]/div/div[3]/div/div/div/div[1]/div[1]/div[2]')
        desc_blob = str(station_desc.text)

        # Clean Up General Info
        desc = desc_blob.replace("\n", " ")
        desc_list = desc.split(" ")

        # Get Number Of Reviews & Split Index
        review_num = re.findall("\((.*?)\)", desc)
        review_str = "(" + review_num[0] + ")"
        review_index = desc_list.index(review_str)

        # Get Name
        name = desc_list[:review_index]
        name = "".join(name)

        # Get Address
        address_data = desc_list[review_index + 1:-3]
        address = ""
        for val in address_data:
            address = address + val + " "

        # Get City
        city = desc_list[-3]
        city = city.replace(",", "")

        print("Station Name: {0}, Reviews: {1}, Address: {2}, City: {3}".format(name, review_num[0], address, city))

    chrome.close()



# ----------------------------------------------------------------------------------------------------------------------
