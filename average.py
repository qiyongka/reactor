# -*- coding: utf-8 -*-
"""
将fft就可以得到基频点和倍频点的增益，读取出来，并且计算其相似度
Created on Tue 11. 16 :01:56 2019
@author: 齐用卡
"""
import csv
import threading
import os
import pandas as pd
import numpy as np
from scipy.fftpack import fft
import glob

count = 0
def mkdir(path):
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True

path = '/home/qyk/Desktop/电抗器'
foldernames = os.listdir(path + '/'+'output')
foldernames.sort()


foldernames = ['750kV哈吐一线高抗A相','750kV哈吐一线高抗B相','750kV吐哈一线高抗A相',
'750kV吐哈一线高抗C相','750kV哈吐一线高抗C相','750kV吐巴二线高抗C相',
'750kV吐哈一线高抗B相','750kV吐巴二线高抗A相','750kV吐巴二线高抗B相']


excel_head =[["index","position","0Hz","100Hz","200Hz","300Hz","400Hz","500Hz","600Hz","700Hz","800Hz","900Hz","1000Hz"]]
for folder in range(len(foldernames)):
    count = count +1
    print("count:",count)
    input_path = '/home/qyk/Desktop/电抗器/demo1/fft' + '/'+foldernames[folder]
    output_path = '/home/qyk/Desktop/电抗器' + '/'+ 'demo3'+ '/' + 'similar'
    
    print("input_path:",input_path)
    print("output_path:",output_path)

    mkdir(output_path)

    input_file = input_path +'/'+ foldernames[folder]+'_fft_point.csv'          #输入fft后的结果
    output_file = output_path +'/'+ 'fft_average.csv'  #输出基频和倍频的增益
    print("input_file:",input_file)
    print("output_file:",output_file)

    temp = pd.read_csv(input_file, sep = ',', header=0,engine = 'c')#读文件
    temp = np.array(temp)

    #print(temp)
    data = temp[:,1:] 
    samples = data.shape[0]
    timestamp = data.shape[1]
    #print(data)
    print(samples,timestamp)

###################################################     average

    array = np.sum(temp,axis=0) 
    array [0]  = foldernames[folder]
    array[1:] = array[1:]/samples
    print(array)

    index_temp = 'average'
    #data = np.vstack((data,array))
    #index_array = np.vstack((index_array,index))

    excel_temp = np.hstack((index_temp,array))
    excel_head = np.vstack((excel_head,excel_temp))
    print(excel_temp)

excel = excel_head

csvFile = open(output_file, "w",newline='')            #创建csv文件
writer = csv.writer(csvFile)                          #创建写的对象          
writer.writerows(excel)
csvFile.close()


