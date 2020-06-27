import pandas as pd
import numpy as np
from putemg_features import biolab_utilities
import putemg_features
from putemg_features import biolab_utilities
import time 
from pathlib import Path
import statistics

#filtering_time = []
feature_calc_time = []
total_processing_time = []
#Load test subject data.=======================================
data_files = sorted(Path('.').glob('**/*repeats_short*.hdf5'))
#print(data_files)
#data = pd.read_hdf('../Data-HDF5/emg_gestures-03-repeats_short-2018-05-11-11-15-21-403.hdf5')

for test_subject_trial in range(88):
    print('\n' + 'Loaded data for test subject trial number ' + str(test_subject_trial))
    print(str(data_files[test_subject_trial]))
    data = pd.read_hdf(str(data_files[test_subject_trial]))
    #print(data)

#Only keep gesture values for flexion, extension and idle.====================================
    print('\n' + 'Removing values for unused gestures.')
    data.drop(data.loc[data['TRAJ_GT']==1].index, inplace=True)
    data.drop(data.loc[data['TRAJ_GT']==2].index, inplace=True)
#Search for initial index of data to keep.
    prev_gesture = -1
    current_gesture = -1
    count = 0
    for gesture in range(len(list(data['TRAJ_GT']))):
        current_gesture = data.iloc[gesture]['TRAJ_GT']
        if prev_gesture == -1 and current_gesture == 0:
            count += 1
            if count == 3:#Set to 3 to include only signals from wrist extension.
                initial_cutoff_index = gesture
                break
        prev_gesture = data.iloc[gesture]['TRAJ_GT']
#Keep data based on its indices.
    data = data.iloc[initial_cutoff_index:len(list(data['TRAJ_GT'])) - 1 - list(data['TRAJ_GT'])[::-1].index(3),:]#index set to 3 to include only signals related to wrist extension.
    data.drop(data.loc[data['TRAJ_GT']==-1].index, inplace=True)
    data.to_csv(r'raw_wrist_extension.txt')

#Only keep data for 8 EMG channels.
    data.drop(columns=['RMS_1',
 'RMS_2',
 'RMS_3',
 'RMS_4',
 'RMS_5',
 'RMS_6',
 'RMS_7',
 'RMS_8',
 'RMS_9',
 'RMS_10',
 'RMS_11',
 'RMS_12',
 'RMS_13',
 'RMS_14',
 'RMS_15',
 'RMS_16',
 'RMS_17',
 'RMS_18',
 'RMS_19',
 'RMS_20',
 'RMS_21',
 'RMS_22',
 'RMS_23',
 'RMS_24',
 'MAV_1',
 'MAV_2',
 'MAV_3',
 'MAV_4',
 'MAV_5',
 'MAV_6',
 'MAV_7',
 'MAV_8',
 'MAV_9',
 'MAV_10',
 'MAV_11',
 'MAV_12',
 'MAV_13',
 'MAV_14',
 'MAV_15',
 'MAV_16',
 'MAV_17',
 'MAV_18',
 'MAV_19',
 'MAV_20',
 'MAV_21',
 'MAV_22',
 'MAV_23',
 'MAV_24',
 'WL_1',
 'WL_2',
 'WL_3',
 'WL_4',
 'WL_5',
 'WL_6',
 'WL_7',
 'WL_8',
 'WL_17',
 'WL_18',
 'WL_19',
 'WL_20',
 'WL_21',
 'WL_22',
 'WL_23',
 'WL_24',
 'ZC_1',
 'ZC_2',
 'ZC_3',
 'ZC_4',
 'ZC_5',
 'ZC_6',
 'ZC_7',
 'ZC_8',
 'ZC_17',
 'ZC_18',
 'ZC_19',
 'ZC_20',
 'ZC_21',
 'ZC_22',
 'ZC_23',
 'ZC_24',
 'SSC_1',
 'SSC_2',
 'SSC_3',
 'SSC_4',
 'SSC_5',
 'SSC_6',
 'SSC_7',
 'SSC_8',
 'SSC_17',
 'SSC_18',
 'SSC_19',
 'SSC_20',
 'SSC_21',
 'SSC_22',
 'SSC_23',
 'SSC_24',
 'IAV_1',
 'IAV_2',
 'IAV_3',
 'IAV_4',
 'IAV_5',
 'IAV_6',
 'IAV_7',
 'IAV_8',
 'IAV_17',
 'IAV_18',
 'IAV_19',
 'IAV_20',
 'IAV_21',
 'IAV_22',
 'IAV_23',
 'IAV_24',
 'VAR_1',
 'VAR_2',
 'VAR_3',
 'VAR_4',
 'VAR_5',
 'VAR_6',
 'VAR_7',
 'VAR_8',
 'VAR_17',
 'VAR_18',
 'VAR_19',
 'VAR_20',
 'VAR_21',
 'VAR_22',
 'VAR_23',
 'VAR_24',
 'WAMP_1',
 'WAMP_2',
 'WAMP_3',
 'WAMP_4',
 'WAMP_5',
 'WAMP_6',
 'WAMP_7',
 'WAMP_8',
 'WAMP_17',
 'WAMP_18',
 'WAMP_19',
 'WAMP_20',
 'WAMP_21',
 'WAMP_22',
 'WAMP_23',
 'WAMP_24'], axis=1,inplace=True)

#Filter data.==========================================================
    print('\n' + 'Filtering data...')
    #start_time = time.time()
    biolab_utilities.apply_filter(data)
    #filtering_time.append(time.time() - start_time)
    #data.to_csv(r'filtered.txt')
    data.to_hdf(r'filtered_data_wrist_extension.hdf5', 'data', format='table', mode='w', complevel=5)

#Calculate features from filtered data.===========================================
    print('\n' + 'Calculating features...')
    start_time = time.time()
    ft: pd.DataFrame = putemg_features.features_from_xml('./features_shallow_learn.xml', r'filtered_data_wrist_extension.hdf5')
    feature_calc_time.append(time.time() - start_time)
    ft.to_hdf(r'data_features_wrist_extension.hdf5', 'data', format='table', mode='w', complevel=5)
    #data.to_csv(r'data_features.txt')
#Count number of gesture instances in data and find feature calculation rate.=================================
    num_of_gestures = (data['TRAJ_GT'].fillna(0).diff() !=0).sum() + 1
    print('\n' + str(num_of_gestures) + ' ' + 'gestures calculated.')
    feature_calc_rate = float(num_of_gestures)/feature_calc_time[test_subject_trial] #In gestures/second
    print('\n' + 'Feature calculation rate: '+ ' ' + str(round(feature_calc_rate, 2)) + 'gestures/s')

#Filtering time is negligible, since mean is less than 0.01s < interface feedback time of 0.1s noticeable to humans.
#So filtering time calculation not included in total processing time.
#Calculate filtering time per feature and total processing time per feature, where total_processing_time = filtering time per feature + 1/feature_calc_rate.==============
    #filtering_time_per_feature = filtering_time[test_subject_trial]/float(num_of_gestures)
    #total_processing_time.append(filtering_time_per_feature + 1.0/feature_calc_rate)
    total_processing_time.append(1.0/feature_calc_rate + 0.244)
    print('\n' + 'Total processing time per feature: '+ ' ' + str(total_processing_time[test_subject_trial]) + 's/gesture')

results = {
        0: "filtering_time",
        1: "feature_calc_time",
        2: "total_processing_time",
    }

print('\n' + 'Mean total processing time = ' + str(statistics.mean(total_processing_time)) + '+/-' + str(statistics.stdev(total_processing_time)) + 's/gesture')
#Write signal processing results to txt files.
for result in range(len(results)):
    results_file = open(results[result] +'_wrist_extension'+'.txt', 'w') 
    if result == 2:
        results_file.write('mean = ' + str(statistics.mean(total_processing_time)) +  '\n' + 'standard deviation = ' + str(statistics.stdev(total_processing_time)) + '\n')
    for test_subject_trial in range(88):
        #if result == 0:
        #    results_file.write(str(filtering_time[test_subject_trial]) + '\n') 
        if result == 1:
            results_file.write(str(feature_calc_time[test_subject_trial]) + '\n') 
        if result == 2:
            results_file.write(str(total_processing_time[test_subject_trial]) + '\n') 
    results_file.close()

