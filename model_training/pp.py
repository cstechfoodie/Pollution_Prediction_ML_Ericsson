# 2019 Hackathon ML Ericsson
import os
import re
import math
import datetime
import math

csv_records_list = []
training_csv_file_directory = './challenge2_sorted.csv'
weights_file_directory = "weights.txt"
test_result_filepath_prefix = "./test_results/test_"
dict_for_cbwd = {'NW':1, "NE":2, "SE":3, "cv":4}

#The learning rate is : 5e-10
learning_rate = 0.00000000005
threshold = 25
#w_DEWP, w_TEMP, w_PRES, w_cbwd, w_iws, w_is, w_ir = 0,0,0,0,0,0,0
weight_list = [0,0,0,0,0,0,0.16,0.16,0.16,0.16,0.16,0.1,0.1]

weight_index = 6

def training(csv_records_list):
    
    i = 0
    while i < len(csv_records_list)-2:
        if csv_records_list[i+1][5] is None:
            if csv_records_list[i+2][5] is None:
                i += 1
                continue
            else:
                trainingData(csv_records_list[i], csv_records_list[i+2], weight_list, weight_index)
        else:
            trainingData(csv_records_list[i], csv_records_list[i+1], weight_list, weight_index)
        i += 1
    
    if csv_records_list[i+1][5] is not None:
        trainingData(csv_records_list[i], csv_records_list[i+1], weight_list, weight_index)
    persist_weights(weight_list,weights_file_directory)



def trainingData(record_current, record_next, weight_list, weight_index):
    global threshold
    global learning_rate
    predicated_pm_for_next_hour = 0
    
    while weight_index < len(record_current):
        if weight_index == 8:
            predicated_pm_for_next_hour += (record_current[weight_index]-1000) * weight_list[weight_index]
        elif weight_index == 9:
            predicated_pm_for_next_hour += dict_for_cbwd.get(record_current[weight_index]) * weight_list[weight_index]
        else:
            predicated_pm_for_next_hour += record_current[weight_index] * weight_list[weight_index]
        
        weight_index += 1
    #print("predicated_pm_for_next_hour : " , predicated_pm_for_next_hour)
        
    if abs(predicated_pm_for_next_hour - record_next[5]) > threshold:
        error = predicated_pm_for_next_hour - record_next[5]
        if error < 0:
            error = math.log(abs(error)) * (-1)
        else:
            error = math.log(error)
        error = 1
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
        if input is not None:
            return float(input)
        else: 
            return 0.0
    except ValueError:
        if input is None:
            return 0.0
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
    for j in range(len(weights_lst)):
        weights_lst[j] = str(weights_lst[j])
    f.write(','.join(weight_list))
    f.close()

def predict(inputs):
    inputs = re.split(",", inputs)
    for i in range(5,len(inputs)):
        inputs[i] = convert_to_float_otherwise_none_or_string(inputs[i])

    f = open(weights_file_directory, "r", encoding="iso8859_2")
    line = f.readline()
    weights = re.split(',', line)
    for i in range(len(weights)):
        weights[i] = float(weights[i])
    f.close()

    record_anchor = 6
    predicted_pm = float(weight_list[record_anchor]) * float(inputs[record_anchor]) + \
            float(weight_list[record_anchor + 1]) * float(inputs[record_anchor + 1]) + \
            float(weight_list[record_anchor + 2]) * float(inputs[record_anchor + 2]-1000) + \
            float(weight_list[record_anchor + 3]) * float(dict_for_cbwd.get(inputs[record_anchor + 3])) + \
            float(weight_list[record_anchor + 4]) * float(inputs[record_anchor + 4]) + \
            float(weight_list[record_anchor + 5]) * float(inputs[record_anchor + 5]) + \
            float(weight_list[record_anchor + 6]) * float(inputs[record_anchor + 6])
    return int(predicted_pm)

def test_model(test_records_list, weights_file_directory, test_result_filepath_prefix):
    global weight_list
    predicted_pm = 0
    difference = 0
    is_below_threshhold = False
    correct_estimate = 0
    incorrect_estimate = 0

    f = open(weights_file_directory, "r", encoding="iso8859_2")
    line = f.readline()
    weights = re.split(',', line)
    for i in range(len(weights)):
        weights[i] = float(weights[i])
    f.close()

    record_anchor = 6
    test_result_file_directory = test_result_filepath_prefix + str(datetime.datetime.now())
    f = open(test_result_file_directory, "w", encoding="iso8859_2")
    for i in range(len(test_records_list)):
        try:
            record = test_records_list[i]
            for i in range(len(record)):
                record[i] = convert_to_float_otherwise_none_or_string(record[i])
            predicted_pm = float(weights[record_anchor]) * float(record[record_anchor]) + \
            float(weights[record_anchor + 1]) * float(record[record_anchor + 1]) + \
            float(weights[record_anchor + 2]) * float(record[record_anchor + 2]-1000) + \
            float(weights[record_anchor + 3]) * float(dict_for_cbwd.get(record[record_anchor + 3])) + \
            float(weights[record_anchor + 4]) * float(record[record_anchor + 4]) + \
            float(weights[record_anchor + 5]) * float(record[record_anchor + 5]) + \
            float(weights[record_anchor + 6]) * float(record[record_anchor + 6])
            expected_pm = convert_to_float_otherwise_none_or_string(test_records_list[i+1][5])
            difference = abs(predicted_pm - expected_pm)
            if difference <= threshold:
                is_below_threshhold = True
                correct_estimate += 1
            else:
                is_below_threshhold = False
                incorrect_estimate += 1
            record.extend(list([predicted_pm, is_below_threshhold, difference]))
            for j in range(len(record)):
                record[j] = str(record[j])
            f.write(",".join(record) + '\r')
        except Exception:
            continue
    f.write("------------------------------Report----------------\r")
    f.write("The allowed differece between estimation and real is : " + str(threshold) + "\r")
    f.write("The learning rate is : " + str(learning_rate) + "\r")
    f.write("correct estimated is : " + str(correct_estimate) + "\r")
    f.write("incorrect estimated is : " + str(incorrect_estimate) + "\r")
    f.write("The accuracy is : " + str(correct_estimate/(correct_estimate+incorrect_estimate)) + "\r")
    f.close()


csv_records_list = read_data_file(training_csv_file_directory)
training(csv_records_list[10000:])
test_model(csv_records_list[0:10000],weights_file_directory, test_result_filepath_prefix)
intputs = "2656.0,2014.0,1.0,3.0,13.0,29.0,-17.0,9.0,1022.0,NW,22.35,0.0,0.0"
print(predict(intputs))