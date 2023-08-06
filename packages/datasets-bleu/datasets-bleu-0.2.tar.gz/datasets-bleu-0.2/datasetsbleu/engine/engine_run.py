#!/usr/bin/env python
# encoding: utf-8

from datasetsbleu.engine.bleu_level_en_zh import select_en_zh,get_en_cate
from datasetsbleu.engine.en_zh import get_en_cate_plus,get_en_zh
from datasetsbleu.bleu_calc.score import get_score,get_file_score


def get_en_zh_bleu(corpus_type,category,num,en,model_zh):
    # print(corpus_type,category,num,en,model_zh)
    if corpus_type == 'bleu_level':
        result = select_en_zh(category,num,en)
        if isinstance(en,str):
            ori, youdao, google2youdao, tengxun2youdao = result
            bleu4 = get_score(model_zh,youdao)
            return result,bleu4
        else:
            youdao_list = list()
            for res_tuple in result:
                ori, youdao, google2youdao, tengxun2youdao = res_tuple
                youdao_list.append(youdao)
            bleu_list,bleu4 = get_file_bleu(model_zh,youdao_list)
            return result,bleu_list,bleu4
    else:
        result = get_en_zh(corpus_type, category, num, en)
        if isinstance(en,str):
            ori, trans = result
            bleu4 = get_score(model_zh, trans)
            return result,bleu4
        else:
            trans_list = list()
            for res_tuple in result:
                ori, trans = res_tuple
                trans_list.append(trans)
            bleu_list, bleu4 = get_file_bleu(model_zh, trans_list)
            return result, bleu_list, bleu4


def get_en_list(corpus_type,category,num):
    if corpus_type == 'bleu_level':
        result = get_en_cate(category,num)
    else:
        result = get_en_cate_plus(corpus_type,category,num)
    return result

def get_simple_bleu(sys,ref):
    bleu4 = get_score(sys,ref)
    return bleu4

def get_file_bleu(sys,ref):
    bleu_list = list()
    for sys_line,ref_line in zip(sys,ref):
        bleu_list.append(get_score(sys_line,ref_line))
    bleu4 = get_file_score(sys,ref)
    return bleu_list,bleu4

def get_file_mean_bleu(sys,ref):
    bleu4 = get_file_score(sys,ref)
    return bleu4

if __name__ == '__main__':

    print(get_en_zh_bleu('field', 'finance', 10, [
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
    ],["2019年6月3日，驻澳大利亚大使程景野在澳大利亚主流媒体《澳大利亚人报》发表题为《平等互利:唯有平等互利才能解决中美贸易争端》的署名文章。", "平等互利是解决中美贸易争端的唯一出路", "每次美国宣布有意对中国商品加征关税，主要经济体金融市场就接连动荡，许多企业和民众受到伤害。", "这是刻意忽视市场规则和国际贸易规则的必然结果。", "经合组织最新发布的《经济展望》指出，中美贸易摩擦升级，可能导致2021年至2022年全球GDP损失0.7%，近6000亿美元。", "有经济学家认为，美国现行贸易政策是17、18世纪重商主义政策的延伸，与21世纪经济全球化的现实完全不符。", "某国际贸易组织前总干事表示，国际贸易必须以规则为基础，而不是以权力为基础。", "但这必须在相互尊重、平等和诚信的基础上进行。", "对于损害中国核心利益和正当发展权利的无理要求，中国决不屈服。", "无论中美经贸谈判走向何方，中国都将继续推动多边主义，倡导以规则为基础、以世贸组织为核心的多边贸易体制，支持世贸组织改革，推动贸易和投资自由化便利化。"]))
    print(get_en_zh_bleu('bleu_level','2',10,[
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
    ],['上课，开放工作室时间…', '该脚本具有错误检查功能，并具有链接锁定功能....', '孩子们喜欢他们的电脑和', '我爱我的雷蒙德，但我也不知道那本书…', '>——可以说是我们面临的最困难的化学挑战。', '实现的硬件必须能够承受恶劣的环境，并在不同的环境中提供有效的覆盖区域。', '保护加拿大的水作为公共资源:NDP', '肠道，肝脏，血管和骨骼肌', '奥巴马和俄罗斯的预言....', '令人印象深刻的写作风格……']))
    pass