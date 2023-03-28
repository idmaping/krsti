'''
CATATAN
[V] BACA FILE MOTION
[V] PERPINDAHAN ANTAR MOTION

[V] XM430 MENGATUR POSISI
[V] XM430 MENGATUR KECEPATAN
[X] XM430 MENGATUR TORSI
[X] XM430 MENGATUR POSISI SYNC
[V] XM430 MEMBACA POSISI SYNC

[V] XL320 MENGATUR POSISI
[V] XL320 MENGATUR KECEPATAN
[X] XL320 MENGATUR TORSI
[X] XL320 MENGATUR POSISI SYNC
[ ] XL320 MEMBACA POSISI SYNC

LIST ERROR
There is no status packet =  kabel trouble

'''

import os
import numpy as np
import time
if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

from dynamixel_sdk import *                    # Uses Dynamixel SDK library

import csv




#INIT SERVO
PROTOCOL_VERSION = 2.0

XL320_ADDR_TORQUE_ENABLE = 24
XL320_ADDR_GOAL_POSITION = 30
XL320_ADDR_PRESENT_POSITION = 37
XL320_ADDR_PROFILE_VELOCITY = 32
XL320_LEN_GOAL_POSITION = 4                     
XL320_LEN_PRESENT_POSITION = 4 

XM430_ADDR_TORQUE_ENABLE = 64 
XM430_ADDR_GOAL_POSITION = 116
XM430_ADDR_PRESENT_POSITION = 132
XM430_ADDR_PROFILE_VELOCITY = 112
XM430_LEN_GOAL_POSITION = 4                      #!!!
XM430_LEN_PRESENT_POSITION = 4  

BAUDRATE = 1000000
DXL_MOVING_STATUS_THRESHOLD = 15.0

DEVICENAME                  = '/dev/ttyUSB0'

DXL_KEPALA = [0,1,2]
DXL_TANGAN_KANAN = [3,5,7,9,11,13] 
DXL_TANGAN_KIRI = [4,6,8,10,12,14] 
DXL_KAKI_KANAN = [15,17,19,21,23,25]
DXL_KAKI_KIRI = [16,18,20,22,24,26]
DXL_ALL = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26]
DXL_XM430 = [0,1,2,3,4,5,6,7,8,9,10,11,12]
DXL_XL320 = [13,14,15,16,17,18,19,20,21,22,23,24,25,26]

portHandler = PortHandler(DEVICENAME)
packetHandler = PacketHandler(PROTOCOL_VERSION)
groupSyncRead_XM430 = GroupSyncRead(portHandler, packetHandler, XM430_ADDR_PRESENT_POSITION, XM430_LEN_PRESENT_POSITION)
groupSyncRead_XL320 = GroupSyncRead(portHandler, packetHandler, XL320_ADDR_PRESENT_POSITION, XL320_LEN_PRESENT_POSITION)

MOTION_STEP = []
MOTION_TIME_XL320 = []
MOTION_TIME_XM430 = []
MOTION_DXL = []

#########################
### CODING KINEMATIKA ###
#########################

def constrain_degree(degree):
    if degree < 0:
        degree = degree+360
    if degree > 360:
        degree = degree-360

    return degree

def invert_degree(degree):
    return 360-degree

def hitung_kaki_kanan(x=0 -0.02, y=0 -0.015, z=-0.22 + 0.035, theta=180):
    L1 = 0.11
    L2 = 0.11
    L3 = math.sqrt(z**2 + x**2)

    DXL_7 = theta

    alpha1 = math.atan2(x,z) * convertToDegree
    alpha2 = math.acos( (L1**2 + L3**2 - L2**2) / (2*L1*L3) ) * convertToDegree
    DXL_11 = alpha1 + alpha2
    DXL_11 = constrain_degree(DXL_11)

    alpha3 = math.acos( (L1**2 + L2**2 - L3**2) / (2*L1*L2) ) * convertToDegree
    DXL_13 = alpha3
    DXL_13 = constrain_degree(DXL_13)

    alpha4 = math.atan2(-y,z) * convertToDegree
    DXL_9 = alpha4
    DXL_9 = constrain_degree(DXL_9)
    DXL_9 = invert_degree(DXL_9)

    alpha5 = 180 - DXL_11
    alpha6 = 180 - DXL_13
    DXL_15 = 180 - (alpha5 + alpha6)
    DXL_15 = constrain_degree(DXL_15)

    DXL_17 = DXL_9
    DXL_17 = constrain_degree(DXL_17)

    return int(DXL_7), int(DXL_9), int(DXL_11), int(DXL_13), int(DXL_15), int(DXL_17)
    
def hitung_kaki_kiri(x=0 -0.02, y=0 +0.015, z=-0.22 + 0.035, theta=180):
    L1 = 0.11
    L2 = 0.11
    L3 = math.sqrt(z**2 + x**2)

    DXL_6 = theta

    alpha1 = math.atan2(x,z) * convertToDegree
    alpha2 = math.acos( (L1**2 + L3**2 - L2**2) / (2*L1*L3) ) * convertToDegree
    DXL_12 = alpha1 + alpha2
    DXL_12 = constrain_degree(DXL_12)
    DXL_12 = invert_degree(DXL_12)

    alpha3 = math.acos( (L1**2 + L2**2 - L3**2) / (2*L1*L2) ) * convertToDegree
    DXL_14 = alpha3
    DXL_14 = constrain_degree(DXL_14)
    DXL_14 = invert_degree(DXL_14)

    alpha4 = math.atan2(-y,z) * convertToDegree
    DXL_10 = alpha4
    DXL_10 = constrain_degree(DXL_10)
    DXL_10 = invert_degree(DXL_10)

    alpha5 = 180 - DXL_12
    alpha6 = 180 - DXL_14
    DXL_16 = 180 - (alpha5 + alpha6)
    DXL_16 = constrain_degree(DXL_16)

    DXL_18 = DXL_10
    DXL_18 = constrain_degree(DXL_18)
    
    return int(DXL_6), int(DXL_10), int(DXL_12), int(DXL_14), int(DXL_16), int(DXL_18)

########################
### CODING DYNAMIXEL ###
########################

def enableTorque(DXL_GROUP,ENABLE):###BELUM XL
    for DXL_ID in DXL_GROUP:
        if DXL_ID in DXL_KAKI_KIRI or DXL_ID in DXL_KAKI_KANAN or DXL_ID == 13 or DXL_ID == 14:
            dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, XM430_ADDR_TORQUE_ENABLE, ENABLE)
            
        else:
            dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, XL320_ADDR_TORQUE_ENABLE, ENABLE)
        
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result), "on ID", DXL_ID)
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error), "on ID", DXL_ID)
        else:
            pass
            

def inisialisasi():
    # Open port
    if portHandler.openPort():
        print("Succeeded to open the port")
    else:
        print("Failed to open the port")
        print("Press any key to terminate...")
        getch()
        quit()

    # Set port baudrate
    if portHandler.setBaudRate(BAUDRATE):
        print("Succeeded to change the baudrate")
    else:
        print("Failed to change the baudrate")
        print("Press any key to terminate...")
        getch()
        quit()

    # Add parameter storage for Dynamixel present position value
    for DXL_ID in DXL_KAKI_KANAN + DXL_KAKI_KIRI + [13,14]:
        dxl_addparam_result = groupSyncRead_XM430.addParam(DXL_ID)
        if dxl_addparam_result != True:
            print("[ID:%03d] groupSyncRead_XM430 addparam failed" % DXL_ID)
            quit()

    
    for DXL_ID in DXL_TANGAN_KANAN[:-1] + DXL_TANGAN_KIRI[:-1] + DXL_KEPALA:
        dxl_addparam_result = groupSyncRead_XL320.addParam(DXL_ID)
        if dxl_addparam_result != True:
            print("[ID:%03d] groupSyncRead_XL320 addparam failed" % DXL_ID)
            quit()
    
def map(x , in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def setGoalPosition_single(DXL_ID, DEGREE):
    #1 dxl
    if DXL_ID in DXL_KAKI_KIRI or DXL_ID in DXL_KAKI_KANAN or DXL_ID == 13 or DXL_ID == 14:
        #print(DXL_ID," XM ",TIME)
        goal = map(DEGREE,0,360,0,4096)
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, XM430_ADDR_GOAL_POSITION, int(goal))
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result) , "on ID", DXL_ID)
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error) , "on ID", DXL_ID)

    else :
        #print(DXL_ID,"XL320",TIME)
        goal = map(DEGREE,0,300,0,1023)
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL_ID, XL320_ADDR_GOAL_POSITION, int(goal))
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result) , "on ID", DXL_ID)
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error) , "on ID", DXL_ID)

def setGoalPosition_group(DXL_GROUP, DEGREE_GROUP):
    for i in range(len(DXL_GROUP)):
        #print(DXL_GROUP[i], DEGREE_GROUP[i])
        setGoalPosition_single(int(DXL_GROUP[i]), int(DEGREE_GROUP[i]))

def setTime(DXL_GROUP,TIME_XL320,TIME_XM430):
    #1 grup dengan time yang sama
    for DXL_ID in DXL_GROUP:
        if DXL_ID in DXL_KAKI_KIRI or DXL_ID in DXL_KAKI_KANAN or DXL_ID == 13 or DXL_ID == 14:
            #print(DXL_ID,"XM430",TIME)
            addr = XM430_ADDR_PROFILE_VELOCITY
            dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, addr, int(TIME_XM430))
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % packetHandler.getTxRxResult(dxl_comm_result), "on ID", DXL_ID)
            elif dxl_error != 0:
                print("%s" % packetHandler.getRxPacketError(dxl_error), "on ID", DXL_ID)

        else:
            #print(DXL_ID,"XL320",TIME)
            addr = XL320_ADDR_PROFILE_VELOCITY
            dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL_ID, addr, int(TIME_XL320))
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % packetHandler.getTxRxResult(dxl_comm_result), "on ID", DXL_ID)
            elif dxl_error != 0:
                print("%s" % packetHandler.getRxPacketError(dxl_error), "on ID", DXL_ID)

def getIndexByNotElement(array,element):
    j = 0
    index = []
    for i in array:
        if(i != element):
            index.append(j)
        j+=1
    return index

def getNotValue(array,element):
    index = []
    for i in array:
        if(i != element):
            index.append(int(i))
    return index


def getIndexByNotElement_v2(array,element):
    j=0
    index_xl320 = []
    index_xm430 = []
    for i in array:
        if(i != element):
            if j in DXL_KAKI_KIRI or j in DXL_KAKI_KANAN or j == 13 or j == 14:
                index_xm430.append(j)
            else:
                index_xl320.append(j)
        j+=1
    return index_xl320,index_xm430

def getNotValue_v2(array,element):
    j=0
    index_xl320 = []
    index_xm430 = []
    for i in array:
        if(i != element):
            if j in DXL_KAKI_KIRI or j in DXL_KAKI_KANAN or j == 13 or j == 14:
                index_xm430.append(int(i))
            else:
                index_xl320.append(int(i))
        j+=1
    return index_xl320, index_xm430




#####################
### CODING MOTION ###
#####################
def bacaFile(FILE_NAME):
    global MOTION_TIME_XM430,MOTION_TIME_XL320,MOTION_DXL
    file = open(FILE_NAME)•••••••••
    csvreader = csv.reader(file)
    header = next(csvreader)
    
    MOTION_TIME_XM430 = [] #menyimpan bagian time
    MOTION_TIME_XL320 = [] #menyimpan bagian time
    MOTION_DXL = [] #menyimpan posisi dxl 4-30

    for row in csvreader:
        MOTION_TIME_XM430.append(row[2])
        MOTION_TIME_XL320.append(row[1])
        MOTION_DXL.append(row[3:])
    
    file.close()

def gerak_by_motion(NAMA_FILE, THRESHOLD):
    
    bacaFile(NAMA_FILE)
    
    for i in range(len(MOTION_DXL)):
        #SET POSISI
        i = int(i)
        DXL_IDS = getIndexByNotElement(MOTION_DXL[i],"-1")
        DXL_DEGREE = getNotValue(MOTION_DXL[i],"-1")

        #print(DXL_IDS,DXL_DEGREE)

        setTime(DXL_IDS,MOTION_TIME_XL320[i],MOTION_TIME_XM430[i])
        setGoalPosition_group(DXL_IDS,DXL_DEGREE) 
        print( "MOTION : ",NAMA_FILE," STEP : ",i)

        #READ POSISI
        while True:
            # Read present position
            dxl_present_position = []
            for DXL_ID in DXL_IDS:
                if DXL_ID in DXL_KAKI_KIRI or DXL_ID in DXL_KAKI_KANAN or DXL_ID == 13 or DXL_ID == 14:
                    val, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DXL_ID, XM430_ADDR_PRESENT_POSITION)
                    if dxl_comm_result != COMM_SUCCESS:
                        print(DXL_ID, " is %s" % packetHandler.getTxRxResult(dxl_comm_result))
                    elif dxl_error != 0:
                        print(DXL_ID, " is %s" % packetHandler.getRxPacketError(dxl_error))
                    dxl_present_position.append(map(val,0,4096,0,360))
                else:
                    val, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DXL_ID, XL320_ADDR_PRESENT_POSITION)
                    if dxl_comm_result != COMM_SUCCESS:
                        print(DXL_ID, " is %s" % packetHandler.getTxRxResult(dxl_comm_result))
                    elif dxl_error != 0:
                        print(DXL_ID, " is %s" % packetHandler.getRxPacketError(dxl_error))
                    dxl_present_position.append(map(val,0,1023,0,300))

            dxl_present_position_ = np.asarray(dxl_present_position)
            DXL_DEGREE_ = np.asarray(DXL_DEGREE)
            hasil = dxl_present_position_-DXL_DEGREE_
            #print(hasil)
            if all(abs(i) <= THRESHOLD for i in hasil) is True:
                break


def gerak_by_motion_v2(NAMA_FILE, THRESHOLD_XL320, THRESHOLD_XM430):
    
    bacaFile(NAMA_FILE)
    
    for i in range(len(MOTION_DXL)):
        #SET POSISI
        i = int(i)
        DXL_IDS = getIndexByNotElement(MOTION_DXL[i],"-1")
        DXL_DEGREE = getNotValue(MOTION_DXL[i],"-1")
        DXL_DEGREE_XL320, DXL_DEGREE_XM430 = getNotValue_v2(MOTION_DXL[i],"-1")

        

        
        #print(DXL_IDS,DXL_DEGREE)

        setTime(DXL_IDS,MOTION_TIME_XL320[i],MOTION_TIME_XM430[i])
        setGoalPosition_group(DXL_IDS,DXL_DEGREE) 
        print( "MOTION : ",NAMA_FILE," STEP : ",i)

        #READ POSISI
        while True:
            # Read present position
            dxl_present_position_xm430 = []
            dxl_present_position_xl320 = []
            
            for DXL_ID in DXL_IDS:
                if DXL_ID in DXL_KAKI_KIRI or DXL_ID in DXL_KAKI_KANAN or DXL_ID == 13 or DXL_ID == 14:
                    val, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DXL_ID, XM430_ADDR_PRESENT_POSITION)
                    if dxl_comm_result != COMM_SUCCESS:
                        print(DXL_ID, " is %s" % packetHandler.getTxRxResult(dxl_comm_result))
                    elif dxl_error != 0:
                        print(DXL_ID, " is %s" % packetHandler.getRxPacketError(dxl_error))
                    dxl_present_position_xm430.append(map(val,0,4096,0,360))
                else:
                    val, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DXL_ID, XL320_ADDR_PRESENT_POSITION)
                    if dxl_comm_result != COMM_SUCCESS:
                        print(DXL_ID, " is %s" % packetHandler.getTxRxResult(dxl_comm_result))
                    elif dxl_error != 0:
                        print(DXL_ID, " is %s" % packetHandler.getRxPacketError(dxl_error))
                    dxl_present_position_xl320.append(map(val,0,1023,0,300))

            dxl_present_position_xl320 = np.asarray(dxl_present_position_xl320)
            dxl_present_position_xm430 = np.asarray(dxl_present_position_xm430)
            DXL_DEGREE_XL320 = np.asarray(DXL_DEGREE_XL320)
            DXL_DEGREE_XM430 = np.asarray(DXL_DEGREE_XM430)
            hasil_XL320 = dxl_present_position_xl320-DXL_DEGREE_XL320
            hasil_XM430 = dxl_present_position_xm430-DXL_DEGREE_XM430

            if all(abs(i) <= THRESHOLD_XL320 for i in hasil_XL320) is True and all(abs(i) <= THRESHOLD_XM430 for i in hasil_XM430) is True:
                break
            
            

        


if __name__ == "__main__":
    inisialisasi()
    
    enableTorque(DXL_KEPALA,1)
    enableTorque([13,14],1)
    enableTorque(DXL_KAKI_KANAN,1)
    enableTorque(DXL_KAKI_KIRI,1)
    
    #gerak_by_motion_v2("Siap.csv",30,5)

    #mulai while

    #gerak_by_motion_v2("motion/2_Pasang Masker.csv",30,5)
    #gerak_by_motion_v2("motion/1_Cuci tangan_fix.csv",30,5)
    #gerak_by_motion_v2("motion/3_Salam Pembuka.csv",30,5)
    #gerak_by_motion_v2("motion/berdiri fix.csv",30,5)
    gerak_by_motion_v2("motion/jalanbarunaik.csv",30,5)
    #gerak_by_motion_v2("motion/4_Ngajat.csv",30,5)
    #gerak_by_motion_v2("motion/4_Ngajat_Cepat.csv",30,5)
    #gerak_by_motion_v2("motion/ngasai.csv",30,5)
    #gerak_by_motion_v2("motion/6_Purak barik_1.csv",30,5)
    #gerak_by_motion_v2("motion/7_Ngasai Purak+Barik_1.csv",30,5)
    #gerak_by_motion_v2("motion/7_Ngasai Purak+Barik_2.csv",30,5)
    #gerak_by_motion_v2("motion/7_Ngasai Purak+Barik_1.csv",30,5)
    #gerak_by_motion_v2("motion/7_Ngasai Purak+Barik_2.csv",30,5)
    #gerak_by_motion_v2("motion/8_Salam penutup.csv",30,5)    
    #gerak_by_motion_v2("motion/backup.csv",30,5)
    #gerak_by_motion_v2("motion/1_Cuci tangan_fix.csv",30,5)

    #enableTorque(DXL_KEPALA,0)
    #enableTorque(DXL_TANGAN_KANAN,0)
    #enableTorque(DXL_TANGAN_KIRI,0)
    #enableTorque(DXL_KAKI_KANAN,0)
    #enableTorque(DXL_KAKI_KIRI,0)
    #Close port
    portHandler.closePort()
    print("DONE")

