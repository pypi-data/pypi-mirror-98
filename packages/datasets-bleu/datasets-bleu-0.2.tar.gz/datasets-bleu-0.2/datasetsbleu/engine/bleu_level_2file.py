#!/usr/bin/env python
# encoding: utf-8

import pandas as pd
import glob
import os

from datasetsbleu.utils.scripts import (write_file, get_filename, get_num_from_str)

src_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
xlsx_path = os.path.join(src_path, 'datasets', 'bleu_level')


def read_xlsx():
    files = glob.glob(xlsx_path + '/level_*_bleu.xlsx')
    for file in files:
        basename = get_filename(file)
        level = get_num_from_str(basename)[0]
        df = pd.read_excel(file)
        data = df[['origi', 'youdao', 'google2youdao', 'tengxun2youdao', 'mean']]
        for i, line in enumerate(data.values):
            # ori,youdao,google2youdao,tengxun2youdao,mean = line
            line = [str(x).strip() for x in line]
            item = str(level) + '\t' + '\t'.join(line)
            write_file(xlsx_path + '/orig_trans_{}_bleu.txt'.format(str(level)), item)


if __name__ == '__main__':
    read_xlsx()
