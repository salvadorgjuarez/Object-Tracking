
# coding: utf-8

# In[2]:
#%%

import ReadCsv

# In[3]:

import ot_cluster
from time import sleep 
import os



def cls():
    if os.name=='posix':
        !clear
    else:
        !clc
     

def FunctionReadData(sample):
    vClusters=ReadCsv.get_nofValidClusters(sample)
    return vClusters

def FunctionCreateClusters(sample, egoRinfo, egoLinfo):
    vClus=FunctionReadData(sample)
    validRClusters=[]
    validLClusters=[]
    for clusR in range(vClus[0]):
        cR=ot_cluster.Cluster()
        cRinfo=ReadCsv.get_RightInfoCluster(clusR,sample)
        cR.set_attributes(cRinfo[0],cRinfo[1],cRinfo[2],cRinfo[3], cRinfo[4], cRinfo[5], cRinfo[6], cRinfo[7], cRinfo[8],cRinfo[9])
        cR.set_filtercluster(egoRinfo.f_EgoSpeedSensorSpeedX,egoRinfo.f_EgoSpeedSensorSpeedY, egoRinfo.f_StaClsThrshld,egoRinfo.f_DynClsThrshld, egoRinfo.f_AmbClsThrshld)
        cR.eval_kinematics(egoRinfo.f_EgoSpeedClusterBased)
        cR.eval_asnewobject()
        validRClusters.append(cR)
        
    for clusL in range(vClus[1]):
        cL=ot_cluster.Cluster()
        cLinfo=ReadCsv.get_LeftInfoCluster(clusL,sample)
        cL.set_attributes(cLinfo[0],cLinfo[1],cLinfo[2],cLinfo[3],cLinfo[4], cLinfo[5], cLinfo[6], cLinfo[7], cLinfo[8], cLinfo[9])
        cL.set_filtercluster(egoLinfo.f_EgoSpeedSensorSpeedX,egoLinfo.f_EgoSpeedSensorSpeedY, egoLinfo.f_StaClsThrshld,egoLinfo.f_DynClsThrshld, egoLinfo.f_AmbClsThrshld)
        cL.eval_kinematics(egoLinfo.f_EgoSpeedClusterBased)
        cL.eval_asnewobject()
        validLClusters.append(cL)   
    return validRClusters,validLClusters


def FunctionFilterClusters():
    return None

def FunctionCreateObjects(valLeftClusters, valRightClusters, l_trackedobj, r_trackedobj, egoRInfo, egoLinfo):
    L_ValidClustersObjects=[]
    R_ValidClustersObjects=[]
    L_nvalidclusters=len(valLeftClusters)
    R_nvalidclusters=len(valRightClusters)
    
    for i in range (L_nvalidclusters):
        if valLeftClusters[i].s_ValidObjectID == 'True':
            L_ValidClustersObjects.append(valLeftClusters[i])
            
    for i in range (R_nvalidclusters):
        if valRightClusters[i].s_ValidObjectID == 'True':
            R_ValidClustersObjects.append(valRightClusters[i])
            
    L_ValidClustersObjects.sort(reverse = True, key= lambda Cluster: Cluster.f_ObjectPriority)
    R_ValidClustersObjects.sort(reverse = True, key= lambda Cluster: Cluster.f_ObjectPriority)
    
    l_trackedobj.set_lifecounterup()
    l_trackedobj.set_createNewObjects_v2(L_ValidClustersObjects, egoLInfo)
    l_trackedobj.set_evalDistanceToEgo()
    l_trackedobj.set_evalCombineObjs()
    l_trackedobj.set_update40TrackedObjs()
    l_trackedobj.set_evalContinuityObjs()

    r_trackedobj.set_lifecounterup()
    r_trackedobj.set_createNewObjects_v2(L_ValidClustersObjects, egoLInfo)
    r_trackedobj.set_evalDistanceToEgo()
    r_trackedobj.set_evalCombineObjs()
    r_trackedobj.set_update40TrackedObjs()
    r_trackedobj.set_evalContinuityObjs()
    return l_trackedobj, r_trackedobj

def FunctionMergeObjects():
    return None

def FunctionTrackingObjects():
    return None

def FunctionGraphicalInterface():
    return None


LeftTrackedObjects = ot_cluster.TrackedObjects()
RightTrackedObjects = ot_cluster.TrackedObjects()

#CICLES_TO_RUN = 4885
#DELAY_IN_S = 0.25
CICLES_TO_RUN = 50
for sample in range(CICLES_TO_RUN):
    
    sleep(DELAY_IN_S)
    cls()
    print("sample:" + str(sample))
#    !clear
 #   sample = 200
    egoInfoLeft=ReadCsv.get_egoLeftInfoCluster(sample)
    egoInfoRight=ReadCsv.get_egoRightInfoCluster(sample)

    
    egoRInfo=ot_cluster.Ego()
    egoRInfo.set_EgoSpeeds(egoInfoRight[0],egoInfoRight[1],egoInfoRight[2],egoInfoRight[3],egoInfoRight[4], egoInfoRight[5], egoInfoRight[6], egoInfoRight[7], egoInfoRight[8], egoInfoRight[9])
    
    egoLInfo=ot_cluster.Ego()
    egoLInfo.set_EgoSpeeds(egoInfoLeft[0],egoInfoLeft[1],egoInfoLeft[2],egoInfoLeft[3],egoInfoLeft[4], egoInfoLeft[5], egoInfoLeft[6], egoInfoLeft[7] ,egoInfoLeft[8] ,egoInfoLeft[9])
    
    egoRInfo.eval_thresholds()
    egoLInfo.eval_thresholds()

    [valLeftClusters, valRightClusters]  = FunctionCreateClusters(sample, egoRInfo, egoLInfo)
    
    # print("Number of validLClusters::type::elements" +str(len(valLeftClusters)) + "::" + str(type(valLeftClusters)) + "::" +str(valLeftClusters))
    [LTO, RTO] = FunctionCreateObjects(valLeftClusters, valRightClusters, LeftTrackedObjects, RightTrackedObjects, egoRInfo, egoLInfo)
    # print("sample:" + str(sample))
    
    # if len(LeftTrackedObjects.l_40TrackedObjs) > 1:
        
    #     print(LeftTrackedObjects.TRACKEDCOUNTER)
    #     print(RightTrackedObjects.TRACKEDCOUNTER)

        # print("LeftTrackedObjects kalman :" + str(sample))
        # LeftTrackedObjects.l_40TrackedObjs[0].f_Kalman.Matrix_A_P_Q_H_R_I()
        # LeftTrackedObjects.l_40TrackedObjs[0].f_Kalman.OldStateVector(5)
        # LeftTrackedObjects.l_40TrackedObjs[0].f_Kalman.RelativeVelocities()
        # LeftTrackedObjects.l_40TrackedObjs[0].f_Kalman.AceleratioFramework()
        # LeftTrackedObjects.l_40TrackedObjs[0].f_Kalman.KalmanFilter_Predict()
        # print(LeftTrackedObjects.l_40TrackedObjs[0].f_Kalman.X)
        # print("RightTrackedObjects kalman:" + str(sample))
        # RightTrackedObjects.l_40TrackedObjs[0].f_Kalman.Matrix_A_P_Q_H_R_I()
        # RightTrackedObjects.l_40TrackedObjs[0].f_Kalman.OldStateVector(5)
        # RightTrackedObjects.l_40TrackedObjs[0].f_Kalman.RelativeVelocities()
        # RightTrackedObjects.l_40TrackedObjs[0].f_Kalman.AceleratioFramework()
        # RightTrackedObjects.l_40TrackedObjs[0].f_Kalman.KalmanFilter_Predict()
        # print(RightTrackedObjects.l_40TrackedObjs[0].f_Kalman.X)

#
#LTO.l_40TrackedObjs[0].f_Kalman.Matrix_A_P_Q_H_R_I()
#LTO.l_40TrackedObjs[0].f_Kalman.OldStateVector(5)
#LTO.l_40TrackedObjs[0].f_Kalman.RelativeVelocities()
#LTO.l_40TrackedObjs[0].f_Kalman.AceleratioFramework()
#LTO.l_40TrackedObjs[0].f_Kalman.KalmanFilter_Predict()
#print(LTO.l_40TrackedObjs[0].f_Kalman.P)
    # [sorteda, sortedb] = FunctionCreateObjects(valLeftClusters, valRightClusters)
    # for i in range (len(sorteda)):
    #     #print("###############################################")
    #     print("Left objects:" + str(sorteda[i].f_ObjectPriority) + "No of objects " + str(len(sorteda)))

        
    # for i in range (len(sortedb)):
    #     #print("+++++++++++++++++++++++++++++++++++++++++++++++")
    #     print("Right objects:" + str(sortedb[i].f_ObjectPriority) + "No of objects " + str(len(sortedb)))
