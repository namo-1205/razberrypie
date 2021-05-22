# 연결 테스트 코드
# 아두이노: 파일 → 예제 → Firmata → StandFirmata 실행
# 라즈베리파이: 아래 코드 실행
# 아두이노의 기판 LED 깜빡임을 확인할 수 있는 테스트 코드입니다.

#!/usr/bin/env python3
#!pip install pyfirmata
from pyfirmata import Arduino

PIN = 13
DELAY = 1
board = None


def Blink():
    global board
    #
    if board is None:
        board = Arduino('COM4')
        print("Communication Successfully started")
    while True:
        board.digital[PIN].write(1) 
        board.pass_time(DELAY) 
        board.digital[PIN].write(0) 
        board.pass_time(DELAY)

Blink()
