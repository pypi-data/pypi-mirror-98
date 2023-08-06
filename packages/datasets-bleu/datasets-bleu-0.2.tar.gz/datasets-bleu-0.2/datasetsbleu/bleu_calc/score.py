#!/usr/bin/env python3
# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""
BLEU scoring of generated translations against reference translations.
"""

import argparse
import os
import sys

from datasetsbleu.bleu_calc.bleu import Scorer
from datasetsbleu.bleu_calc.dictionary import Dictionary
from datasetsbleu.bleu_calc.tokenizer import seg_char


def get_parser():
    parser = argparse.ArgumentParser(description='Command-line script for BLEU scoring.')
    # fmt: off
    parser.add_argument('-s', '--sys', default='-', help='system output')
    parser.add_argument('-r', '--ref', required=True, help='references')
    parser.add_argument('-o', '--order', default=4, metavar='N',
                        type=int, help='consider ngrams up to this order')
    parser.add_argument('--ignore-case', action='store_true',
                        help='case-insensitive scoring')
    parser.add_argument('--sacrebleu', action='store_true',
                        help='score with sacrebleu')
    parser.add_argument('--sentence-bleu', action='store_true',
                        help='report sentence-level BLEUs (i.e., with +1 smoothing)')
    # fmt: on
    return parser


def cli_main():
    parser = get_parser()
    args = parser.parse_args()
    print(args)

    assert args.sys == '-' or os.path.exists(args.sys), \
        "System output file {} does not exist".format(args.sys)
    assert os.path.exists(args.ref), \
        "Reference file {} does not exist".format(args.ref)

    dict = dictionary.Dictionary()

    def readlines(fd):
        for line in fd.readlines():
            if args.ignore_case:
                yield line.lower()
            else:
                yield line

    if args.sacrebleu:
        import sacrebleu

        def score(fdsys):
            with open(args.ref) as fdref:
                print(sacrebleu.corpus_bleu(fdsys, [fdref]))
    elif args.sentence_bleu:
        def score(fdsys):
            with open(args.ref) as fdref:
                scorer = bleu.Scorer(dict.pad(), dict.eos(), dict.unk())
                for i, (sys_tok, ref_tok) in enumerate(zip(readlines(fdsys), readlines(fdref))):
                    scorer.reset(one_init=True)
                    sys_tok = dict.encode_line(sys_tok)
                    ref_tok = dict.encode_line(ref_tok)
                    scorer.add(ref_tok, sys_tok)
                    print(i, scorer.result_string(args.order))
    else:
        def score(fdsys):
            with open(args.ref) as fdref:
                scorer = bleu.Scorer(dict.pad(), dict.eos(), dict.unk())
                for sys_tok, ref_tok in zip(readlines(fdsys), readlines(fdref)):
                    sys_tok = dict.encode_line(sys_tok)
                    ref_tok = dict.encode_line(ref_tok)
                    scorer.add(ref_tok, sys_tok)
                print(scorer.result_string(args.order))

    if args.sys == '-':
        score(sys.stdin)
    else:
        with open(args.sys, 'r') as f:
            score(f)


def readlines(path):
    with open(path,'r')as fd:
        for line in fd.readlines():
            yield line

def generator_list(list):
    for i in list:
        yield i


def get_file_score(sys_list,ref_list,order=4):
    dict = Dictionary()
    scorer = Scorer(dict.pad(), dict.eos(), dict.unk())
    for sys_tok, ref_tok in zip(generator_list(sys_list),generator_list(ref_list)):
        sys_tok = dict.encode_line(seg_char(sys_tok))
        ref_tok = dict.encode_line(seg_char(ref_tok))
        scorer.add(ref_tok, sys_tok)
    # print(scorer.result_string(order))
    bleu4_str, bleu4 = scorer.result_string(order)
    return bleu4


def get_score(sys,ref,order=4):
    '''
    Gets the result of a single BLEU calculation
    :param sys_tok: The original token
    :param ref_tok: The target token
    :param order: ngram of BLEU
    :return:
    '''
    dict = Dictionary()
    scorer = Scorer(dict.pad(), dict.eos(), dict.unk())
    scorer.reset(one_init=True)
    sys_tok = dict.encode_line(seg_char(sys))
    ref_tok = dict.encode_line(seg_char(ref))
    scorer.add(ref_tok, sys_tok)
    # print(scorer.result_string(order))
    bleu4_str,bleu4 = scorer.result_string(order)
    return bleu4

if __name__ == '__main__':
    # cli_main()
    print(get_file_score(['能源天体水晶周末', '收养的孩子必须知道，他们可以根据需要在任何问题上轻松舒适地对待收养父母。'],
                         ['能量星相水晶周末', '重要的是，被收养的孩子知道，他们可以在任何必要的问题上轻松和舒适地接近他们的养父母。']))
    # get_sentence_bleu_score()
    print(get_score('能源天体水晶周末', '能量星相水晶周末'))
    print(get_score('收养的孩子必须知道，他们可以根据需要在任何问题上轻松舒适地对待收养父母。', '重要的是，被收养的孩子知道，他们可以在任何必要的问题上轻松和舒适地接近他们的养父母。'))