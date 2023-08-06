#!/usr/bin/env python
# coding: utf-8

# # GDBFS Measure
import numpy as np
import pandas as pd
import math

#함수 1. Sequential Forward Selection with gdbfs
def fit(df,target):
    
    # 단계별 선택되는 feature와 gdfs값 list []
    gdfs_by_feature = []
    chosen_features = []

    # feature list
    X = df.drop(target,axis=1).columns
    available_features = list(X)
    run = 0
    
    # Loop : feature가 모두 선택될 때 까지
    while len(available_features)> 0:

        #print("colList=",available_features)

        run += 1

        # Reset best
        best_result = 0
        best_feature = ''

        # Loop : abailable_feature 하나씩 check
        for feature in available_features:

            # Create copy of already chosen features
            features_to_use = chosen_features.copy()
            features_to_use.append(feature)
   
            # gdbfs restult of features_to_sure
            result = gdbfs(df,features_to_use,target) #함수 2.
    
            # Update chosen feature and result if this feature is a new best
            if result > best_result:
                best_result = result
                best_feature = feature

        # record
        gdfs_by_feature.append(best_result)
        chosen_features.append(best_feature)
        available_features.remove(best_feature)

    # Put results in DataFrame
    results = pd.DataFrame()
    results['feature to add'] = chosen_features
    results['gdbfs'] = gdfs_by_feature
    print(results)
    
    #  return max gdfs feature subset
    maxidx = results['gdbfs'].idxmax()
    return np.array(results.loc[:maxidx,['feature to add']])
   

    
#함수 2. GDBFS Measure: dataframe과 feature subset, target 이름을 넣으면, GDBFS값을 return
def gdbfs(df,col,target):
    
    #feature subset + target list
    col.append(target)
    df = df[col]
    
    #DataFrame과 target column명을 전달하면 dic return
    dic = {}
    category = df[target].unique()
    for i in category:
        dic[i] = np.matrix(df[df[target]==i].drop(target,axis=1))
    
    # Evaluate 값 계산
    total = len(df)
    D =0
    for i in range(len(dic)-1):
        D+=(len(dic[i])+len(dic[i+1]))*(distance_min(dic[i],dic[i+1],total)) #함수 3.
    
    D/=total
    E = eveness(dic,total) #함수4.
    
    return D*E



#함수3. distance_min() : class I와 class J간의 최소거리를 구하는 함수

# I,J간의 최소 거리 구하는 distance_min 함수
def distance_min(I,J,total):
    
    # inter_dist
    ui =I.mean(axis=0)
    uj =J.mean(axis=0)
    inter_class_dist = ((len(I)+len(J))/total) * np.linalg.norm(ui-uj)
   
    # eigen value, vector each class
    valueI, vectorI = eigen(I)
    valueJ, vectorJ = eigen(J)
    
    # inter class center connect vector
    dij = uj - ui
    dji = ui - uj
    
    # cosine
    cosij = np.inner(dij,vectorI) / (np.linalg.norm(dij)*np.linalg.norm(vectorI))
    cosji = np.inner(dji,vectorJ) / (np.linalg.norm(dji)*np.linalg.norm(vectorJ))
    
    #intra-class variance
    intra_class_variance = 0.5*(math.sqrt(valueI)*abs(cosij) + math.sqrt(valueJ)*abs(cosji))
    intra_class_variance = intra_class_variance.item(0,0)
    
    return inter_class_dist - intra_class_variance


# 함수4. eveness() : 클래스 간 거리의 균등도 return
def eveness(dic,total):
    d = []
    for i in range(len(dic)-1):
        I=dic[i]
        J=dic[i+1]
        AVG_I =I.mean(axis=0)
        AVG_J =J.mean(axis=0)
        inter = ((len(I)+len(J))/total)*np.linalg.norm(AVG_I-AVG_J)
        d.append(inter)
    
    U=0
    avg = np.mean(d)
    for i in range(len(d)):
        U+=abs(d[i]-avg)
        
    c =len(dic)
    U = U/ (c*(c-1)/2)
#    print(U)
 #   print(avg)
    return 2- (U/avg)


# 함수5. eigen(X) : data X의 공분산행렬의 eigenValue와 eigenVector return
def eigen(X):
    X_cen = X - X.mean(axis=0)  # 평균을 0으로
    X_cov = np.dot(X_cen.T, X_cen) / (len(X)-1)
    w, v = np.linalg.eig(X_cov)
    return w[0],v[0]

