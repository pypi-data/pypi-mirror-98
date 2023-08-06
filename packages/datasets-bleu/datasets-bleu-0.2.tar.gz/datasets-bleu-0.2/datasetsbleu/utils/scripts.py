import os
import re


def write_file(path, item):
    with open(path, 'a', encoding='utf-8')as fw:
        fw.write(item + '\n')


def get_filename(path):
    return os.path.basename(path)

def get_num_from_str(string):
    return re.findall(r'\d+',string)

def get_feature_from_str(string):
    return string.split('_')[1]


def get_readlines(path):
    with open(path,'r',encoding='utf-8')as fr:
        return fr.readlines()