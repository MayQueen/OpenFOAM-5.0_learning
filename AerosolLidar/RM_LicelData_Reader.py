# -*- encoding: utf-8 -*-
'''
@NAME      :Untitled-1.py
@TIME      :2021/03/04 16:01:52
@AUTHOR     :MERI
@Email     :mayqueen2016@163.com
'''
# Inbuild package list
import struct

# Site-package list
import numpy as np
import pickle

# Userdefined package list


# CODING CONTENTs


class RM_reader ():
    '''
    接受一个符合Licel格式的Lidar文件的python类文件对象(file-like-object),
    返回文件标题信息、通道信息,原始数据\n
    输入:\n
        `file-like`对象(可通过`python with-open`方法创建)
    输出:\n
        `标题信息,list,header_info`;
        `通道信息,list,channel_info`;
        `原始数据,list,raw_data`;
    header_info = [ 'filename',
                    'site start_date start_time end_date end_time altitude longitude latitude zenith_angle azimuth_angle temperature pressure',
                    'LS1 rate_1 LS2 rate_2 number_of_datasets', ]\n
    channel_info = ['active analog_photon laser_used number_of_datapoints 1 HV bin_width wavelength d1 d2 d3 d4 ADCbits number_of_shots discriminator ID']\n
    raw_data = ['raw_data']\n
    '''

    def __init__(self):
        self.header_info = {}
        self.channel_info = []
        self.wavelength = []
        self.num_points = []
        self.analog_photon = []
        self.dataset_mode = []
        self.raw_data = []

    def read_first_line(self, f):
        # 读取文件第一行
        self.header_info["Filename"] = f.readline().decode().strip()
        return self.header_info

    def read_second_line(self, f):
        # 读取文件第二行
        second_line = f.readline().decode().strip()
        # 格式化第二行信息,以空格位分节符取出数据
        self.header_info['site'] = str(second_line.split()[0])
        self.header_info['start_date'] = str(second_line.split()[1])
        self.header_info['start_time'] = str(second_line.split()[2])
        self.header_info['end_date'] = str(second_line.split()[3])
        self.header_info['end_time'] = str(second_line.split()[4])
        self.header_info['altitude'] = float(second_line.split()[5])
        self.header_info['longitude'] = float(second_line.split()[6])
        self.header_info['latitude'] = float(second_line.split()[7])
        self.header_info['zenith_angle'] = float(second_line.split()[8])
        self.header_info['azimuth_angle'] = float(second_line.split()[9])
        self.header_info['temperature'] = float(second_line.split()[10])
        self.header_info['pressure'] = float(second_line.split()[11])
        return self.header_info

    def read_third_line(self, f):
        # 读取文件第三行
        third_line = f.readline().decode().strip()
        self.header_info['LS1_number_of_shots'] = int(third_line.split()[0])
        self.header_info['LS_1_Frequency'] = int(third_line.split()[1])
        self.header_info['LS2_number_of_shots'] = int(third_line.split()[2])
        self.header_info['LS2_Frequency'] = int(third_line.split()[3])
        self.header_info['number_of_datasets'] = int(third_line.split()[4])
        return self.header_info

    def get_channel_info(self, f):
        # 从文件header中读取雷达channel信息
        # channel_format = 'active analog_photon laser_used number_of_datapoints 1 HV bin_width wavelength d1 d2 d3 d4 ADCbits number_of_shots discriminator ID'
        # self.channel_info.append(channel_format.split())

        # print(int(self.header_info["number_of_datasets"]))
        for c1 in range(int(self.header_info["number_of_datasets"])):
            channel_line = f.readline().decode().strip().split()
            self.channel_info.append(channel_line)
        # print(self.channel_info)
        return self.channel_info

    def read_rest_line(self, f):
        '''
        读取channel的数据
        '''
        # +++++++ 读取文件的数据信息 +++++++
        t_raw_data = []
        for c4 in self.num_points:  # 根据每个channel数据点的数量读取数据
            # print(c4)
            # 跳过一行
            f.readline().strip()  # 注意:此处空行尤为重要
            read_byte_data = np.fromfile(
                f, "i4", c4)
            t_raw_data.append(read_byte_data)
            self.raw_data = np.array(t_raw_data, dtype=object)
        return self.raw_data

    def get_analog_photon(self):
        '''
        获取每个channel的信号类型,analog 或 phonto = 0; phonton = 1
        '''
        for c2 in range(len(self.channel_info)):
            self.analog_photon.append(
                str(self.channel_info[c2][1]))  # analog_photon
        # print(num_points)
        return self.analog_photon

    def get_dataset_mode(self):
        '''
        获取每个channel的数据集的类型，BC=模拟信号数据集;BT=光子信号数据集
        '''
        for c2 in range(len(self.channel_info)):
            self.dataset_mode.append(
                str(self.channel_info[c2][-1][0:2]))  # analog_photon
        # print(dataset_mode)
        return self.dataset_mode

    def get_wavelength(self):
        '''
        获取每个channel的波长和极化方式.o=无极化;s=垂直;p=平行
        '''
        for c2 in range(len(self.channel_info)):
            self.wavelength.append(
                str(self.channel_info[c2][7]))  # wavelength
        # print(wavelength)
        return self.wavelength

    def get_number_of_datapoints(self):
        '''
        获取每个通道数据点的数量
        '''
        for c2 in range(len(self.channel_info)):
            self.num_points.append(
                int(self.channel_info[c2][3]))  # number_of_datapoints
        # print(num_points)
        return self.num_points

    def save_as_txt(self):
        '''
        保存文件为txt格式
        '''
        pass
