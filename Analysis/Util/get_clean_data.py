import sys
sys.path.append('/home/ardelalegre/SoundMapping/Analysis/Util')
sys.path.append('/home/ardelalegre/SoundMapping/Database')
from DatabaseAPI import DatabaseAPI
import numpy as np
from get_time_interval_data import *
import pickle

def get_V6_data():
    
    # # Table calibration points
    CP1 = get_time_interval_matrix_data("May 12 2021 9:35AM", "May 12 2021 9:36AM")
    CP1_trimmed = CP1[400:800,:]
    CP2 = get_time_interval_matrix_data("May 12 2021 9:36AM", "May 12 2021 9:37AM")
    CP2_trimmed = CP2[530:,:]
    CP3 = get_time_interval_matrix_data("May 12 2021 9:37AM", "May 12 2021 9:38AM")
    CP3_trimmed = CP3[400:800,:]
    CP4 = get_time_interval_matrix_data("May 12 2021 9:38AM", "May 12 2021 9:39AM")
    CP4_trimmed = CP4[400:800,:]
    CP5 = get_time_interval_matrix_data("May 12 2021 10:11AM", "May 12 2021 10:13AM")
    CP5_trimmed = CP5[400:800,:]
    CP6 = get_time_interval_matrix_data("May 12 2021 10:13AM", "May 12 2021 10:14AM")
    CP6_trimmed = CP6[400:800,:]
    CP7 = get_time_interval_matrix_data("May 12 2021 9:25AM", "May 12 2021 9:26AM")
    CP7_trimmed = CP7[500:800,:]
    CP8 = get_time_interval_matrix_data("May 12 2021 10:40AM", "May 12 2021 10:41AM")
    CP8_trimmed = CP8[200:600,:]
    CP9 = get_time_interval_matrix_data("May 12 2021 10:28AM", "May 12 2021 10:29AM")
    CP9_trimmed = CP9[400:800,:]
    CP10 = get_time_interval_matrix_data("May 12 2021 9:40AM", "May 12 2021 9:41AM")
    CP10_trimmed = CP10[500:800,:]
    CP11 = get_time_interval_matrix_data("May 12 2021 10:14AM", "May 12 2021 10:15AM")
    CP11_trimmed = CP11[250:550,:]

    cp_tmp =[CP1_trimmed,CP2_trimmed,CP3_trimmed,CP4_trimmed,CP5_trimmed,CP6_trimmed,CP7_trimmed,CP8_trimmed,CP9_trimmed,CP10_trimmed,CP11_trimmed]
    CP_LIST = []
    for item in cp_tmp:
        cp_DOA, _ = extract_all_active_observations(item,[0,1,2,3,5])
        CP_LIST.append(cp_DOA)
        
    # L table slide
    L_table_slide = get_time_interval_matrix_data("May 13 2021 03:43PM", "May 13 2021 03:44PM")
    array_0_L_slide_1 = pickle.load(open('/home/ardelalegre/SoundMapping/Analysis/data/array_0_0513_L_slide_data_1.p','rb'))
    L_table_slide[:,1:4] = array_0_L_slide_1[:-1,:]
    active_L_table_slide_DOA, active_L_table_slide_matrix = extract_all_active_observations(L_table_slide[100:790,:],[0,1,2,3,5])
    # Long table slide
    long_table_slide = get_time_interval_matrix_data("May 13 2021 03:46PM", "May 13 2021 03:47PM")
    active_long_table_slide_DOA, active_long_table_slide_matrix = extract_all_active_observations(long_table_slide[120:460],[0,1,2,3,5])
    
    return CP_LIST, active_L_table_slide_DOA, active_L_table_slide_matrix, active_long_table_slide_DOA, active_long_table_slide_matrix


def get_V5_data():
    # Table calibration points
    L_table_cp1 = get_time_interval_matrix_data("Jan 27 2021 02:26PM", "Jan 27 2021 02:30PM")
    L_table_cp2 = get_time_interval_matrix_data("Jan 27 2021 02:30PM", "Jan 27 2021 02:34PM")
    long_table_cp = get_time_interval_matrix_data("Jan 27 2021 03:30PM", "Jan 27 2021 03:33PM")
    
    p1 = L_table_cp2[100:500,:]
    p2 = L_table_cp2[1500:1800,:]
    # patch array 0
    p2[:,1:4] = L_table_cp1[1300:1600,1:4]
    p3 = L_table_cp2[2000:2500,:]
    p4 = L_table_cp2[2900:3200,:]
    array_3_p4 = pickle.load(open('/home/ardelalegre/SoundMapping/Analysis/data/array_3_p4_data.p','rb'))
    # patch array 3
    p4[:,10:13] = array_3_p4
    p5 = long_table_cp[500:900,:]
    p6 = long_table_cp[2000:2400,:]
    # p12 = long_table_cp[1100:1600,:]
    
    
    # Chair calibration points
    chair_cp = pickle.load(open('/home/ardelalegre/SoundMapping/Analysis/data/chairs_cleaned.p','rb'))
    p7 = chair_cp[:400,:]
    p8 = chair_cp[500:1000,:]
    p9 = chair_cp[1350:1750,:]
    p10 = chair_cp[2000:2400,:]
    p11 = chair_cp[2700:,:]
    
    cp_tmp = [p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11]
    CP_LIST = []
    for item in cp_tmp:
        cp_DOA, _ = extract_all_active_observations(item,[0,1,2,3,5])
        CP_LIST.append(cp_DOA)

    # L table slide
    L_table_slide = get_time_interval_matrix_data("Jan 29 2021 04:50PM", "Jan 29 2021 04:52PM")
    active_L_table_slide_DOA, active_L_table_slide_matrix = extract_all_active_observations(L_table_slide[:870,:],[0,1,2,3,5])
    # Long table slide
    long_table_slide = get_time_interval_matrix_data("Jan 02 2021 03:05PM", "Jan 02 2021 03:06PM")
    active_long_table_slide_DOA, active_long_table_slide_matrix = extract_all_active_observations(long_table_slide, [0,1,2,3,5])
    
    return CP_LIST, active_L_table_slide_DOA, active_L_table_slide_matrix, active_long_table_slide_DOA, active_long_table_slide_matrix