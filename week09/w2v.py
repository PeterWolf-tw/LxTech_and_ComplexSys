#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import fasttext
import fasttext.util

def ref():
    """"""
    print("https://fasttext.cc/docs/en/crawl-vectors.html")
    return None


if __name__ == "__main__":

    ft = fasttext.load_model("cc.en.300.bin")
    fasttext.util.reduce_model(ft, 10)
    print(ft.get_dimension())

    print(ft.get_nearest_neighbors('hello'))