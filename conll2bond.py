#!/bin/python
# -*- coding: utf8 -*-

'''
Description:
Auther: Yuepei Li
Date: 2021-10-30
'''

import json

def add_tag(d, tag):
    i = max(d.values())
    d["B-"+tag] = i + 1
    d["I-"+tag] = i + 2


def file_read(f_name, tag_id, id_tag):
    str_words = []
    tags = []
    pre_tag = "O"
    pre_flag = 0
    sentences = []
    with open(f_name) as fp:
        for line in fp.readlines():
            aLine = line.strip("\n").strip(" ").split(" ")
            if len(aLine) < 3:
                sentences.append({
                    "str_words": str_words,
                    "tags": tags
                })
                str_words = []
                tags = []
                continue
                # return sentences
            word = aLine[0]
            tag = aLine[1].split("-")[-1]
            flag = int(aLine[2])
            # if tag != "O":
            #     if "B-" + tag not in tag_id:
            #         add_tag(tag_id, tag)
            #     if "B-" + id_tag[flag] not in tag_id:
            #         add_tag(tag_id, id_tag[flag])

            str_words.append(word)
            if "train" in f_name:
                if flag != 0:
                    if flag == pre_flag:
                        prefix = "I-"
                    else:
                        prefix = "B-"
                else:
                    prefix = ""
                tag = id_tag[flag]
                tags.append(tag_id[prefix + tag])
                pre_flag = flag
            else:
                if tag != "O":
                    if tag == pre_tag:
                        prefix = "I-"
                    else:
                        prefix = "B-"
                else:
                    prefix = ""
                tags.append(tag_id[prefix + tag])
                pre_tag = tag
    return sentences


def main():
    # with open("dataset/CoNLL2003_Dict/tag_to_id.json") as fp:
    with open("dataset/BC5CDR_Dict_0.2/tag_to_id.json") as fp:
        tag_id = json.load(fp)

    # id_tag = {0: "O", 1: "PER", 2: "LOC", 3: "ORG", 4: "MISC"}
    id_tag = {0: "O", 1: "Chemical", 2: "Disease"}
    sentences = file_read("dataset/BC5CDR_Dict_0.2/train.ALL.txt", tag_id, id_tag)
    # sentences = file_read("dataset/CoNLL2003_KB/train.ALL.txt", tag_id, id_tag)
    with open("train.json", "w") as outfile:
        json.dump(sentences, outfile)
    pass

    sentences = file_read("dataset/BC5CDR_Dict_0.2/valid.txt", tag_id, id_tag)
    # sentences = file_read("dataset/CoNLL2003_KB/valid.txt", tag_id, id_tag)
    with open("dev.json", "w") as outfile:
        json.dump(sentences, outfile)
    pass

    sentences = file_read("dataset/BC5CDR_Dict_0.2/test.txt", tag_id, id_tag)
    # sentences = file_read("dataset/CoNLL2003_KB/test.txt", tag_id, id_tag)
    with open("test.json", "w") as outfile:
        json.dump(sentences, outfile)
    pass


if __name__ == "__main__":
    main()
