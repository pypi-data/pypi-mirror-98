import glob
import os
import json

from datasetsbleu.utils.scripts import (write_file, get_filename, get_num_from_str, get_readlines, get_feature_from_str)

src_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sents_level_path = os.path.join(src_path, 'datasets', 'sents_level')
field_path = os.path.join(src_path, 'datasets', 'field_sents')
scene_path = os.path.join(src_path, 'datasets', 'scene_sents')

def read_sents_level():
    en_files = glob.glob(sents_level_path + '/level_*_en')
    zh_files = glob.glob(sents_level_path + '/level_*_zh')
    for file in en_files:
        basename = get_filename(file)
        level = get_num_from_str(basename)[0]
        en_readlines = get_readlines(file)
        for zh_file in zh_files:
            zh_basename = get_filename(zh_file)
            if level in zh_basename:
                zh_readlines = get_readlines(zh_file)
        for i,line in enumerate(en_readlines):
            id,en = line.strip().split('\t')
            id,zh = zh_readlines[i].strip().split('\t')
            item = str(level) + '\t' + en + '\t' + zh
            write_file(sents_level_path+'/sents_{}_level.txt'.format(str(level)),item)


def read_field_file():
    en_files = glob.glob(field_path + '/*_en')
    zh_files = glob.glob(field_path + '/*_zh')
    for file in en_files:
        basename = get_filename(file)
        feature = get_feature_from_str(basename)
        en_readlines = get_readlines(file)
        for zh_file in zh_files:
            zh_basename = get_filename(zh_file)
            if feature in zh_basename:
                zh_readlines = get_readlines(zh_file)
        for i,line in enumerate(en_readlines):
            try:
                en = json.loads(line.strip()).replace(r'\n','')
                zh = json.loads(zh_readlines[i].strip()).replace(r'\n','')
            except:
                en = line.strip().replace(r'\n','')
                zh = zh_readlines[i].strip().replace(r'\n','')
            item = feature + '\t' + en + '\t' + zh
            write_file(field_path + '/field_{}_corpus.txt'.format(feature), item)

def read_scene_file():
    en_files = glob.glob(scene_path + '/*_en')
    zh_files = glob.glob(scene_path + '/*_zh')
    for file in en_files:
        basename = get_filename(file)
        feature = get_feature_from_str(basename)
        en_readlines = get_readlines(file)
        for zh_file in zh_files:
            zh_basename = get_filename(zh_file)
            if feature in zh_basename:
                zh_readlines = get_readlines(zh_file)
        for i, line in enumerate(en_readlines):
            try:
                en = json.loads(line.strip()).replace(r'\n', '')
                zh = json.loads(zh_readlines[i].strip()).replace(r'\n', '')
            except:
                en = line.strip().replace(r'\n', '')
                zh = zh_readlines[i].strip().replace(r'\n', '')
            item = feature + '\t' + en + '\t' + zh
            write_file(scene_path + '/scene_{}_corpus.txt'.format(feature), item)


if __name__ == '__main__':
    # read_sents_level()
    # read_field_file()
    # read_scene_file()
    pass