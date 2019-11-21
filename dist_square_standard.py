# -*- coding: utf-8 -*-
"""
将每个点归一化后和均值（利用初始数据先求和，再归一化）之间的距离计算出来,附加在行末尾,并且计算得到的最前面的domin个点显示在尾部
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
'''
a = [0,1,2,3,4,5]
b = [14,2,3,4,5,6]
result = o_distance(a,b)
print(result)
'''
foldernames = ['750kV哈吐一线高抗A相','750kV哈吐一线高抗B相','750kV吐哈一线高抗A相',
'750kV吐哈一线高抗C相','750kV哈吐一线高抗C相','750kV吐巴二线高抗C相',
'750kV吐哈一线高抗B相','750kV吐巴二线高抗A相','750kV吐巴二线高抗B相']
for folder in range(len(foldernames)):
    input_path = '/home/qyk/Desktop/电抗器/demo1/fft' + '/' + foldernames[folder]
    output_path = '/home/qyk/Desktop/电抗器/demo3/similar/square_distance_standard'

    mkdir(output_path)
    input_file = input_path +'/'+ foldernames[folder]+'_fft_point.csv' #输入fft后的结果
    output_file = output_path +'/' +foldernames[folder]+'square_fft__distance.csv'  #输出基频和倍频的增益

    temp = pd.read_csv(input_file, sep = ',', header=0,engine = 'c')#读文件
    temp = np.array(temp)

    data = temp[:,1:] 
    data = data **2
    samples = data.shape[0]
    timestamp = data.shape[1]

    average_distance = [0]*samples

    array_average = array_average_get(data)

    print(array_average)                        #归一化均值
    array_average_standard = array_average[1]
    array_average = array_average /array_average_standard
    print(array_average)
                                                #归一化采样点数据
    for row in range(data.shape[0]):
        standard = data[row,1]
        for col in range(data.shape[1]):
            data[row,col] = data[row,col] / standard
    print(data)


    for row in range(samples):
        average_distance[row] = o_distance(array_average,data[row,:])
    average_distance = np.array(average_distance)
    '''
    print(average_distance)
    average_distance_standard = average_distance[1]
    print(average_distance_standard)
    average_distance = average_distance / average_distance_standard
    print(average_distance)
    '''
    dist = np.array(average_distance)
    dist = dist.reshape(dist.shape[0],1)

    temp = np.hstack((temp,dist))
    subscript = sort(samples,average_distance)
    #print(subscript)
    neighbor = [0]*13
    for i in range(samples):
        #print(neighbor)
        neighbor = np.vstack((neighbor,temp[subscript[i],:]))


    #print(neighbor)
    temp = np.vstack((temp,neighbor))
    csvFile = open(output_file, "w",newline='')            #创建csv文件
    writer = csv.writer(csvFile)                          #创建写的对象  
    writer.writerow(["index","0Hz","100Hz","200Hz","300Hz","400Hz","500Hz","600Hz","700Hz","800Hz","900Hz","1000Hz","distance"])
    writer.writerows(temp)
    csvFile.close()

