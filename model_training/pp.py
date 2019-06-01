# 2019 Hackathon ML Ericsson
import os
import re
import math
import datetime

csv_records_list = []
training_csv_file_directory = './challenge2_sorted.csv'
weights_file_directory = "weights.txt"
test_result_filepath_prefix = "./test/test_"
dict_for_cbwd = {'NW':1, "NE":2, "SE":3, "cv":4}

learning_rate = 0.05
threshold = 15
w_DEWP, w_TEMP, w_PRES, w_cbwd, w_iws, w_is, w_ir = 0,0,0,0,0,0,0
weight_list = [0,0,0,0,0,0,0.16,0.16,0.16,0.16,0.16,0.1,0.1]
predicated_pm_for_next_hour = 0
predicated_list = [0]
current_pm_for_this_hour = 0
year = 0
month = 0
day = 0
hour = 0

weight_index = 6

def training(csv_records_list):
    
    i = 0
    while i < len(csv_records_list)-2:
        if csv_records_list[i+1][5] is None:
            if csv_records_list[i+2][5] is None:
                i += 1
                continue
            else:
                trainingData(csv_records_list[i], csv_records_list[i+2], weight_list, predicated_pm_for_next_hour, weight_index)
        else:
            trainingData(csv_records_list[i], csv_records_list[i+1], weight_list, predicated_pm_for_next_hour, weight_index)
        i += 1
    
    if csv_records_list[i+1][5] is not None:
        trainingData(csv_records_list[i], csv_records_list[i+1], weight_list, predicated_pm_for_next_hour, weight_index)
    persist_weights(weight_list,trained_weights_file)



def trainingData(record_current, record_next, weight_list, predicated_pm_for_next_hour, weight_index):
    global threshold
    global learning_rate
    global predicated_list
    
    while weight_index < len(record_current):
        if weight_index == 8:
            predicated_pm_for_next_hour += (record_current[weight_index]-1000) * weight_list[weight_index]
        elif weight_index == 9:
            predicated_pm_for_next_hour += dict_for_cbwd.get(record_current[weight_index]) * weight_list[weight_index]
        else:
            predicated_pm_for_next_hour += record_current[weight_index] * weight_list[weight_index]
        
        weight_index += 1
    
    predicated_list.append(predicated_pm_for_next_hour)
    print(predicated_pm_for_next_hour)
        
    if abs(predicated_pm_for_next_hour - record_next[5]) > threshold:
        error = predicated_pm_for_next_hour - record_next[5]

        weight_index = 6
        while weight_index < len(record_current):
            if weight_index == 8:
                weight_list[weight_index] = weight_list[weight_index] + error * learning_rate * (record_current[weight_index] - 1000)
            elif weight_index == 9:
                weight_list[weight_index] = weight_list[weight_index] + error * learning_rate * dict_for_cbwd.get(record_current[weight_index])
            else:
                weight_list[weight_index] = weight_list[weight_index] + error * learning_rate * record_current[weight_index]
            weight_index += 1
    

def convert_to_float_otherwise_none_or_string(input):
    try:
        return float(input)
    except ValueError:
        if len(input) == 0:
            return None
        else:
            return str(input)

def read_data_file(file_directory):
    records_list = []
    f = open(file_directory, "r", encoding="iso8859_2")
    lines = f.read().splitlines()
    for line in lines:
        one_record_list = re.split(",", line)
        if(len(one_record_list[0]) == 0):
            continue
        for i in range(5,len(one_record_list)):
            one_record_list[i] = convert_to_float_otherwise_none_or_string(one_record_list[i])
        records_list.append(one_record_list)
    f.close()
    return records_list

def persist_weights(weights_lst, file_directory):
    f = open(file_directory, "w")
    line = ','.join(weights_lst)
    f.write(line)
    f.close()

def test_model(test_records_list, weights_file_directory, test_result_filepath_prefix):
    predicted_pm = 0
    difference = 0
    is_below_threshhold = False

    f = open(weights_file_directory, "r", encoding="iso8859_2")
    line = f.readline(1)
    weights = re.split(',', line)
    f.close()

    weights_anchor, record_anchor = 0, 6
    test_result_file_directory = test_result_filepath_prefix + datetime.datetime.now
    f = open(test_result_file_directory, "w", encoding="iso8859_2")
    for i in range(len(test_records_list)):
        try:
            record = test_records_list[i]
            predicted_pm = convert_to_float_otherwise_none_or_string(weights[weights_anchor]) * record[record_anchor] + \
            convert_to_float_otherwise_none_or_string(weights[weights_anchor + 1]) * record[record_anchor + 1] + \
            convert_to_float_otherwise_none_or_string(weights[weights_anchor + 2]) * record[record_anchor + 2] + \
            convert_to_float_otherwise_none_or_string(weights[weights_anchor + 3]) * record[record_anchor + 3] + \
            convert_to_float_otherwise_none_or_string(weights[weights_anchor + 4]) * record[record_anchor + 4] + \
            convert_to_float_otherwise_none_or_string(weights[weights_anchor + 5]) * record[record_anchor + 5] + \
            convert_to_float_otherwise_none_or_string(weights[weights_anchor + 6]) * record[record_anchor + 6]

            difference = abs(predicted_pm - test_records_list[i+1][5])
            if difference <= threshold:
                is_below_threshhold = True
            else:
                is_below_threshhold = False
                record.extend(list(predicted_pm, difference, is_below_threshhold))
                f.write(",".join(record))
        except Exception:
            continue
    f.close()


csv_records_list = read_data_file(training_csv_file_directory)
training(csv_records_list)
test_model(csv_records_list[200:500],weights_file_directory, test_result_filepath_prefix)