# -*- encoding: utf-8 -*-
"""
@NAME      :RM_Hander.py
@TIME      :2021/03/03 14:57:45
@AUTHOR     :MERI
@Email     :mayqueen2016@163.com
"""
# Inbuild package list
from math import ceil
# Site-package list

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Userdefined package list


def plot(singal_list=[],height_list=[],header_info={},wavelength = []):

    # plt.style.use('ggplot')
    plt.rcParams['figure.figsize'] = (16.0, 12.0)
    fig=plt.figure()
    
    fig.subplots_adjust(hspace=0.4, wspace=0.6)
    fig.suptitle('Raw data of Raymetric Lidar File %s'% header_info['Filename'] )

    # x = np.linspace(1,10)
    # for i in range(1,8):
    #     ax=fig.add_subplot(2,4,i)
    #     ax.plot(x,x*x)

    len_singal_list = len(singal_list)
    # print(len_singal_list)

    num_raw = ceil(len_singal_list/2) # 获取子图的行数
    # print(num_raw)

    # 设置子图x坐标名称
    item_1 = 'Analog Singal Indensity(mV)'
    item_2 = 'Photon number(counts)'
    x_label = [item_1,item_2,item_1,item_2,item_1,item_2,item_1]

    # 创建子图并进行数据绑定
    for idx in range(len_singal_list):
        # print(idx)
        # print(len(singal_list))
        
        # print(num_raw) 
        ax = fig.add_subplot(2,num_raw,idx+1)

        # 设置坐标轴数据
        t_x = singal_list[idx][:550]# 转化为科学计数法
        t_y = height_list[idx][:550]/1000 # 单位由m换成km
        
        # 调整y坐标范围
        plt.ylim(0,2)
        ax.plot(t_x,t_y,color= 'c',linestyle = '-.')

        # 设置各子图的标题和坐标轴标签
        ax.set(ylabel = 'Height (km)')
        ax.set(xlabel = '%s' % x_label[idx])
        ax.set_title('%s' % wavelength[idx])

    plt.show()
