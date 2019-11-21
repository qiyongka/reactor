# -*- coding: utf-8 -*-
"""
验证找到的采样点是否是正确的
Created on Tue 10. 13 21:01:56 2019
@author: 齐用卡
"""
import csv
import math
import threading
import os
import pandas as pd
import numpy as np
from scipy.fftpack import fft
import glob
import openpyxl
domin = 20
count = 0
def mkdir(path):            #路径的计算
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True

def distance(array1,array2):#距离计算
    length1 =len(array1)
    length2 =len(array2)
    if length1 == length2 :
        array1 = np.array(array1)
        array2 = np.array(array2)

        array = array1 -array2
        array = abs(array)
        dist = np.sum(array) 
        return dist
    else:
        return "array length error"

def o_distance(array1,array2):
    length1 =len(array1)
    length2 =len(array2)
    if length1 == length2 :
        array1 = np.array(array1)
        array2 = np.array(array2)

        array = array1 -array2
        result = sum([c*c for c in array])
        result = math.sqrt(result)
        return result
    else:
        return "array length error"


def array_average_get (data):#列均值

    data = np.array(data)

    samples = data.shape[0]
    timestamp = data.shape[1]

    array_average = np.sum(data,axis=0) 
    array_average = array_average / samples

    return array_average
def sort(samples,average_distance):
    subscript = [0]*samples
    for i in range(samples):
        subscript[i] = i

    #print(subscript)
    for i in range(samples):
       for j in range(samples):
           if average_distance[subscript[i]] < average_distance[subscript[j]]:
                x = subscript[i]
                subscript[i] = subscript[j]
                subscript[j] = x
    return subscript
def point_get(index):
    #print("index",index)
    index_str = index.split('_')    #字符串分割
    index_str = index_str[1]        #获取目标字符串
    #phase = index_str[0] #获取相位信息
    phase = index_str
    print("phase",phase)
    return phase
similar = ["A4","A5","A6","B4","B5","B6","C5","C6","C9","D6","D8","D9"]
#similar = ["C4","C6","D8","C8","B6","D9","D6","C5","B5"]
foldernames = ['750kV哈吐一线高抗A相','750kV哈吐一线高抗B相','750kV吐哈一线高抗A相',
'750kV吐哈一线高抗C相','750kV哈吐一线高抗C相','750kV吐巴二线高抗C相',
'750kV吐哈一线高抗B相','750kV吐巴二线高抗A相','750kV吐巴二线高抗B相']
article = [0]*12
for folder in range(len(foldernames)):
#for folder in range(1):
    input_path = '/home/qyk/Desktop/电抗器/demo1/fft' + '/' + foldernames[folder]
    output_path = '/home/qyk/Desktop/电抗器/demo3/similar/distance_standard_makesure'

    mkdir(output_path)

    input_file = input_path +'/'+ foldernames[folder]+'_fft_point.csv' #输入fft后的结果
    output_file = output_path +'/' +'TEST.csv'  #输出基频和倍频的增益

    temp = pd.read_csv(input_file, sep = ',', header=0,engine = 'c')#读文件
    temp = np.array(temp)
    data =[0] *( temp.shape[1] - 1 )
    for row in range(temp.shape[0]):
        index = temp[row][0]
        point = point_get(index)
        if point in similar :
            print("hhhhhhhhhhhhhhhh")
            data = np.vstack((data,temp[row,1:]))

    print(data)   
    data = data[1:,:]
    #data = temp[:,1:]
    samples = data.shape[0]
    timestamp = data.shape[1]

    average_distance = [0]*samples

    array_average = array_average_get(data)

    print(array_average)                        #归一化均值
    array_average_standard = array_average[1]
    array_average = array_average /array_average_standard
    print(type(array_average))
    print(array_average)  
    #array_average = np.array(array_average)
    '''                                        #归一化采样点数据
    for row in range(data.shape[0]):
        standard = data[row,1]
        for col in range(data.shape[1]):
            data[row,col] = data[row,col] / standard
    print(data)
    

    for row in range(samples):
        average_distance[row] = o_distance(array_average,data[row,:])
    average_distance = np.array(average_distance)

    dist = np.array(average_distance)
    dist = dist.reshape(dist.shape[0],1)

    print("temp",temp)
    print("dist",dist)
    temp = np.hstack((temp,dist))
    subscript = sort(samples,average_distance)

    neighbor = [0]*13
    for i in range(samples):
        neighbor = np.vstack((neighbor,temp[subscript[i],:]))
    
    temp = np.vstack((temp,neighbor))
    '''
    index = foldernames[folder]
    array_average = np.hstack((index,array_average))
    article = np.vstack((article,array_average))
print(article)
article= article[1:,:]
csvFile = open(output_file, "w",newline='')            #创建csv文件
writer = csv.writer(csvFile)                          #创建写的对象  
writer.writerow(["index","0Hz","100Hz","200Hz","300Hz","400Hz","500Hz","600Hz","700Hz","800Hz","900Hz","1000Hz"])
#writer.writerows((array_average[0],array_average[0],array_average[0],array_average[0],array_average[0]))
writer.writerows(article)
csvFile.close()

