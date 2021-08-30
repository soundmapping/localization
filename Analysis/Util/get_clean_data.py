import sys
rootDir = '../../'
sys.path.append(rootDir + 'Analysis/Util')
sys.path.append(rootDir + 'Database')
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

def try_get_data():
    # data1 = get_time_interval_matrix_data("Jul 07 2021 12:15PM", "Jul 07 2021 12:20PM")
    # data1 = get_time_interval_matrix_data("Jun 24 2021 08:00PM", "Jun 24 2021 08:05PM")
    # data2 = get_time_interval_matrix_data("Jul 20 2021 11:50PM", "Jul 20 2021 11:55PM")
    # data1 = get_time_interval_matrix_data("Jul 20 2021 03:10PM", "Jul 20 2021 03:15PM")

    x69_y69 = get_time_interval_matrix_data("Jul 21 2021 07:17PM", "Jul 21 2021 07:19PM")
    x0_y69 = get_time_interval_matrix_data("Jul 21 2021 07:21PM", "Jul 21 2021 07:23PM")
    x69_y0 = get_time_interval_matrix_data("Jul 21 2021 07:27PM", "Jul 21 2021 07:29PM")

    # Calibration Points
    cp1 = x69_y69[400:800, :]
    cp2 = x69_y69[800:1200, :]
    cp3 = x69_y69[1200:1600, :]

    cp4 = x0_y69[400:800, :]
    cp5 = x0_y69[800:1200, :]
    cp6 = x0_y69[1200:1600, :]

    cp7 = x69_y0[400:800, :]
    cp8 = x69_y0[800:1200, :]
    cp9 = x69_y0[1200:1600, :]

    cp_tmp = [cp1, cp2, cp3, cp4, cp5, cp6, \
            cp7, cp8, cp9]
    CP_LIST = []

    print("cp7 = ", cp7[300][:] )
    print("cp7 nan = ", np.isnan(cp7))
    print("cp7 0s", any(cp7[200,:]==0))

    ROOM_LIST = []

    print("For CP_LIST: ")
    for idx, item in enumerate(cp_tmp) :
        cp_DOA, _ = extract_all_active_observations(item, [1,2,5])

        if idx / 3 == 0 :
            roomCoordinates = np.empty([cp_DOA.shape[0], 2])
            roomCoordinates[:,0:2] = [70,70]
        
        if idx / 3 == 1 :
            roomCoordinates = np.empty([cp_DOA.shape[0], 2])
            roomCoordinates[:,0:2] = [1,70]

        if idx / 3 == 2 :
            roomCoordinates = np.empty([cp_DOA.shape[0], 2])
            roomCoordinates[:,0:2] = [70,1]

        CP_LIST.append(cp_DOA)
        ROOM_LIST.append(roomCoordinates)

    square = get_time_interval_matrix_data("Jul 21 2021 08:10PM", "Jul 21 2021 08:15PM")
    print("For Square: ")
    square_DOA, square_Matrix = extract_all_active_observations(square, [0,1]) 
    print("square = ", square[300][:] )
    print("square nan = ", np.isnan(square))
    print("square 0s", any(square[200,:]==0))

    return CP_LIST, ROOM_LIST, square_DOA, square_Matrix


def bigEnuf():
    # Creds: Big Enough - Jimmy Barnes  
    x69_y69 = get_time_interval_matrix_data("Jul 22 2021 08:51PM", "Jul 22 2021 08:54PM")
    x69_y0 = get_time_interval_matrix_data("Jul 22 2021 08:56PM", "Jul 22 2021 08:59PM")
    x0_y0 = get_time_interval_matrix_data("Jul 22 2021 09:01PM", "Jul 22 2021 09:04PM")
    x0_y69 = get_time_interval_matrix_data("Jul 22 2021 09:06PM", "Jul 22 2021 09:09PM")

    # Calibration Points
    cp1 = x69_y69[400:800, :]
    cp2 = x69_y69[800:1200, :]
    cp3 = x69_y69[1200:1600, :]

    cp4 = x69_y0[400:800, :]
    cp5 = x69_y0[800:1200, :]
    cp6 = x69_y0[1200:1600, :]

    cp7 = x0_y0[400:800, :]
    cp8 = x0_y0[800:1200, :]
    cp9 = x0_y0[1200:1600, :]

    cp10 = x0_y69[400:800, :]
    cp11 = x0_y69[800:1200, :]
    cp12 = x0_y69[1200:1600, :]

    # cp_tmp = [cp1, cp2, cp3, cp4, cp5, cp6, \
    #         cp7, cp8, cp9, cp10, cp11, cp12]

    cp_tmp = [cp1, cp2, cp3, cp4, cp5, cp6, \
            cp7, cp8, cp9]
    CP_LIST = []

    print("cp10 = ", cp10[300][:] )
    print("cp10 nan = ", np.isnan(cp10))
    print("cp10 0s", any(cp10[200,:]==0))

    ROOM_LIST = []

    print("For CP_LIST: ")
    for idx, item in enumerate(cp_tmp) :
        cp_DOA, _ = extract_all_active_observations(item, [0,3])

        if idx / 3 == 0 :
            roomCoordinates = np.empty([cp_DOA.shape[0], 2])
            roomCoordinates[:,0:2] = [70,70]
        
        if idx / 3 == 1 :
            roomCoordinates = np.empty([cp_DOA.shape[0], 2])
            roomCoordinates[:,0:2] = [70,1]

        if idx / 3 == 2 :
            roomCoordinates = np.empty([cp_DOA.shape[0], 2])
            roomCoordinates[:,0:2] = [1,1]

        # if idx / 3 == 3 :
        #     roomCoordinates = np.empty([cp_DOA.shape[0], 2])
        #     roomCoordinates[:,0:2] = [1,70]

        CP_LIST.append(cp_DOA)
        ROOM_LIST.append(roomCoordinates)

    square = get_time_interval_matrix_data("Jul 22 2021 09:10PM", "Jul 22 2021 09:15PM")
    print("square = ", square[300][:] )
    print("square nan = ", np.isnan(square))
    print("square 0s", any(square[200,:]==0))
    print("For Square: ")
    square_DOA, square_Matrix = extract_all_active_observations(square, [0,4]) 

    cp_all = np.vstack([x69_y69, x69_y0, x0_y0, x0_y69])

    return CP_LIST, ROOM_LIST, square_DOA, square_Matrix, square, cp_all

def bigEnufVertical():
    # Creds: Big Enough - Jimmy Barnes  
    x69_y69 = get_time_interval_matrix_data("Jul 25 2021 05:35PM", "Jul 25 2021 05:40PM")
    x69_y0 = get_time_interval_matrix_data("Jul 25 2021 05:40PM", "Jul 25 2021 05:45PM")
    x0_y0 = get_time_interval_matrix_data("Jul 25 2021 05:50PM", "Jul 25 2021 05:55PM")
    x0_y69 = get_time_interval_matrix_data("Jul 25 2021 05:55PM", "Jul 25 2021 06:00PM")

    # Calibration Points
    cp1 = x69_y69[400:800, :]
    cp2 = x69_y69[800:1200, :]
    cp3 = x69_y69[1200:1600, :]

    cp4 = x69_y0[400:800, :]
    cp5 = x69_y0[800:1200, :]
    cp6 = x69_y0[1200:1600, :]

    cp7 = x0_y0[400:800, :]
    cp8 = x0_y0[800:1200, :]
    cp9 = x0_y0[1200:1600, :]

    cp10 = x0_y69[400:800, :]
    cp11 = x0_y69[800:1200, :]
    cp12 = x0_y69[1200:1600, :]

    cp_tmp = [cp1, cp2, cp3, cp4, cp5, cp6, \
            cp7, cp8, cp9, cp10, cp11, cp12]

    # cp_tmp = [cp1, cp2, cp3, cp4, cp5, cp6, \
    #         cp7, cp8, cp9]
    CP_LIST = []

    print("cp10 = ", cp10[300][:] )
    print("cp10 nan = ", np.isnan(cp10))
    print("cp10 0s", any(cp10[200,:]==0))

    ROOM_LIST = []

    print("For CP_LIST: ")
    for idx, item in enumerate(cp_tmp) :
        cp_DOA, _ = extract_all_active_observations(item, [0,1,2,3,4,5])

        if idx / 3 == 0 :
            roomCoordinates = np.empty([cp_DOA.shape[0], 2])
            roomCoordinates[:,0:2] = [70,70]
        
        if idx / 3 == 1 :
            roomCoordinates = np.empty([cp_DOA.shape[0], 2])
            roomCoordinates[:,0:2] = [70,1]

        if idx / 3 == 2 :
            roomCoordinates = np.empty([cp_DOA.shape[0], 2])
            roomCoordinates[:,0:2] = [1,1]

        if idx / 3 == 3 :
            roomCoordinates = np.empty([cp_DOA.shape[0], 2])
            roomCoordinates[:,0:2] = [1,70]

        CP_LIST.append(cp_DOA)
        ROOM_LIST.append(roomCoordinates)

    square = get_time_interval_matrix_data("Jul 25 2021 06:01PM", "Jul 25 2021 06:05PM")
    print("square = ", square[300][:] )
    print("square nan = ", np.isnan(square))
    print("square 0s", any(square[200,:]==0))
    print("For Square: ")
    square_DOA, square_Matrix = extract_all_active_observations(square, [0,1,2,3,4,5]) 

    cp_all = np.vstack([x69_y69, x69_y0, x0_y0, x0_y69])

    return CP_LIST, ROOM_LIST, square_DOA, square_Matrix, square, cp_all

def bigEnufBigRoom():
    # Creds: Big Enough - Jimmy Barnes  
    x0_y69 = get_time_interval_matrix_data("Jul 26 2021 09:00PM", "Jul 26 2021 09:05PM")
    x69_y69 = get_time_interval_matrix_data("Jul 26 2021 09:05PM", "Jul 26 2021 09:10PM")
    x69_y0 = get_time_interval_matrix_data("Jul 26 2021 09:10PM", "Jul 26 2021 09:15PM")
    x0_y0 = get_time_interval_matrix_data("Jul 26 2021 09:15PM", "Jul 26 2021 09:20PM")
    
    # Calibration Points
    cp1 = x69_y69[400:800, :]
    cp2 = x69_y69[800:1200, :]
    cp3 = x69_y69[1200:1600, :]

    cp4 = x69_y0[400:800, :]
    cp5 = x69_y0[800:1200, :]
    cp6 = x69_y0[1200:1600, :]

    cp7 = x0_y0[400:800, :]
    cp8 = x0_y0[800:1200, :]
    cp9 = x0_y0[1200:1600, :]

    cp10 = x0_y69[400:800, :]
    cp11 = x0_y69[800:1200, :]
    cp12 = x0_y69[1200:1600, :]

    cp_tmp = [cp1, cp2, cp3, cp4, cp5, cp6, \
            cp7, cp8, cp9, cp10, cp11, cp12]

    # cp_tmp = [cp1, cp2, cp3, cp4, cp5, cp6, \
    #         cp7, cp8, cp9]
    CP_LIST = []

    # Debugging Purposes
    print("cp1 = ", cp1[300][:] )
    print("cp1 nan = ", np.isnan(cp1))
    print("cp1 0s", any(cp1[200,:]==0))

    print("cp4 = ", cp4[300][:] )
    print("cp4 nan = ", np.isnan(cp4))
    print("cp4 0s", any(cp4[200,:]==0))

    print("cp7 = ", cp7[300][:] )
    print("cp7 nan = ", np.isnan(cp7))
    print("cp7 0s", any(cp7[200,:]==0))

    print("cp10 = ", cp10[300][:] )
    print("cp10 nan = ", np.isnan(cp10))
    print("cp10 0s", any(cp10[200,:]==0))

    ROOM_LIST = []

    print("For CP_LIST: ")
    for idx, item in enumerate(cp_tmp) :
        cp_DOA, _ = extract_all_active_observations(item, [0,1,5])
        print("idx = ", idx, " w/ type: ", type(idx))

        if int(idx / 3) == 0 :
            roomCoordinates = np.empty([1, 2])
            roomCoordinates[:,0:2] = [70,70]
        
        if int(idx / 3) == 1 :
            roomCoordinates = np.empty([1, 2])
            roomCoordinates[:,0:2] = [70,1]

        if int(idx / 3) == 2 :
            roomCoordinates = np.empty([1, 2])
            roomCoordinates[:,0:2] = [1,1]

        if int(idx / 3) == 3 :
            roomCoordinates = np.empty([1, 2])
            roomCoordinates[:,0:2] = [1,70]

        CP_LIST.append(cp_DOA)
        ROOM_LIST.append(roomCoordinates)

    square = get_time_interval_matrix_data("Jul 26 2021 09:20PM", "Jul 26 2021 09:25PM")
    print("square = ", square[800][:] )
    print("square nan = ", np.isnan(square))
    print("square 0s", any(square[200,:]==0))
    print("For Square: ")
    square_DOA, square_Matrix = extract_all_active_observations(square, [0,1,2,3]) 

    cp_all = np.vstack([x69_y69, x69_y0, x0_y0, x0_y69])

    return CP_LIST, ROOM_LIST, square_DOA, square_Matrix, square, cp_all

def bigEnufWideRoom():
    # Creds: Big Enough - Jimmy Barnes  
    x0_y0 = get_time_interval_matrix_data("Jul 28 2021 08:06AM", "Jul 28 2021 08:09AM")
    x0_y69 = get_time_interval_matrix_data("Jul 28 2021 08:11AM", "Jul 28 2021 08:14AM")
    x69_y69 = get_time_interval_matrix_data("Jul 28 2021 08:16AM", "Jul 28 2021 08:19AM")
    x69_y0 = get_time_interval_matrix_data("Jul 28 2021 08:21AM", "Jul 28 2021 08:24AM")
    
    
    # Calibration Points
    cp1 = x69_y69[400:800, :]
    cp2 = x69_y69[800:1200, :]
    cp3 = x69_y69[1200:1600, :]

    cp4 = x69_y0[400:800, :]
    cp5 = x69_y0[800:1200, :]
    cp6 = x69_y0[1200:1600, :]

    cp7 = x0_y0[400:800, :]
    cp8 = x0_y0[800:1200, :]
    cp9 = x0_y0[1200:1600, :]

    cp10 = x0_y69[400:800, :]
    cp11 = x0_y69[800:1200, :]
    cp12 = x0_y69[1200:1600, :]

    cp_tmp = [cp1, cp2, cp3, cp4, cp5, cp6, \
            cp7, cp8, cp9, cp10, cp11, cp12]

    # cp_tmp = [cp1, cp2, cp3, cp4, cp5, cp6, \
    #         cp7, cp8, cp9]
    CP_LIST = []

    # Debugging Purposes
    print("cp1 = ", cp1[300][:] )
    print("cp1 nan = ", np.isnan(cp1))
    print("cp1 0s", any(cp1[200,:]==0))

    print("cp4 = ", cp4[300][:] )
    print("cp4 nan = ", np.isnan(cp4))
    print("cp4 0s", any(cp4[200,:]==0))

    print("cp7 = ", cp7[300][:] )
    print("cp7 nan = ", np.isnan(cp7))
    print("cp7 0s", any(cp7[200,:]==0))

    print("cp10 = ", cp10[300][:] )
    print("cp10 nan = ", np.isnan(cp10))
    print("cp10 0s", any(cp10[200,:]==0))

    ROOM_LIST = []

    print("For CP_LIST: ")
    for idx, item in enumerate(cp_tmp) :
        cp_DOA, _ = extract_all_active_observations(item, [0,1,2,3])
        print("idx = ", idx, " w/ type: ", type(idx))

        if int(idx / 3) == 0 :
            roomCoordinates = np.empty([1, 2])
            roomCoordinates[:,0:2] = [70,70]
        
        if int(idx / 3) == 1 :
            roomCoordinates = np.empty([1, 2])
            roomCoordinates[:,0:2] = [70,1]

        if int(idx / 3) == 2 :
            roomCoordinates = np.empty([1, 2])
            roomCoordinates[:,0:2] = [1,1]

        if int(idx / 3) == 3 :
            roomCoordinates = np.empty([1, 2])
            roomCoordinates[:,0:2] = [1,70]

        CP_LIST.append(cp_DOA)
        ROOM_LIST.append(roomCoordinates)

    square = get_time_interval_matrix_data("Jul 28 2021 08:30AM", "Jul 28 2021 08:36AM")
    print("square = ", square[800][:] )
    print("square nan = ", np.isnan(square))
    print("square 0s", any(square[200,:]==0))
    print("For Square: ")
    square_DOA, square_Matrix = extract_all_active_observations(square, [0,1,2,3]) 

    center = get_time_interval_matrix_data("Jul 28 2021 08:37AM", "Jul 28 2021 08:43AM")
    print("center = ", center[800][:] )
    print("center nan = ", np.isnan(center))
    print("center 0s", any(center[200,:]==0))
    print("For Center: ")
    center_DOA, center_Matrix = extract_all_active_observations(center, [0,1,2,3,4,5])
    
    offRight = get_time_interval_matrix_data("Jul 28 2021 08:45AM", "Jul 28 2021 08:50AM")
    print("offRight = ", offRight[800][:] )
    print("offRight nan = ", np.isnan(offRight))
    print("offRight 0s", any(offRight[200,:]==0))
    print("For offRight: ")
    offRight_DOA, offRight_Matrix = extract_all_active_observations(offRight, [0,1,4,5])

    semiCircle = get_time_interval_matrix_data("Jul 28 2021 08:50AM", "Jul 28 2021 08:51AM")
    print("semiCircle = ", semiCircle[20][:] )
    print("semiCircle nan = ", np.isnan(semiCircle))
    print("semiCircle 0s", any(semiCircle[200,:]==0))
    print("For semiCircle: ")
    semiCircle_DOA, semiCircle_Matrix = extract_all_active_observations(semiCircle, [0,1,2,3,4,5])

    edgeSquare = get_time_interval_matrix_data("Jul 28 2021 08:51AM", "Jul 28 2021 08:53AM")
    print("edgeSquare = ", edgeSquare[800][:] )
    print("edgeSquare nan = ", np.isnan(edgeSquare))
    print("edgeSquare 0s", any(edgeSquare[200,:]==0))
    print("For edgeSquare: ")
    edgeSquare_DOA, edgeSquare_Matrix = extract_all_active_observations(edgeSquare, [0,1,2,3,4,5])

    cp_all = np.vstack([x69_y69, x69_y0, x0_y0, x0_y69])

    return CP_LIST, ROOM_LIST, square_DOA, square_Matrix, square, cp_all, \
        center_DOA, center_Matrix, offRight_DOA, offRight_Matrix, \
        semiCircle_DOA, semiCircle_Matrix, edgeSquare_DOA, edgeSquare_Matrix

def bigEnufTable():
    # Creds: Big Enough - Jimmy Barnes  
    dataBank = pickle.load(open("../notebooks/29Jul2021.p", "rb"))

    x0_y69 = dataBank["x0_y69"]
    x69_y69 = dataBank["x69_y69"]
    x69_y0 = dataBank["x69_y0"]
    x0_y0 = dataBank["x0_y0"]
    
    
    # Calibration Points
    cp1 = x69_y69[400:800, :]
    cp2 = x69_y69[800:1200, :]
    cp3 = x69_y69[1200:1600, :]

    cp4 = x69_y0[400:800, :]
    cp5 = x69_y0[800:1200, :]
    cp6 = x69_y0[1200:1600, :]

    cp7 = x0_y0[400:800, :]
    cp8 = x0_y0[800:1200, :]
    cp9 = x0_y0[1200:1600, :]

    cp10 = x0_y69[400:800, :]
    cp11 = x0_y69[800:1200, :]
    cp12 = x0_y69[1200:1600, :]

    cp_tmp = [cp1, cp2, cp3, cp4, cp5, cp6, \
            cp7, cp8, cp9, cp10, cp11, cp12]

    # cp_tmp = [cp1, cp2, cp3, cp4, cp5, cp6, \
    #         cp7, cp8, cp9]
    CP_LIST = []

    # Debugging Purposes
    print("cp1 = ", cp1[300][:] )
    print("cp1 nan = ", np.isnan(cp1))
    print("cp1 0s", any(cp1[200,:]==0))

    print("cp4 = ", cp4[300][:] )
    print("cp4 nan = ", np.isnan(cp4))
    print("cp4 0s", any(cp4[200,:]==0))

    print("cp7 = ", cp7[300][:] )
    print("cp7 nan = ", np.isnan(cp7))
    print("cp7 0s", any(cp7[200,:]==0))

    print("cp10 = ", cp10[200][:] )
    print("cp10 nan = ", np.isnan(cp10))
    print("cp10 0s", any(cp10[200,:]==0))

    ROOM_LIST = []

    print("For CP_LIST: ")
    for idx, item in enumerate(cp_tmp) :
        cp_DOA, _ = extract_all_active_observations(item, [0,1,3,4,5])

        if int(idx / 3) == 0 :
            roomCoordinates = np.empty([1, 2])
            roomCoordinates[:,0:2] = [70,70]
        
        if int(idx / 3) == 1 :
            roomCoordinates = np.empty([1, 2])
            roomCoordinates[:,0:2] = [70,1]

        if int(idx / 3) == 2 :
            roomCoordinates = np.empty([1, 2])
            roomCoordinates[:,0:2] = [1,1]

        if int(idx / 3) == 3 :
            roomCoordinates = np.empty([1, 2])
            roomCoordinates[:,0:2] = [1,70]

        CP_LIST.append(cp_DOA)
        ROOM_LIST.append(roomCoordinates)

    square = dataBank["square"]
    print("square = ", square[800][:] )
    print("square nan = ", np.isnan(square))
    print("square 0s", any(square[200,:]==0))
    print("For Square: ")
    square_DOA, square_Matrix = extract_all_active_observations(square, [0,1,2,3,4,5]) 

    table1 = dataBank["table1"]
    print("table1 = ", table1[800][:] )
    print("table1 nan = ", np.isnan(table1))
    print("table1 0s", any(table1[200,:]==0))
    print("For Center: ")
    table1_DOA, table1_Matrix = extract_all_active_observations(table1, [0,1,2,3,4,5])
    
    line = dataBank["line"]
    print("line = ", line[800][:] )
    print("line nan = ", np.isnan(line))
    print("line 0s", any(line[200,:]==0))
    print("For line: ")
    line_DOA, line_Matrix = extract_all_active_observations(line, [0,1,2,3,4,5])

    point = dataBank["point"]
    print("point = ", point[20][:] )
    print("point nan = ", np.isnan(point))
    print("point 0s", any(point[200,:]==0))
    print("For point: ")
    point_DOA, point_Matrix = extract_all_active_observations(point, [0,1,2,3,4,5])

    table2 = dataBank["table2"]
    print("table2 = ", table2[800][:] )
    print("table2 nan = ", np.isnan(table2))
    print("table2 0s", any(table2[200,:]==0))
    print("For table2: ")
    table2_DOA, table2_Matrix = extract_all_active_observations(table2, [0,1,2,3,4,5])

    cp_all = np.vstack([x69_y69, x69_y0, x0_y0, x0_y69])

    return CP_LIST, ROOM_LIST, square_DOA, square_Matrix, square, cp_all, \
        table1_DOA, table1_Matrix, line_DOA, line_Matrix, \
        point_DOA, point_Matrix, table2_DOA, table2_Matrix

def bigEnufSecondTable():
    # Creds: Big Enough - Jimmy Barnes  
    dataBank = pickle.load(open("../notebooks/1Aug2021.p", "rb"))

    x0_y69 = dataBank["x0_y69"]
    x69_y69 = dataBank["x69_y69"]
    x69_y0 = dataBank["x69_y0"]
    x0_y0 = dataBank["x0_y0"]
    
    xN69_y0 = dataBank["xN69_y0"]
    xN138_y0 = dataBank["xN138_y0"]
    xN138_y69 = dataBank["xN138_y69"]
    xN69_y69 = dataBank["xN69_y69"]
    
    # Calibration Points
    cp1 = x69_y69[400:800, :]
    cp2 = x69_y69[800:1200, :]
    cp3 = x69_y69[1200:1600, :]

    cp4 = x69_y0[400:800, :]
    cp5 = x69_y0[800:1200, :]
    cp6 = x69_y0[1200:1600, :]

    cp7 = x0_y0[400:800, :]
    cp8 = x0_y0[800:1200, :]
    cp9 = x0_y0[1200:1600, :]

    cp10 = x0_y69[400:800, :]
    cp11 = x0_y69[800:1200, :]
    cp12 = x0_y69[1200:1600, :]

    cp13 = xN69_y0[400:800, :]
    cp14 = xN69_y0[800:1200, :]
    cp15 = xN69_y0[1200:1600, :] 

    cp16 = xN138_y0[400:800, :]
    cp17 = xN138_y0[800:1200, :]
    cp18 = xN138_y0[1200:1600, :]

    cp19 = xN138_y69[400:800, :]
    cp20 = xN138_y69[800:1200, :]
    cp21 = xN138_y69[1200:1600, :]

    cp22 = xN69_y69[400:800, :]
    cp23 = xN69_y69[800:1200, :]
    cp24 = xN69_y69[1200:1600, :]

    cp_tmp = [cp1, cp2, cp3, cp4, cp5, cp6, \
            cp7, cp8, cp9, cp10, cp11, cp12, \
            cp13, cp14, cp15, cp16, cp17, cp18, \
            cp19, cp20, cp21, cp22, cp23, cp24]

    # cp_tmp = [cp1, cp2, cp3, cp4, cp5, cp6, \
    #         cp7, cp8, cp9]
    CP_LIST = []

    # Debugging Purposes
    print("cp1 = ", cp1[300][:] )
    print("cp1 nan = ", np.isnan(cp1))
    print("cp1 0s", any(cp1[200,:]==0))

    print("cp4 = ", cp4[300][:] )
    print("cp4 nan = ", np.isnan(cp4))
    print("cp4 0s", any(cp4[200,:]==0))

    print("cp7 = ", cp7[300][:] )
    print("cp7 nan = ", np.isnan(cp7))
    print("cp7 0s", any(cp7[200,:]==0))

    print("cp10 = ", cp10[200][:] )
    print("cp10 nan = ", np.isnan(cp10))
    print("cp10 0s", any(cp10[200,:]==0))

    ROOM_LIST = []

    print("For CP_LIST: ")
    for idx, item in enumerate(cp_tmp) :
        cp_DOA, _ = extract_all_active_observations(item, [0,1,3,4,5])

        if int(idx / 3) == 0 :
            roomCoordinates = np.empty([1, 2])
            roomCoordinates[:,0:2] = [70,70]
        
        if int(idx / 3) == 1 :
            roomCoordinates = np.empty([1, 2])
            roomCoordinates[:,0:2] = [70,1]

        if int(idx / 3) == 2 :
            roomCoordinates = np.empty([1, 2])
            roomCoordinates[:,0:2] = [1,1]

        if int(idx / 3) == 3 :
            roomCoordinates = np.empty([1, 2])
            roomCoordinates[:,0:2] = [1,70]

        if int(idx / 3) == 4 :
            roomCoordinates = np.empty([1, 2])
            roomCoordinates[:,0:2] = [-68,1]

        if int(idx / 3) == 5 :
            roomCoordinates = np.empty([1, 2])
            roomCoordinates[:,0:2] = [-137,1]

        if int(idx / 3) == 6 :
            roomCoordinates = np.empty([1, 2])
            roomCoordinates[:,0:2] = [-137,70]

        if int(idx / 3) == 7 :
            roomCoordinates = np.empty([1, 2])
            roomCoordinates[:,0:2] = [-68,70]

        CP_LIST.append(cp_DOA)
        ROOM_LIST.append(roomCoordinates)

    square = dataBank["square"]
    print("square = ", square[800][:] )
    print("square nan = ", np.isnan(square))
    print("square 0s", any(square[200,:]==0))
    print("For Square: ")
    square_DOA, square_Matrix = extract_all_active_observations(square, [0,1,2,3,4,5]) 

    rectangle = dataBank["rectangle"]
    print("rectangle = ", rectangle[800][:] )
    print("rectangle nan = ", np.isnan(rectangle))
    print("rectangle 0s", any(rectangle[200,:]==0))
    print("For Rectangle: ")
    rectangle_DOA, rectangle_Matrix = extract_all_active_observations(rectangle, [0,1,2,3,4,5]) 

    table1 = dataBank["table1"]
    print("table1 = ", table1[800][:] )
    print("table1 nan = ", np.isnan(table1))
    print("table1 0s", any(table1[200,:]==0))
    print("For Center: ")
    table1_DOA, table1_Matrix = extract_all_active_observations(table1, [0,1,2,3,4,5])

    table2 = dataBank["table2"]
    print("table2 = ", table2[800][:] )
    print("table2 nan = ", np.isnan(table2))
    print("table2 0s", any(table2[200,:]==0))
    print("For table2: ")
    table2_DOA, table2_Matrix = extract_all_active_observations(table2, [0,1,2,3,4,5])

    table3 = dataBank["table3"]
    print("table3 = ", table3[800][:] )
    print("table3 nan = ", np.isnan(table3))
    print("table3 0s", any(table3[200,:]==0))
    print("For table3: ")
    table3_DOA, table3_Matrix = extract_all_active_observations(table3, [0,1,2,3,4,5])

    table4 = dataBank["table4"]
    print("table4 = ", table4[800][:] )
    print("table4 nan = ", np.isnan(table4))
    print("table4 0s", any(table4[200,:]==0))
    print("For table4: ")
    table4_DOA, table4_Matrix = extract_all_active_observations(table4, [0,1,2,3,4,5])

    cp_all = np.vstack([x69_y69, x69_y0, x0_y0, x0_y69, xN69_y0, xN138_y0, xN138_y69, xN69_y69])

    return CP_LIST, ROOM_LIST, square_DOA, square_Matrix, square, cp_all, \
        rectangle_DOA, rectangle_Matrix, \
        table1_DOA, table1_Matrix, table2_DOA, table2_Matrix, \
        table3_DOA, table3_Matrix, table4_DOA, table4_Matrix

# def main() :
#     CP_LIST, active_L_table_slide_DOA, active_L_table_slide_matrix, active_long_table_slide_DOA, active_long_table_slide_matrix = get_V5_data()
#     print("CP_LIST = ", CP_LIST,
#             "\n active_L_table_slide_DOA = ", active_L_table_slide_DOA,
#             "\n active_L_table_slide_matrix = ", active_L_table_slide_matrix,
#             "\n active_long_table_slide_DOA = ", active_long_table_slide_DOA,
#             "\n active_long_table_slide_matrix = ", active_long_table_slide_matrix)

def main() :
    tester = {}

    # Beeg Yosh
    # tester["cp_list"], tester["room_list"], \
    #     tester["square_DOA"], tester["square_Matrix"] = try_get_data()
    
    # with open("bigYosh.p", "wb") as handle :
    #     pickle.dump(tester, handle, protocol=pickle.HIGHEST_PROTOCOL)
    # print("\n data2 = \n", data2)

    # # Big Enough
    # tester["cp_list"], tester["room_list"], \
    #     tester["square_DOA"], tester["square_Matrix"], \
    #      tester["sqRaw"], tester["cpRaw"] = bigEnuf()
    
    # # with open("bigEnuf.p", "wb") as handle :
    # #     pickle.dump(tester, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # # Big Enough Vertical
    # tester["cp_list"], tester["room_list"], \
    #     tester["square_DOA"], tester["square_Matrix"], \
    #      tester["sqRaw"], tester["cpRaw"] = bigEnufVertical()
    
    # with open("bigEnufVertical.p", "wb") as handle :
    #     pickle.dump(tester, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # # Big Enough Beeg Room
    # tester["cp_list"], tester["room_list"], \
    #     tester["square_DOA"], tester["square_Matrix"], \
    #      tester["sqRaw"], tester["cpRaw"] = bigEnufBigRoom()
    
    # with open("bigEnufBigRoom.p", "wb") as handle :
    #     pickle.dump(tester, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # # Big Enough Wide Room
    # tester["cp_list"], tester["room_list"], \
    #     tester["square_DOA"], tester["square_Matrix"], \
    #      tester["sqRaw"], tester["cpRaw"], \
    #      tester["center_DOA"], tester["center_Matrix"], \
    #      tester["offRight_DOA"], tester["offRight_Matrix"], \
    #      tester["semiCircle_DOA"], tester["semiCircle_Matrix"], \
    #      tester["edgeSquare_DOA"], tester["edgeSquare_Matrix"] = bigEnufWideRoom()
    
    # with open("bigEnufWideRoom.p", "wb") as handle :
    #     pickle.dump(tester, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # # Big Enough Table
    # tester["cp_list"], tester["room_list"], \
    #     tester["square_DOA"], tester["square_Matrix"], \
    #      tester["sqRaw"], tester["cpRaw"], \
    #      tester["table1_DOA"], tester["table1_Matrix"], \
    #      tester["line_DOA"], tester["line_Matrix"], \
    #      tester["point_DOA"], tester["point_Matrix"], \
    #      tester["table2_DOA"], tester["table2_Matrix"] = bigEnufTable()
    
    # with open("bigEnufTable.p", "wb") as handle :
    #     pickle.dump(tester, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # Big Enough Second Table
    tester["cp_list"], tester["room_list"], \
        tester["square_DOA"], tester["square_Matrix"], \
         tester["sqRaw"], tester["cpRaw"], \
         tester["rectangle_DOA"], tester["rectangle_Matrix"], \
         tester["table1_DOA"], tester["table1_Matrix"], \
         tester["table2_DOA"], tester["table2_Matrix"], \
         tester["table3_DOA"], tester["table3_Matrix"], \
         tester["table4_DOA"], tester["table4_Matrix"] = bigEnufSecondTable()
    
    with open("bigEnufSecondTable.p", "wb") as handle :
        pickle.dump(tester, handle, protocol=pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__" :
    main()