#!/usr/bin/env python
# encoding: utf-8

import os
from datasetsbleu.utils.scripts import get_readlines

src_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bleu_level_file = os.path.join(src_path, 'datasets', 'bleu_level')


def filter_en(line):
    level, ori, youdao, google2youdao, tengxun2youdao, mean = line.split('\t')
    return ori

def filter_tuple(line):
    level, ori, youdao, google2youdao, tengxun2youdao, mean = line.split('\t')
    return ori,youdao,google2youdao,tengxun2youdao

def select_en_zh(category,num,en):
    # print(category,num,en)
    file = os.path.join(bleu_level_file,'orig_trans_{}_bleu.txt'.format(category))
    lines = get_readlines(file)
    if isinstance(en, str):
        for line in lines:
            if en.strip() in line.strip():
                level, ori, youdao, google2youdao, tengxun2youdao, mean = line.split('\t')
            else:
                continue
        try:
            return ori,youdao,google2youdao,tengxun2youdao
        except Exception as e:
            raise FileNotFoundError('en not found')
    elif isinstance(en, list):
        result = list(map(filter_tuple,lines[:num]))
        return result
    else:
        raise TypeError('input type error')


def get_en_cate(category,num):
    file = os.path.join(bleu_level_file,'orig_trans_{}_bleu.txt'.format(category))
    lines = get_readlines(file)
    en_list = list(map(filter_en,lines[:num]))
    total = len(lines)
    return en_list,total


if __name__ == '__main__':
    print(select_en_zh('2',10,[
        "Taking classes, open studio hours...",
        "The script is featured with error check function, and has link lock facility....",
        "The children likes their computer and",
        "I love my Raymond but I wasn't aware of that book either...",
        ">-- arguably the most difficult chemical challenge that we face.",
        "The implemented hardware must be capable of withstanding harsh environments, as well as provide efficient coverage zones in the different environments.",
        "Protect Canada's water as a public resource: NDP",
        "tract, liver, blood vessels, and skeletal muscle",
        "THE PROPHECY OF OBAMA AND RUSSIA....",
        "Impressive writing style..."
    ]))
    # print(get_en_cate('1', 5))