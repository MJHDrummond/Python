##########################################################################
#
# Script to automatically delevel PvP rank in South Parks Phone Destroyer game.
# We will use image recognition to find the start game button and then use mouse
# clicks to start the battle. The script will then wait before looking for the
# button again to repeat the process. Sometimes the opponent will leave or time
# out so a second image search was added to deal with this.
#
# The images used for the recognition process must be manually retrieved before
# running the script as depending on the size of the game window the button
# locations will differ.
#
# Written in PyCharm for Windows.
#
# Author: McGregor Drummond
# Date: 20 January 2018
# Working: 21 January 2018
# Updated: 24 January 2018
#
##########################################################################

# import required modules
import pyautogui
from random import randrange
import time


# create mouse click function
def clickButton(buttonLocation):

    # to avoid always clicking the same location (to be safe incase there are autoclick detectors in game)
    # the x and y coordinates are selected within a random range around the center of the button.
    clickLocationX = randrange(buttonLocation[0],     buttonLocation[0]+buttonLocation[2])
    clickLocationY = randrange(buttonLocation[1], buttonLocation[1]+buttonLocation[3])

    print('Click location: ', clickLocationX, clickLocationY)

    pyautogui.click(clickLocationX, clickLocationY)


# create function for finding the begin battle button
def beginBattle():

    # input begin battle button image
    im1 = 'beginBattleButtonOriginal.png'  # using 'T' in 'BATTLE' to increase chances of finding the button
    counter = 0  # counter used to track number of button search attempts
    while True:
        try:
            beginBattleLocate = pyautogui.locateOnScreen(im1)  # search and return location of button
            print(beginBattleLocate)

            if beginBattleLocate is not None:
                clickButton(beginBattleLocate)
                print('Start battle successful, waiting 120s before next search...')  # losing matches typically 2 mins
                time.sleep(120)
                return True  # returns True = function successful
            elif counter == 5:  # if button not found after 5 attempts then break loop and search for another button
                print('Begin battle button not found, trying next button search.')
                global globalCounter # call the global keyword to update number of overall fails without having to return variables
                globalCounter += 1
                return False
            else:  # if button not found, retry
                print('Button not found, retrying...')
                counter += 1

        except TypeError as e:
            print('Failed with error: ', e)
            globalCounter += 1
            return False


# create function for finding the opponent left button
# the button is an "ok" button to acknowledge that the opponent has left
def opponentLeftScreen():

    # input opponent left button
    # im1 = takeOppoLeftScreenshot()
    im1 = 'opponentLeftButtonOriginal.png'
    counter = 0  # counter used to track the number of button search attempts
    while True:
        try:
            oppoLeftButtonLocation = pyautogui.locateOnScreen(im1)  # search and return the location of button
            print(oppoLeftButtonLocation)

            if oppoLeftButtonLocation is not None:
                clickButton(oppoLeftButtonLocation)
                print('Escaped opponent left screen, beginning search for start battle button...')
                time.sleep(10)  # wait 10 seconds after finding the button to account for loading screens
                return True  # returns True = function successful
            elif counter == 2:  # if button not found after 2 attempts then break loop and search for another button
                print('Opponent left button not found, trying next button search.')
                global globalCounter  # call the global keyword to update number of overall fails without having to return variables
                globalCounter += 1
                return False
            else:  # if button not found, retry
                print('Button not found, retrying...')
                counter += 1

        except TypeError as e:
            print('Failed with error: ', e)
            globalCounter += 1
            return False

# create function call to check if the required pvp rank has been reached then stop the script
def rankLimiter():

    im1 = 'pvpRank20Image.png'
    if pyautogui.locateOnScreen(im1) is not None:
        print('Minimum pvp rank reached, stopping script.')
        quit()
        
        
# create function to call the button search functions
# will add counter feature here so that it is not an infinite loop and to break after so many failed attempts
def main():

    global globalCounter
    globalCounter = 0  # used to track the number of overall failed search attempts within the functions
    while True:
        rankLimiter()  # first check if minimum rank reached
        if beginBattle() is True:
            globalCounter = 0  # reset failed attempts counter after a successful button click
            continue  # if begin battle successful, return to start of loop
        elif opponentLeftScreen() is True:
            globalCounter = 0  # reset failed attempts counter after a successful button click
            continue  # if opponent left screen escape successful, return to start of loop
        elif globalCounter == 6:  # each function gets 3 attempts at finding the button otherwise stop the script
            print('Button search has reached maximum attempts, stopping script.')
            quit()

# call main function to start the script
main()

