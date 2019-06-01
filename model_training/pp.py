# 2019 Hackathon ML Ericsson

csv_records_list = []
training_csv_filepath = './challenge2_sorted.csv'
trained_weights_file = "weights.txt"
test_result_filepath_prefix = "./test_"
dict_for_cbwd = {'NW':1, "NE":2, "SE":3, "cv":4}

learning_rate = 0.05
threshold = 15
w_DEWP, w_TEMP, w_PRES, w_cbwd, w_iws, w_is, w_ir = 0,0,0,0,0,0,0
predicated_pm_for_next_hour = 0
current_pm_for_this_hour = 0
year = 0
month = 0
day = 0
hour = 0
