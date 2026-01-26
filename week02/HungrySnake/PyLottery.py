#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import pygame
import math
from  pygame.locals import *
from sys import exit
from random import randint

def nextMove(currentSnakeheadPos, mode):
    """
    計算蛇頭的下一個移動位置

    Args:
        currentSnakeheadPos (list): 當前蛇頭位置 [x, y]
        mode (str): 移動方向模式
            - "xMovePlus": 向右移動 (x+20)
            - "xMoveMinus": 向左移動 (x-20)
            - "yMovePlus": 向下移動 (y+20)
            - "yMoveMinus": 向上移動 (y-20)

    Returns:
        list: 下一個蛇頭位置 [x, y]
    """
    if mode == "xMovePlus":
        nextSnakeheadPos = [currentSnakeheadPos[0] + 20,  currentSnakeheadPos[1]]
    elif mode == "xMoveMinus":
        nextSnakeheadPos = [currentSnakeheadPos[0] - 20,  currentSnakeheadPos[1]]
    elif mode == "yMovePlus":
        nextSnakeheadPos = [currentSnakeheadPos[0],  currentSnakeheadPos[1] + 20]
    elif mode == "yMoveMinus":
        nextSnakeheadPos = [currentSnakeheadPos[0],  currentSnakeheadPos[1] - 20]
    return nextSnakeheadPos

def snakeDrawer(currentSnakeBodyList, nextSnakeheadPos=None, mode="circling", _step=[0]):
    """
    繪製蛇身體，支援兩種模式：循環移動和追蹤移動

    Args:
        currentSnakeBodyList (list): 當前蛇身體位置列表
        nextSnakeheadPos (list, optional): 下一個蛇頭位置，用於追蹤模式
        mode (str): 繪製模式
            - "circling": 循環移動模式，蛇沿著矩形路徑移動
            - "hunting": 追蹤模式，蛇追蹤目標移動
        _step (list): 用於追蹤循環移動步數的可變列表

    Returns:
        list: 新的蛇身體位置列表
    """
    newSnakeBodyList = []
    step=_step[0]
    if mode == "circling" and step != None:
        # 定義循環路徑的邊界：上(T)、下(B)、左(L)、右(R)
        T,B,L,R=540,600,40,880
        # 建立矩形循環路徑：右→下→左→上
        defaultSnakeBodyCycle = [[x,T] for x in range(L, R, 20)] +\
                                [[R,y] for y in range(T, B, 20)] + \
                                [[x,B] for x in range(R, L, -20)] +\
                                [[L,y] for y in range(B, T, -20)]
        N=len(defaultSnakeBodyCycle)
        # 取得蛇身體的5個節點位置
        for i in range(step, step+5):
            newSnakeBodyList.append(defaultSnakeBodyCycle[i%N])
        step+=1
        if step>=N:
            step=step-N
        _step[0]=step
    else: #mode == "hunting"
        # 追蹤模式：將新頭部加入，移除尾部
        currentSnakeBodyList.insert(0, nextSnakeheadPos)
        currentSnakeBodyList.pop()
        newSnakeBodyList = currentSnakeBodyList
    return newSnakeBodyList

def snakeLotteryControler(windowSize, mode="initial", maxNum=999):
    """
    主要的彩票遊戲控制器，處理遊戲初始化、事件處理和主循環

    Args:
        windowSize (tuple): 視窗大小 (width, height)
        mode (str): 遊戲模式
            - "initial": 初始模式，顯示歡迎畫面
            - "idle": 閒置模式
        maxNum (int): 彩票號碼的最大值，預設為999

    Returns:
        bool: True表示遊戲結束，False表示繼續遊戲
    """
    # 計算最大號碼的位數範圍
    digitRange = []
    for i in str(maxNum):
        digitRange.append(int(i))

    # 初始化Pygame和遊戲視窗
    pygame.init()
    screen = pygame.display.set_mode(windowSize, FULLSCREEN)
    runningSpeed = pygame.time.Clock()
    #caption = pygame.display.set_caption("PyLottery")

    # 設置字體和文字
    titleFont = pygame.font.SysFont("comicsansms", 50)
    title     = titleFont.render("PyLottery", True, (238, 60, 42))
    title0     = titleFont.render("Py", True, (0, 111, 130))
    title.blit(title0, (0,0))  # 將"Py"部分用不同顏色覆蓋
    textFont  = pygame.font.SysFont("comicsansms", 30)
    text      = textFont.render("Press 'SPACE' to crack a ball.", True, (0, 111, 130))
    text3     = textFont.render("Press 'X' to restart.", True, (0, 111, 130))
    text2     = textFont.render(u"The gifts are provided by our generous sponsors...", True, (100, 111, 230))

    # 載入並縮放贊助商圖片
    sponsorImg=pygame.image.load("./img/sponsorImg.png")
    sponsorImg=pygame.transform.scale(sponsorImg, (300, 300))

    # 初始化蛇身體位置
    snakeBodyList = [[20,100],[40,100], [60,100], [60,120], [60, 140]]

    if mode == "initial":
        screen.fill((234, 240, 243))
        pygame.display.flip()
    else: #mode == "idle"
        pass

    #x = 0
    # 主遊戲循環
    while True:
        # 處理事件
        for event in pygame.event.get():
                if event.type == QUIT:
                    return True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    print("exit")
                    return True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    return True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    # 播放準備音效並開始彩票遊戲
                    readySnd = pygame.mixer.music
                    readySnd.load('./snd/im-so-ready.wav')
                    readySnd.play(0,0)
                    rect0=(0 , 40)
                    rect1=(windowSize[0], rect0[1]+text.get_height())
                    pygame.draw.rect(screen, (234, 240, 243),
                            Rect(rect0, rect1), 0)
                    return snakeLottery(screen, snakeBodyList, windowSize, title, text3, digitRange, runningSpeed, maxNum)
                else:
                    pass

        # 繪製遊戲元素
        drawSnake(screen, snakeBodyList)
        screen.blit(title, (10, 10))
        screen.blit(text, (title.get_width()+50 , 40))
        screen.blit(text2, (50, 100))
        screen.blit(sponsorImg, (350,200))

        pygame.display.flip()
        runningSpeed.tick(6)
        # 清除螢幕
        pygame.draw.rect(screen, (234, 240, 243), Rect([0, 0], windowSize), 0)

        # 更新蛇的位置（循環移動模式）
        snakeBodyList = snakeDrawer(snakeBodyList, nextSnakeheadPos=None, mode="circling")


def snakeLottery(screen, snakeBody, windowSize, title, text, digitRange, runningSpeed, maxNum):
    """
    執行彩票抽獎遊戲的核心邏輯

    Args:
        screen: Pygame螢幕物件
        snakeBody (list): 蛇身體位置列表
        windowSize (tuple): 視窗大小
        title: 標題文字物件
        text: 說明文字物件
        digitRange (list): 數字位數範圍
        runningSpeed: Pygame時鐘物件
        maxNum (int): 彩票最大號碼

    Returns:
        bool: True表示遊戲結束，None表示重新開始
    """
    # 載入球體圖片
    sphere=pygame.image.load("./img/sphere.png")
    smallSphere=pygame.transform.scale(sphere, (32, 32))
    sphere=pygame.transform.scale(sphere, (100, 100))

    # 產生隨機彩票號碼
    lotteryNumber = randint(1, maxNum)
    lotteryNumberList = []
    for i in str(lotteryNumber):
        lotteryNumberList.append(int(i))

    # 補齊前導零以符合位數要求
    while len(lotteryNumberList) < len(digitRange):
        lotteryNumberList.insert(0, 0)

    ballIndex = 0
    dirIdx=0  # 方向索引，0=x方向，1=y方向

    # 為每個數字位數進行抽獎
    for d in range(0, len(lotteryNumberList)):
        # 建立問號文字
        questionFont = pygame.font.SysFont("comicsansms", 20)
        questionText = questionFont.render("?", True, (0, 0, 0))
        snakeHead=snakeBody[-1]
        ballPos=snakeHead

        # 隨機產生球的位置，確保不與蛇頭太接近
        while abs(ballPos[0]-snakeHead[0])<80 or abs(ballPos[1]-snakeHead[1])<40:
            ballPosX = randint(12, int(windowSize[0]/20)-12)
            ballPosY = randint(12, int((windowSize[1]-140)/20))
            ballPos = [20*ballPosX, 20*ballPosY]

        screen.blit(title, (10, 10))
        screen.blit(text, (title.get_width()+50 , 40))

        def drawScreen(drawBall=True):
            """
            繪製遊戲畫面的內部函數

            Args:
                drawBall (bool): 是否繪製球體
            """
            # 清除遊戲區域
            pygame.draw.rect(screen, (235, 233, 237), Rect([0, 85], [windowSize[0], windowSize[1]-190]), 0)
            if drawBall:
                screen.blit(smallSphere,  (ballPos[0]-16, ballPos[1]-16))
                screen.blit(questionText, (ballPos[0]-3, ballPos[1]-18))
            drawSnake(screen, snakeBody)

        # 蛇追蹤球的移動邏輯
        while snakeHead != ballPos:
            # 交替選擇x或y方向移動
            dir='x' if dirIdx==0 else 'y'
            if snakeHead[dirIdx]==ballPos[dirIdx]:
                step=0
            elif snakeHead[1-dirIdx]==ballPos[1-dirIdx]:
                step=1
            else:
                # 計算移動步數
                step = randint(1, int(math.ceil(abs(snakeHead[dirIdx]-ballPos[dirIdx])/50.0))+ 3)

            # 決定移動方向
            mode=dir+("MoveMinus" if snakeHead[dirIdx] > ballPos[dirIdx] else "MovePlus")

            # 執行移動
            for i in range(step):
                snakeHead=nextMove(snakeHead, mode=mode)
                # 檢查是否撞到自己身體
                if snakeHead in snakeBody and len(snakeBody)>8:
                    pygame.mixer.music.set_volume(0.3)
                    oopsSnd = pygame.mixer.music
                    oopsSnd.load('./snd/doh-ok.wav')
                    oopsSnd.play(0,0)
                    pygame.mixer.music.set_volume(1.0)
                # 處理撞到身體的情況
                while snakeHead in snakeBody:
                    snakeBody=snakeBody[1:]
                    drawScreen()
                    runningSpeed.tick(12)
                    pygame.display.flip()

                # 更新蛇身
                snakeBody.append(snakeHead)
                snakeBody=snakeBody[-(10+d*10):]  # 限制蛇身長度
                drawScreen()
                runningSpeed.tick(6)
                pygame.display.flip()
            dirIdx=1-dirIdx # 切換移動方向

        # 播放爆炸音效
        bangSnd = pygame.mixer.music
        bangSnd.load('./snd/bang_6.wav')
        bangSnd.play(0,0)

        # 播放爆炸動畫
        explosionAnimation=pygame.image.load("./img/explosion-sprite.png")
        explosionAnimation=pygame.transform.scale(explosionAnimation, (280,40))
        for i in range(7):
            drawScreen(drawBall=(i<4))
            screen.blit(explosionAnimation,  (ballPos[0]-20, ballPos[1]-20), area=((40*i,0),(40,40)))
            runningSpeed.tick(6)
            pygame.display.flip()
        drawScreen(drawBall=False)

        # 顯示抽中的數字
        n = lotteryNumberList[-1]
        lotteryNumberList.pop()
        numberFont = pygame.font.SysFont("comicsansms",70)
        numberText = numberFont.render("%d" % n, True, (50, 50, 50), (255, 255, 255))

        # 在右下角顯示球體和數字
        tmp = []
        tmp.append(n)
        for i in tmp:
            screen.blit(sphere, [windowSize[0]-50-100*(ballIndex-tmp.index(i)+1), windowSize[1]-100])
            screen.blit(numberText, (windowSize[0]-110*(ballIndex-tmp.index(i)+1), windowSize[1]-100)
            , special_flags=BLEND_RGB_MULT)
            pygame.display.flip()
        ballIndex = ballIndex + 1

        screen.blit(title,(10,10))
        screen.blit(text,(title.get_width()+50 , 40))
        pygame.display.flip()

    # 等待使用者輸入
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                print("escape")
                return True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                return True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                # 重新開始遊戲
                return
            else:
                pass

# 全域變數，用於快取圖片載入狀態
imgLoaded=False

def loadImg():
    """
    載入蛇的圖片資源（頭部、身體、尾部）
    使用全域變數避免重複載入圖片
    """
    global pyhead_w, pyhead, pybody_w, pybody, pytail_w, pytail, imgLoaded
    if imgLoaded:
        return
    # 載入蛇頭圖片
    pyhead_w=30
    pyhead=pygame.image.load("./img/pyhead.png")
    pyhead=pygame.transform.scale(pyhead, (pyhead_w, pyhead_w))

    # 載入蛇身圖片
    pybody_w=24
    pybody=pygame.image.load("./img/pybody.png")
    pybody=pygame.transform.scale(pybody, (pybody_w, pybody_w))

    # 載入蛇尾圖片
    pytail_w=30
    pytail=pygame.image.load("./img/pytail.png")
    pytail=pygame.transform.scale(pytail, (pytail_w, pytail_w))
    imgLoaded=True

def relDirection(pos1, pos2):
    """
    計算兩個位置之間的相對方向

    Args:
        pos1 (list): 第一個位置 [x, y]
        pos2 (list): 第二個位置 [x, y]

    Returns:
        int: 方向編號
            - 0: 向右
            - 1: 向上
            - 2: 向左
            - 3: 向下
    """
    if pos1[0]==pos2[0]:  # x座標相同，垂直移動
        return 1 if pos2[1]<pos1[1] else 3  # 向上或向下
    else:  # 水平移動
        return 0 if pos2[0] > pos1[0] else 2  # 向右或向左

def drawBodyPart(screen, img, width, lastPart, thisPart, nextPart):
    """
    繪製蛇身體的一個部分，並根據前後位置調整旋轉角度

    Args:
        screen: Pygame螢幕物件
        img: 要繪製的圖片
        width (int): 圖片寬度
        lastPart (list): 前一個身體部分的位置
        thisPart (list): 當前身體部分的位置
        nextPart (list): 下一個身體部分的位置
    """
    # 計算相對於前一部分的方向
    bodyDir1=relDirection(lastPart, thisPart) if lastPart else None
    # 計算相對於下一部分的方向
    bodyDir2=relDirection(thisPart, nextPart) if nextPart else bodyDir1
    if bodyDir1==None:
        bodyDir1=bodyDir2

    # 計算平均方向作為旋轉角度
    bodyDir=0.5*(bodyDir2+bodyDir1)
    # 處理方向差異為3的特殊情況（0和3之間的轉換）
    if abs(bodyDir2-bodyDir1)==3:
        bodyDir=bodyDir+2

    # 旋轉圖片
    imgRotated=pygame.transform.rotate(img, 90*(bodyDir-1))
    # 計算偏移量
    shift=width*0.5 if bodyDir1==bodyDir2 else width*1.414*0.5
    # 繪製到螢幕上
    screen.blit(imgRotated, (thisPart[0]-shift, thisPart[1]-shift))

def drawSnake(screen, snakeBody):
    """
    繪製完整的蛇，包括頭部、身體和尾部

    Args:
        screen: Pygame螢幕物件
        snakeBody (list): 蛇身體位置列表，從尾部到頭部
    """
    if len(snakeBody)<2:
        return

    # 載入圖片資源
    loadImg()

    # 繪製蛇尾（第一個元素）
    drawBodyPart(screen, pytail, pytail_w, None, snakeBody[0], snakeBody[1])

    # 繪製蛇身（中間元素）
    for i in range(1, len(snakeBody)-1):
        drawBodyPart(screen, pybody, pybody_w, snakeBody[i-1], snakeBody[i], snakeBody[i+1])

    # 繪製蛇頭（最後一個元素）
    drawBodyPart(screen, pyhead, pyhead_w, snakeBody[-2], snakeBody[-1], None)

# 程式進入點
if __name__ == "__main__":
    """
    主程式入口，初始化遊戲並進入主循環
    """
    end=False
    while not end:
        # 啟動彩票控制器，設置視窗大小為1024x768，最大號碼為288
        end=snakeLotteryControler(windowSize = (1024, 768), maxNum = 288)
    print("end")
    pygame.display.quit()