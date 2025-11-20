#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for s2f

    Input:
        inputSTR      str,
        utterance     str,
        args          str[],
        resultDICT    dict,
        refDICT       dict,
        pattern       str

    Output:
        resultDICT    dict
"""

from importlib.util import module_from_spec
from importlib.util import spec_from_file_location
from random import sample
import json
import os

INTENT_NAME = "s2f"
CWD_PATH = os.path.dirname(os.path.abspath(__file__))

def import_from_path(module_name, file_path):
    spec = spec_from_file_location(module_name, file_path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

MODULE_DICT = {
    "Account": import_from_path("wh_fronting_lib_Account", os.path.join(os.path.dirname(CWD_PATH), "lib/Account.py")),
    "LLM": import_from_path("wh_fronting_lib_LLM", os.path.join(os.path.dirname(CWD_PATH), "lib/LLM.py"))
}
"""
Account 變數清單
[變數] BASE_PATH         => 根目錄位置
[變數] LIB_PATH          => lib 目錄位置
[變數] INTENT_PATH       => intent 目錄位置
[變數] REPLY_PATH        => reply 目錄位置
[變數] ACCOUNT_DICT      => account.info 內容
[變數] ARTICUT           => ArticutAPI (用法：ARTICUT.parse()。 #需安裝 ArticutAPI.)
[變數] USER_DEFINED_FILE => 使用者自定詞典的檔案路徑
[變數] USER_DEFINED_DICT => 使用者自定詞典內容
"""
REPLY_PATH = MODULE_DICT["Account"].REPLY_PATH
ACCOUNT_DICT = MODULE_DICT["Account"].ACCOUNT_DICT
ARTICUT = MODULE_DICT["Account"].ARTICUT
USER_DEFINED_FILE = MODULE_DICT["Account"].USER_DEFINED_FILE
USER_DEFINED_DICT = MODULE_DICT["Account"].USER_DEFINED_DICT
getLLM = MODULE_DICT["LLM"].getLLM

# userDefinedDICT (Deprecated)
# 請使用 Account 變數 USER_DEFINED_DICT 代替
#userDefinedDICT = {}
#try:
#    userDefinedDICT = json.load(open(os.path.join(CWD_PATH, "USER_DEFINED.json"), encoding="utf-8"))
#except:
#    pass

replyDICT = {}
replyPathSTR = os.path.join(REPLY_PATH, "reply_{}.json".format(INTENT_NAME))
if os.path.exists(replyPathSTR):
    try:
        replyDICT = json.load(open(replyPathSTR, encoding="utf-8"))
    except Exception as e:
        print("[ERROR] reply_{}.json => {}".format(INTENT_NAME, str(e)))
CHATBOT = True if replyDICT else False

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if ACCOUNT_DICT["debug"]:
        print("[{}] {} ===> {}".format(INTENT_NAME, inputSTR, utterance))

def getReply(utterance, args):
    replySTR = ""
    try:
        replySTR = sample(replyDICT[utterance], 1)[0]
        if args:
            replySTR = replySTR.format(*args)
    except:
        pass

    return replySTR

def fronting(inputSTR, args=[], FTobj={"person":[], "time":[], "loc":[], "enty":[]}):
    #<從句首開始檢查，要被FT 的詞彙前，是否有 RC 的出現>
    resultDICT = ARTICUT.parse(inputSTR)
    verbLIST = ARTICUT.getVerbStemLIST(resultDICT)
    verbIndexLIST = []
    RC = None
    for s in range(0, len(verbLIST)):
        for vi in verbLIST[s]:
            verbIndexLIST.append(vi[0])
        if verbIndexLIST !=[]:
            try:
                if resultDICT["result_pos"][s].index("的") > verbIndexLIST[0]:
                    RC = True
                    print("有 RC 在前面")
                else:
                    RC = False
            except ValueError:
                RC = False
    if RC == True:
        return inputSTR
    else:
        pass
    #</從句首開始檢查，要被FT 的詞彙前，是否有 RC 的出現>
    frontedSTR = ""
    #<確認 FT 的詞彙的詞性>
    if "enty" in FTobj.keys():
        frontedSTR = "什麼東西" + inputSTR.replace(FTobj["enty"], "")
    #</確認 FT 的詞彙的詞性>
    return frontedSTR

getResponse = getReply
def getResult(inputSTR, utterance, args, resultDICT, refDICT, pattern="", toolkitDICT={}):
    debugInfo(inputSTR, utterance)
    if utterance == "[你]買了[衛生紙]":
        if CHATBOT:
            replySTR = getReply(utterance, args)
            if replySTR:
                resultDICT["response"] = replySTR
                resultDICT["source"] = "reply"
        else:
            # write your code here
            # resultDICT[key].append(value)
            pass

    if utterance == "[馬小莉][一定][會]買[衛生紙]":
        if CHATBOT:
            replySTR = getReply(utterance, args)
            if replySTR:
                resultDICT["response"] = replySTR
                resultDICT["source"] = "reply"
        else:
            resultSTR = fronting(inputSTR, args=args, FTobj={"enty":args[3]})
            resultDICT["Wh-fronted"].append(resultSTR)

    if utterance == "[馬小莉][最]喜歡[王小明]":
        if CHATBOT:
            replySTR = getReply(utterance, args)
            if replySTR:
                resultDICT["response"] = replySTR
                resultDICT["source"] = "reply"
        else:
            resultSTR = fronting(inputSTR, args=args, FTobj={"enty":args[2]})
            if resultSTR == inputSTR:
                resultDICT["Cannot_be_wh-fronted"].append(resultSTR)
            else:
                resultDICT["Wh-fronted"].append(resultSTR)

    if utterance == "[馬小莉]不喜歡[王小明]":
        if CHATBOT:
            replySTR = getReply(utterance, args)
            if replySTR:
                resultDICT["response"] = replySTR
                resultDICT["source"] = "reply"
        else:
            # write your code here
            # resultDICT[key].append(value)
            pass

    if utterance == "每個[人][都][會]買[衛生紙]":
        if CHATBOT:
            replySTR = getReply(utterance, args)
            if replySTR:
                resultDICT["response"] = replySTR
                resultDICT["source"] = "reply"
        else:
            # write your code here
            # resultDICT[key].append(value)
            pass

    return resultDICT


if __name__ == "__main__":
    from pprint import pprint

    resultDICT = getResult("你買了衛生紙", "[你]買了[衛生紙]", [], {}, {})
    pprint(resultDICT)