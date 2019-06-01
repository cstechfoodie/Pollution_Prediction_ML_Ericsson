# 2019 Hackathon ML Ericsson

csv_records_list = []
training_csv_filepath = './challenge2_sorted.csv'
trained_weights_file = "weights.txt"
test_result_filepath_prefix = "./test_"
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
    

