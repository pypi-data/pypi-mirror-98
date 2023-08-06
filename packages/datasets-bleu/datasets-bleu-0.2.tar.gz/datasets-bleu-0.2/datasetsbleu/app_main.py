#!/usr/bin/env python
# encoding: utf-8

import sys
from os.path import dirname, abspath

path = dirname(dirname(abspath(__file__)))
sys.path.append(path)

import json
from flask import Flask, request, jsonify
from datasetsbleu.engine.engine_run import get_en_zh_bleu, get_en_list, get_simple_bleu, get_file_bleu

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/get_en_list', methods=['POST'])
def get_en():
    if request.method == "POST":
        request_params = json.loads(request.data)  # request_params : corpus_type,category,num
        corpus_type = request_params.get("corpus_type")
        category = request_params.get("category")
        num = request_params.get("num")
        en_list, total = get_en_list(corpus_type, category, int(num))
        return jsonify({"code": 1, "msg": "{}! ".format("sucessful"), "en_list": en_list, "total": total})


@app.route('/effect_based_datasets', methods=['POST'])
def effect_based_datasets():
    if request.method == "POST":
        # try:
        request_params = json.loads(request.data)  # request_params : corpus_type,category,num,en,model_zh
        corpus_type = request_params.get("corpus_type")  # field sents_level scene bleu_level
        category = request_params.get("category")
        num = int(request_params.get("num"))
        en = request_params.get("en")
        model_zh = request_params.get("model_zh")
        # if corpus_type == 'bleu_level':
        if isinstance(en, str):
            result,bleu4 = get_en_zh_bleu(corpus_type,category,num,en,model_zh)
            return jsonify({"code": 1, "msg": "{}! ".format("sucessful"), "result": result, "bleu4": bleu4})
        elif isinstance(en, list):
            result, bleu_list, bleu4 = get_en_zh_bleu(corpus_type,category,num,en,model_zh)
            return jsonify(
                {"code": 1, "msg": "{}! ".format("sucessful"), "result": result, "bleu4": bleu_list, "bleu4_mean":bleu4})
        else:
            msg = "params error!"
            return jsonify({"code": -1, "msg": "{}! ".format(msg)})
        # except Exception as e:
        #     return jsonify({"code": -1, "msg": "{}! ".format(e)})


@app.route('/bleu_calculation', methods=['POST'])
def bleu_calculation():
    if request.method == "POST":
        request_params = json.loads(request.data)  # request_params : sys,ref
        sys = request_params.get("sys")
        ref = request_params.get("ref")
        if isinstance(sys, str) and isinstance(ref, str):
            bleu4 = get_simple_bleu(sys, ref)
            return jsonify({"code": 1, "msg": "{}! ".format("sucessful"), "bleu4": bleu4})
        elif isinstance(sys, list) and isinstance(ref, list):
            bleu_list, bleu4 = get_file_bleu(sys, ref)
            return jsonify({"code": 1, "msg": "{}! ".format("sucessful"), "bleu4": bleu_list, "bleu4_mean": bleu4})
        else:
            msg = "params error!"
            return jsonify({"code": -1, "msg": "{}! ".format(msg)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5020)
