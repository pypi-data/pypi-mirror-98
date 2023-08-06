import os
from datasetsbleu.utils.scripts import get_readlines

src_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sents_level_file = os.path.join(src_path, 'datasets', 'sents_level')
field_path = os.path.join(src_path, 'datasets', 'field_sents')
scene_path = os.path.join(src_path, 'datasets', 'scene_sents')


def get_en_zh(corpus_type, category, num, en):
    file = get_file(corpus_type, category)
    lines = get_readlines(file)
    if isinstance(en, str):
        for line in lines:
            level, ori, trans, youdao_zh, bleu4 = line.strip().split('\t')
            if en.strip() == ori.strip():
                return ori, trans
            else:
                continue
    elif isinstance(en, list):
        result = list(map(filter_tuple, lines[:num]))
        return result
    else:
        raise TypeError('input type error')


def filter_en(line):
    feature, ori, trans, youdao_zh, bleu4 = line.strip().split('\t')
    # print(ori)
    return ori


def filter_tuple(line):
    feature, ori, trans, youdao_zh, bleu4 = line.strip().split('\t')
    return ori, trans


def get_en_from_file(file, num):
    lines = get_readlines(file)
    en_list = list(map(filter_en, lines[:num]))
    total = len(lines)
    return en_list, total


def get_file(corpus_type, category):
    if corpus_type == 'field':
        file_path = field_path
        file = file_path + '/youdao_field_{}_corpus.txt'.format(category)
    elif corpus_type == 'sents_level':
        file_path = sents_level_file
        file = file_path + '/youdao_sents_{}_level.txt'.format(category)
    elif corpus_type == 'scene':
        file_path = scene_path
        file = file_path + '/youdao_scene_{}_corpus.txt'.format(category)
    else:
        raise FileNotFoundError('corpus_type not found')
    return file


def get_en_cate_plus(corpus_type, category, num):
    file = get_file(corpus_type, category)
    en_list, total = get_en_from_file(file, num)
    return en_list, total


if __name__ == '__main__':
    # print(get_en_cate_plus('field', 'finance', 5))
    print(get_en_zh('field', 'finance', 10, [
        "On June 3, 2019, The Australian published a signed article titled ‘Equality and Mutual Benefit: The Only Solution to China-US Trade Disputes' by Chinese Ambassador to Australia Cheng Jingye.",
        "Equality and Mutual Benefit: The Only Solution to China-US Trade Disputes",
        "Every time the US declared its intention to raise tariffs on Chinese goods, the financial markets of major economies would roil in succession, causing harm to many businesses and people.",
        "This is the inevitable consequence of wilful neglect of the rules of the market and of international trade.",
        "The latest OECD economic outlook indicates that escalating China-US trade friction could cause a 0.7 per cent loss in global GDP from 2021 to 2022, which is nearly $US600bn.",
        "Some economic experts called the current US trade policies an extension of the mercantilist policies in the 17th and 18th centuries, which by no means accord with the reality of economic globalisation in the 21st century.",
        "A former director-general of an international trade organisation expressed the view that international trade must be rule-based instead of power-based.",
        "But it must be done on the basis of mutual respect, equality and good faith.",
        "China never succumbs to unreasonable demands that will do harm to its core interests and the legitimate rights of development.",
        "No matter where the China-US trade talks head to, China will continue to promote multilateralism, will advocate a rule-based multilateral trading system with the WTO at its core, support WTO reforms and will push forward the liberalisation and facilitation of free trade and investment."
    ]))
