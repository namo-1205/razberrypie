# 연결 테스트 코드
#!/usr/bin/env python3
#!pip install pyfirmata
from pyfirmata import Arduino, util
import time

PIN = 13
DELAY = 1
board = None


def Loop():
    global board
    #
    if board is None:
        board = Arduino('COM6')
        pin_light = board.get_pin('a:1:i') #analogpin 0번을 input으로
        it = util.Iterator(board)
        it.start()
        pin_light.enable_reporting()
        print("Communication Successfully started")
    while True:
        CDS = pin_light.read()
        print(CDS)
        time.sleep(0.5)

Loop()