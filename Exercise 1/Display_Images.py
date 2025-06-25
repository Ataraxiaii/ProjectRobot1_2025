from microbit import *

# define numbers
NUMBERS = {
    1: Image("00900:"
             "00900:"
             "00900:"
             "00900:"
             "00900"),

    2: Image("09990:"
             "00090:"
             "09990:"
             "09000:"
             "09990"),

    3: Image("09990:"
             "00090:"
             "09990:"
             "00090:"
             "09990"),

    4: Image("09090:"
             "09090:"
             "09990:"
             "00090:"
             "00090"),

    5: Image("09990:"
             "09000:"
             "09990:"
             "00090:"
             "09990"),

    6: Image("09990:"
             "09000:"
             "09990:"
             "09090:"
             "09990"),

    7: Image("09990:"
             "00090:"
             "00090:"
             "00090:"
             "00090"),

    8: Image("09990:"
             "09090:"
             "09990:"
             "09090:"
             "09990"),

    9: Image("09990:"
             "09090:"
             "09990:"
             "00090:"
             "09990")
}

# show number images on led matrix
while True:
    for number in range(1, 10):  # 1-9
        display.show(NUMBERS[number])
        sleep(1000)  # show 1 second for every number
