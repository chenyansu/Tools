#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = "chenyansu"

"""
一个图像识别程序，需要tesseract在path里
可以以多种方式输出并具有清理功能。
"""

import pytesseract
import os
from PIL import Image
import time
# import logging
#
# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


def dir2list(dir, extension_filter= (), _file_list=[]):
    """
    将目录下的文件名转换为一个列表，可以根据后缀名筛选文件
    :param dir:
    :param extension_filter:
    :param _file_list:
    :return:
    """
    for i in os.listdir(dir):
        i = os.path.join(dir, i)
        if os.path.isfile(i):
            if extension_filter:
                for e in extension_filter:
                    if e == os.path.splitext(i)[1]:
                        _file_list.append(i)
            else:
                _file_list.append(i)
        elif os.path.isdir(i):
            # print(i)
            dir2list(dir=i,extension_filter=extension_filter)
        else:
            raise ValueError("{} is not a file or folder".format(i))
    return _file_list


def tesseract_it(image):
    """
    识别图片并返回识别结果
    :param image:
    :return:
    """
    image = Image.open(image)
    char = pytesseract.image_to_string(image, lang='chi_sim')
    return char


def _save_to_many(result_dict, outdir):
    """
    每条数据都单独存放:文件夹/文件名.txt
    :param result_dict:
    :param outdir:
    :return: 文件名
    """
    # TODO : 去除目录
    out_files = []
    for k, v in result_dict.items():
        basename = os.path.basename(k)
        if outdir == "":
            out_file = "{}{}.txt".format(outdir, k)
            out_files.append(out_file)
            with open(out_file,"w") as fp:
                fp.write("{}:{}\n".format(basename, v))
        else:
            out_file = "{}{}.txt".format(outdir, basename)
            out_files.append(out_file)
            with open(out_file,"w") as fp:
                fp.write("{}:{}\n".format(basename, v))
    return out_files


def _save_to_one(result_dict, outdir):
    """
    将所有数据保存到同一个文件 ：文件夹/时间戳.txt
    :param result_dict:
    :param outdir:
    :return: 文件名
    """
    out_file = "{}/{}图像识别结果.txt".format(outdir, str(int(time.time())))
    with open(out_file,'w') as fp:
        for k, v in result_dict.items():
            fp.write("{}:{}\n".format(k, v))
    return [out_file,] # 统一格式，返回列表


def _save_log(out_files, outdir=""):
    """
    日志
    """
    log_file = "{}/{}图像识别保存记录.log".format(outdir, str(int(time.time())))
    with open(log_file, 'w') as fp:
        for file in out_files:
            fp.write(str(file)+"\n")


def start(indir, out="", model="many"):
    """
    三种模式：
    （1）原地保存：many
    （2）多个文件保存到指定目录里: out_many
    （3）合成一个文件保存到指定目录里: out_one
    :param indir:
    :param out:
    :param model:
    :return:
    """
    task_list = dir2list(indir)
    result_dict = {}

    # 计量模块
    task_len = len(task_list)
    task_finished = 0

    # 先判断，后输入
    if model == "many": # 原地保存
        out_files = []
        for i in task_list:
            task_finished += 1
            print("共有任务{}, 正在处理第{}个".format(task_len, task_finished))
            result_dict[i] = tesseract_it(i)
            out_files = _save_to_many(result_dict, outdir="") # out_files会在最后一次循环赋值为正确的
        _save_log(out_files, outdir=indir)
    elif model == "out_many": # 多个文件保存到指定目录里
        for i in task_list:
            task_finished += 1
            print("共有任务{}, 正在处理第{}个".format(task_len, task_finished))
            result_dict[i] = tesseract_it(i)
            out_files = _save_to_many(result_dict, outdir=out)
        _save_log(out_files, outdir=out)
    elif model == "out_one": # 合成一个文件保存到指定目录里
        for i in task_list:
            task_finished += 1
            print("共有任务{}, 正在处理第{}个".format(task_len, task_finished))
            result_dict[i] = tesseract_it(i)
        out_files = _save_to_one(result_dict, outdir=out)
        _save_log(out_files, outdir=out)
    else:
        raise ValueError("不存在的model值")

    print("完成,保存为{}".format(out_files))


def clean(out_files_log):
    """
    读取日志，逐行删除对应路径的文件
    :param out_files_log:
    :return:
    """
    clean_list = []
    with open(out_files_log,'r') as fp:
        for i in fp.readlines():
            clean_list.append(i.strip())
        # print(clean_list)
    for i in clean_list:
        os.remove(i)
        print("正在删除{}".format(i))
    print("正在删除log：{}".format(out_files_log))
    os.remove(out_files_log)
    print("清理完毕")






if __name__ == "__main__":
    # scan_dir(r"C:\Program Files (x86)\Tesseract-OCR", _print)
    # a = dir2list(r"C:/Users/chenyansu/Documents/GitHub",extension_filter=(".py",".css"))
    # for i in a:
    #     print(i)
    # result_dir = {"1":231, "sdas":"sdasdasd"}
    # outdir = r"C:\Users\chenyansu\Desktop\\"
    # _save_to_multi(result_dir, outdir)
    # start(indir=r"C:\Users\chenyansu\Desktop\test", model="out_one", out=r"C:\Users\chenyansu\Desktop\test2\\")
    # start(indir=r"C:\Users\chenyansu\Desktop\test\\", model="many")
    # _save_log(["1","2",3], outdir=r"C:\Users\chenyansu\Desktop\test2\\")
    clean(r"C:\Users\chenyansu\Desktop\test2\1542014196图像识别保存记录.log")