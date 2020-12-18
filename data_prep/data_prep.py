# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 18:13:32 2020

@author: freddy
Create a JSON file, containing date, time and corresponding weight matrix.

"""

import pandas as pd
import os


if __name__ == "__main__":
    data = pd.read_csv("../data/biketrip_data.csv")

    data_agg = data[["start_station_id", "end_station_id", "hour_from", "date_from"]]
    data_agg["n"] = 1
    data_agg_detail = data_agg.groupby(
        ["start_station_id", "end_station_id", "date_from", "hour_from"]
    ).sum()
    data_agg_detail = data_agg_detail.reset_index()

    for time in data_agg_detail["hour_from"].unique():  # for every time
        directory = "../data/" + str(time)
        if not os.path.exists(directory):
            os.makedirs(directory)
        filtered_data = data_agg_detail[
            data_agg_detail["hour_from"] == time
        ]  # filter day
        for date in data_agg_detail["date_from"].unique():  # for every time
            filtered_data_time = filtered_data[
                filtered_data["date_from"] == date
            ]  # filter time
            # create the matrix
            matrix = pd.crosstab(
                index=filtered_data_time["start_station_id"],
                columns=filtered_data_time["end_station_id"],
                values=filtered_data_time["n"],
                aggfunc="sum",
            )
            filename = directory + "/" + str(date) + ".csv"
            matrix.to_csv(filename)
