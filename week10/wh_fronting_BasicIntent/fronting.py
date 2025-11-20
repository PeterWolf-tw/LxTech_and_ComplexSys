#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from wh_fronting.main import askLoki

def main():
    """"""
    return None


if __name__ == "__main__":
    inputSTR = "彭文正最喜歡賴清德"
    inputSTR = "馬小莉最喜歡的是王小明"
    #inputSTR = "馬小莉一定會買衛生紙"
    refDICT = {"Wh-fronted":[], "Cannot_be_wh-fronted": [],}
    result = askLoki(inputSTR, refDICT=refDICT)
    print(result)
