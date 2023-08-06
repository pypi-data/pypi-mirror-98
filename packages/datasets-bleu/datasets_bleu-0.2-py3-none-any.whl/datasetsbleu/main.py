#!/usr/bin/env python
# encoding: utf-8

import sys
from os.path import dirname, abspath

path = dirname(dirname(abspath(__file__)))
sys.path.append(path)

from datasetsbleu.engine.engine_run import get_en_zh_bleu, get_en_list, get_simple_bleu, get_file_bleu
from datasetsbleu.utils.youdao import YoudaoFanyiApi


def get_en(corpus_type, category, num):
    en_list, total = get_en_list(corpus_type, category, int(num))
    result = {"en_list": en_list, "total": total}
    return result


def effect_based_datasets(corpus_type, category, num, en, model_zh):
    if isinstance(en, str):
        result, bleu4 = get_en_zh_bleu(corpus_type, category, int(num), en, model_zh)
        return {"result": result, "bleu4": bleu4}
    elif isinstance(en, list):
        result, bleu_list, bleu4 = get_en_zh_bleu(corpus_type, category, int(num), en, model_zh)
        return {"result": result, "bleu4": bleu_list, "bleu4_mean": bleu4}


def bleu_calculation(sys, ref):
    if isinstance(sys, str) and isinstance(ref, str):
        bleu4 = get_simple_bleu(sys, ref)
        return {"bleu4": bleu4}
    elif isinstance(sys, list) and isinstance(ref, list):
        bleu_list, bleu4 = get_file_bleu(sys, ref)
        return {"bleu4": bleu_list, "bleu4_mean": bleu4}
    else:
        msg = "params error!"
        return {"msg": "{}! ".format(msg)}


def get_youdao_trans(text,input='en', output='zh-CHS'):
    youdao = YoudaoFanyiApi(input=input, output=output, proxy=1)
    result = youdao.trans(text)
    return result


if __name__ == '__main__':
    # lens = len(get_en("field", "biology", "5949")['en_list'])
    # print(get_en("field", "biology", "5949"))
    print(effect_based_datasets("bleu_level", "2", "2", ["Taking classes, open studio hours...","The script is featured with error check function, and has link lock facility...."], ["上课，开放工作室时间...","该脚本具有错误检查功能，并具有链接锁定功能。"]))
    print(bleu_calculation(["能源天体水晶周末", "收养的孩子必须知道，他们可以根据需要在任何问题上轻松舒适地对待收养父母。"],
                           ["能量星相水晶周末", "重要的是，被收养的孩子知道，他们可以在任何必要的问题上轻松和舒适地接近他们的养父母。"]))
    print(get_youdao_trans('Taking classes, open studio hours'))
    print(get_youdao_trans('能量星相水晶周末',input='zh-CHS',output='en'))