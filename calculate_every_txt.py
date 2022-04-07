import os
import pdb
import time
import math
import jieba
from collections import defaultdict


def data_preprocessing(data_roots):
    listdir = os.listdir(data_roots)

    char_to_be_replaced = "\n `1234567890-=/*-~!@#$%^&*()_+qwertyuiop[]\\QWERTYUIOP{}|asdfghjkl;" \
                          "'ASDFGHJKL:\"zxcvbnm,./ZXCVBNM<>?~！@#￥%……&*（）——+【】：；“‘’”《》？，。" \
                          "、★「」『』～＂□ａｎｔｉ－ｃｌｉｍａｘ＋．／０１２３４５６７８９＜＝＞＠Ａ" \
                          "ＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＶＷＸＹＺ［＼］ｂｄｅｆｇｈｊｋｏｐｒｓ" \
                          "ｕｖｗｙｚ￣\u3000\x1a"
    char_to_be_replaced = list(char_to_be_replaced)

    txt_corpus = []
    txt_names = []

    for tmp_file_name in listdir:
        path = os.path.join(data_roots, tmp_file_name)
        if os.path.isfile(path):
            with open(path, "r", encoding="gbk", errors="ignore") as tmp_file:
                tmp_file_context = tmp_file.read()
                for tmp_char in char_to_be_replaced:
                    tmp_file_context = tmp_file_context.replace(tmp_char, "")
                tmp_file_context = tmp_file_context.replace("本书来自免费小说下载站更多更新免费电子书请关注", "")
                txt_corpus.append(tmp_file_context)
                txt_names.append(tmp_file_name.split(".txt")[0])

    return txt_corpus, txt_names


if __name__ == '__main__':

    data_roots = './txt_files/'
    txt_corpus, txt_names = data_preprocessing(data_roots)

    for idx in range(len(txt_corpus)):
        start_time = time.time()
        tmp_txt_content = txt_corpus[idx]
        tmp_txt_name = txt_names[idx]
        len_char, len_words = 0, 0
        chars_counter, words_counter = defaultdict(int), defaultdict(int)

        for tmp_char in tmp_txt_content:
            chars_counter[tmp_char] += 1
            len_char += 1

        for tmp_word in jieba.cut(tmp_txt_content):
            words_counter[tmp_word] += 1
            len_words += 1

        char_entropy, word_entropy = 0, 0
        for char_item in chars_counter.items():
            char_entropy += (-(char_item[1] / len_char) * math.log(char_item[1] / len_char, 2))
        for word_item in words_counter.items():
            word_entropy += (-(word_item[1] / len_words) * math.log(word_item[1] / len_words, 2))
        end_time = time.time()

        print("---------------------------------------------------")
        print("当前小说题目：《{}》".format(txt_names[idx]))
        print("运行时间：{}".format(round(end_time - start_time, 2)))
        print("当前小说总字数：{}".format(len_char))
        print("当前小说分词总个数：{}".format(len_words))
        print("当前小说平均词长：{}".format(round(len_char / len_words, 3)))
        print("当前小说基于字的中文平均信息熵为：{} bits".format(round(char_entropy, 2)))
        print("当前小说基于词的中文平均信息熵为：{} bits".format(round(word_entropy, 2)))
        