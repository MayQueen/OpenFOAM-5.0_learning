# -*- encoding: utf-8 -*-
"""
@NAME      :RM_Calculate.py
@TIME      :2021/03/03 14:57:45
@AUTHOR     :MERI
@Email     :mayqueen2016@163.com
"""
# Inbuild package list

# Site-package list
import numpy as np

# Userdefined package list

# CODING CONTENT


def calculate_z(single_channel_info=[]):
    '''
    根据channel的信息计算z
    '''

    # +++++++++++++++++++++++++++ 变量赋值 +++++++++++++++++++++++++++
    bin_width = float(single_channel_info[6])  # "bin_width"
    data_points = int(single_channel_info[3])  # "number_of_datapoints"

    # +++++++++++++++++++++++++++ 开始计算 +++++++++++++++++++++++++++
    # 计算 Z
    dz = bin_width  # 单位:m
    z = np.array(
        [dz * bin_number + dz / 2.0 for bin_number in range(data_points)]
    )

    return z


def calculate_channel_data(single_channel_info=[], single_channel_raw_data=[]):
    '''
    根据channel的信息计算channel_data
    '''

    # +++++++++++++++++++++++++++ 变量赋值 +++++++++++++++++++++++++++
    number_of_shots = int(single_channel_info[-3])  # "number_of_shots"
    # analog_photon,0:analog/photon;1:photon counting
    analog_photon = single_channel_info[1]
    # print(analog_photon)

    # dataset_mode = single_channel_info[-1][0:2] # ID;BT:模拟信号;BC:光子信号;PD:???

    discriminator = float(single_channel_info[-2])  # "discriminator" ,单位为mV
    adcbits = int(single_channel_info[-4])  # "ADCbits"

    # +++++++++++++++++++++++++++ 开始计算 +++++++++++++++++++++++++++
    # 计算 channel_data
    norm = single_channel_raw_data / number_of_shots

    # # 判断channel的信号类型,选择计算公式
    if analog_photon == '0':  # 模拟信号
        ADCrange = discriminator
        channel_data = norm * ADCrange/(2**adcbits)*1000
    else:  # 光信号
        channel_data = norm * number_of_shots

    return channel_data


def calculate_rcs(singel_channel_data, z, idx_min=0, idx_max=500, first_signal_bin=10):
    """
    计算范围矫正信号(RCS,range corrected signal)
    """
    background = np.mean(singel_channel_data[idx_min:idx_max])  # 计算制定范围内的平均值
    background_corrected = (singel_channel_data.transpose() -
                            background).transpose()  # 数组转置并做减法
    background_corrected = np.roll(
        background_corrected, -first_signal_bin, axis=0
    )  # 沿着竖直方向滚动数据
    background_corrected[-first_signal_bin:] = 0  # 将指定范围内的数据设为0
    rcs = background_corrected * (z ** 2)  # 计算范围修正信号
    return rcs
