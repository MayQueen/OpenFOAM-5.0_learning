# -*- encoding: utf-8 -*-
"""
@NAME      :RM_Hander.py
@TIME      :2021/03/03 14:57:45
@AUTHOR     :MERI
@Email     :mayqueen2016@163.com
"""
# Inbuild package list

# Site-package list

# Userdefined package list
from RM_LicelData_Reader import RM_reader
import RM_Calculate
from plot import plot

if __name__ == "__main__":
    # RM_PATH = r"./DATA/RM1912000.031272"
    # RM_PATH = r"./DATA/RM1912006.141715"
    # RM_PATH = r"./DATA/RM1912014.021558"
    # RM_PATH = r"./DATA/RM1912018.031555"
    RM_PATH = r"./DATA/RM1912020.021401"

    reader = RM_reader()
    with open(RM_PATH, "rb") as f:
        # ++++++ 读取文件的描述信息 ++++++

        # 从文件header中读取雷达参数信息
        # 读取文件第一行
        reader.read_first_line(f)
        # 读取文件第二行
        reader.read_second_line(f)
        # 读取文件第三行
        header_info = reader.read_third_line(f)
        # print(header_info)

        # 读取雷达信息
        channel_info = reader.get_channel_info(f)
        # print('# channel_info #' + '\n')
        # print(channel_info)
        # print(len(channel_info[0]))

        # 信号类型
        analog_photon = reader.get_analog_photon()
        # print(analog_photon)

        # dataset_mode
        dataset_mode = reader.get_dataset_mode()  # ID
        # print(dataset_mode)

        # 数据点数量
        datapoints = reader.get_number_of_datapoints()
        # print(datapoints)

        # 激光波长
        wavelength = reader.get_wavelength()
        # print(wavelength)

        # # 读取剩余所有行
        raw_data = reader.read_rest_line(f)
        # print(raw_data)

        z_list = []
        channel_data_list = []
        rcs_list = []

        for idx_channel in range(len(channel_info)):
            # print(channel_info[idx_channel])

            z = RM_Calculate.calculate_z(channel_info[idx_channel])
            z_list.append(z)
            # print(z)
            channel_data = RM_Calculate.calculate_channel_data(
                channel_info[idx_channel], raw_data[idx_channel])
            channel_data_list.append(channel_data)
            # print(channel_data)

            rcs = RM_Calculate.calculate_rcs(
                channel_data_list[idx_channel], z[idx_channel])
            rcs_list.append(rcs)
            print(rcs)

        # print(len(z_list))
        # print(channel_data_list)
        # print(rcs_list))
        plot(channel_data_list, z_list, header_info, wavelength)
        # plot(rcs_list,z_list,header_info,wavelength)
