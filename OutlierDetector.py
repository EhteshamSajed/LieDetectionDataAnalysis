import statistics
import numpy as np
import pandas as pd

n = 5
zero_zone_range = 3

def remove_outliers(value_list, linear_interpolation):
    threshold = get_threshold(max_absolute_change(
        value_list), median_absolute_deviation(value_list))
    out_value_list = []
    i = 0
    while i < len(value_list)-1:
        if abs(value_list[i] - value_list[i+1]) > threshold:
            out_value_list.append(0)
        else:
            out_value_list.append(value_list[i])
        i = i+1
    out_value_list.append(value_list[i])
    extend_zero_zone(out_value_list)
    if (linear_interpolation):
        out_value_list = linear_interpolate(out_value_list)
    return out_value_list

def extend_zero_zone(out_value_list):
    i = 0    
    while i < len(out_value_list)-zero_zone_range:
        try:
            start = i+1
            i = out_value_list.index(0, start, start+zero_zone_range)
            bounds = (start, i)
            out_value_list[bounds[0]:bounds[1] + 1] = [0] * ((bounds[1] + 1) - bounds[0])
        except ValueError:
            i += zero_zone_range+1
    return out_value_list

def get_threshold(mac, mad):
    return (statistics.median(mac) + n * mad)


def max_absolute_change(val_list):
    out_list = []
    out_list.append(abs(val_list[1]-val_list[0]))
    i = 1
    while i < len(val_list)-1:
        out_list.append(
            max(abs(val_list[i+1]-val_list[i]), abs(val_list[i]-val_list[i-1])))
        i = i + 1
    out_list.append(abs(val_list[i-2]-val_list[i-1]))
    return out_list


def median_absolute_deviation(val_list):
    mac = max_absolute_change(val_list)
    median = statistics.median(mac)
    mad_list = []
    for val in mac:
        mad_list.append(abs(val - median))
    return statistics.median(mad_list)


def relative_position_on_removed_outiler(filtered_value_list, original_position):
    if original_position >= len(filtered_value_list):
        return -1
    i = 0
    while i <= original_position:
        if filtered_value_list[i] == 0:
            original_position -= 1
        i += 1
    return original_position


def linear_interpolate(value_list):
    value_list = np.array(value_list)
    value_list = np.where(value_list==0 , np.nan, value_list)
    return pd.Series(value_list).interpolate().dropna().array
    
