import math
convertToDegree = 180 / math.pi

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

    return "DXL_15:", int(DXL_7), "| DXL_17:", int(DXL_9), "| DXL_19:", int(DXL_11), "| DXL_21:", int(DXL_13), "| DXL_23:", int(DXL_15), "| DXL_25:",int(DXL_17)
    
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
    
    return "DXL_16:",int(DXL_6), "| DXL_18:", int(DXL_10), "| DXL_20:",int(DXL_12), "| DXL_22:",int(DXL_14), "| DXL_24:",int(DXL_16), "| DXL_26:",int(DXL_18)

if __name__ == "__main__":

    print(hitung_kaki_kanan(  x=0-0.02 -0.023            , 
                              y=0-0.015          +0.07  , 
                              z=-0.22+0.035     +0.03 
                            ))
    
    print(hitung_kaki_kiri( x=0-0.02 - 0.063               , 
                            y=0+0.015            +0.07 ,           
                            z=-0.22+0.035       +0.0
                        ))


    