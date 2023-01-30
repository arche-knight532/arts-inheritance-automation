import pytesseract
import pyscreenshot as ImageGrab
from PIL import Image
import serial

import time
from configparser import ConfigParser
import argparse


#Bonus features to maybe work on:
# - mayke a script to generate config file based on user inputs (potentially clicks for x/y coordinates)
# - maybe make it so it logs if it gets a sigkill?
# - maybe include way for users to run script online/remotely rather than needing to clone repo? not exactly sure an easy way to set that up

def loadConfig():
    #loads config file "config.ini"
    global x1, x2, x3, x4, y1, y2, y3, y4, arts, description, pullLimit, logging, tesseractLocation, port
    #print("loading config")
    config = ConfigParser()
    config.read("config.ini")

    #grab positions of art name/description. 1&2 correspond to art name, 3&4 correspond to description
    x1 = int(config["DEFAULT"]["x1"])
    x2 = int(config["DEFAULT"]["x2"])
    x3 = int(config["DEFAULT"]["x3"])
    x4 = int(config["DEFAULT"]["x4"])
    y1 = int(config["DEFAULT"]["y1"])
    y2 = int(config["DEFAULT"]["y2"])
    y3 = int(config["DEFAULT"]["y3"])
    y4 = int(config["DEFAULT"]["y4"])

    #get art names and whether or not user wants art to be descriptionless
    arts = [art.strip() for art in config["DEFAULT"]["arts"].split(",")]
    description = [desc.strip() for desc in config["DEFAULT"]["description"].split(",")]

    #remaining config options
    pullLimit = int(config["DEFAULT"]["pullLimit"])
    logging = config["DEFAULT"]["logging"]
    tesseractLocation = config["DEFAULT"]["tesseractLocation"]
    port = config["DEFAULT"]["port"]


def takeScreenshot():
    #takes screenshot, save to screenshot.png in current directory
    #print("taking screenshot")
    image_name = "screenshot.png"
    screenshot = ImageGrab.grab()
    filepath = f".\\{image_name}"
    screenshot.save(filepath)


def cropImage():
    #crops out the art name and description of the art, saves to corresponding files
    #print("cropping image")
    image_name = "screenshot.png"
    img = Image.open(image_name)
    imgCroppedArt = img.crop(box = (x1, y1, x2, y2))
    imgCroppedDescription = img.crop(box = (x3, y3, x4, y4))
    #imgCropped.show()
    imgCroppedArt.save("artName.png")
    imgCroppedDescription.save("artDescription.png")


def checkArtName():
    #check the name of the art
    pytesseract.pytesseract.tesseract_cmd = tesseractLocation
    artPulled = pytesseract.image_to_string(Image.open('artName.png')).strip()
    #print(f"Art pulled: '{artPulled}'")
    return artPulled


def checkArtDescription():
    #check if an art is descriptionless
    pytesseract.pytesseract.tesseract_cmd = tesseractLocation
    artDescription = pytesseract.image_to_string(Image.open('artDescription.png')).strip()
    #print(f"Art description: '{artDescription}'")
    return artDescription


def countArtPulls():
    #count arts pulled for logging if enabled
    global artsPulledLog, artsPulledCounts, artName, desc

    #handle prepending 'd.' for descriptionless arts
    if artName != "" and desc == "":
        artName = f"d.{artName}"

    #log art into arrays
    if artName not in artsPulledLog:
        artsPulledLog.append(artName)
        artsPulledCounts.append(1)
    else:
        index = artsPulledLog.index(artName)
        artsPulledCounts[index] = artsPulledCounts[index] + 1


def writeLogFile():
    #write counts to log if logging is enabled
    global artsPulledLog, artsPulledCounts
    outputFilename = "artsLog.txt";
    file = open(outputFilename, "w")
    length = len(artsPulledLog)

    #bubble sort because I'm a lazy bitch, also it's really shitty, also I didn't want to deal with dictionaries
    for i in range(0, length):
        for j in range(i+1, length):
            if artsPulledCounts[i] < artsPulledCounts[j]:
                temp = artsPulledCounts[i]
                artsPulledCounts[i] = artsPulledCounts[j]
                artsPulledCounts[j] = temp

                temp = artsPulledLog[i]
                artsPulledLog[i] = artsPulledLog[j]
                artsPulledLog[j] = temp

    #write arrays to file
    for i in range(0, length):
        file.write(f"{artsPulledLog[i]}\t{artsPulledCounts[i]}\n")

    file.close()
    print(f"Written to output file {outputFilename}")


def press(ser, s):
    #press and release desired button
    ser.write(s.encode())
    time.sleep(0.05)
    ser.write(b'0')
    time.sleep(0.075)


def sleepConsole(ser):
    #press and release desired button
    ser.write('H'.encode())
    time.sleep(2)
    ser.write(b'0')
    time.sleep(0.075)
    ser.write('A'.encode())
    time.sleep(0.05)
    ser.write(b'0')
    time.sleep(0.075)


def main():
    #artsPulledLog and artsPulledCounts to be used for tracking pulls if logging == "enabled"
    global artsPulledLog, artsPulledCounts, artName, desc

    #initialize values
    loadConfig()
    artsPulledLog = []
    artsPulledCounts = []

    #initialize controller
    parser = argparse.ArgumentParser()
    parser.add_argument('--count', type=int, default=1)
    parser.add_argument('--serial', default=port)
    args = parser.parse_args()
    with serial.Serial(args.serial, 9600) as ser:

        #loop for pullLimit iterations
        for i in range(1, pullLimit+1):
            print(f"iteration = {i}")

            #pull art
            press(ser, 'A')
            time.sleep(0.75)
            press(ser, 'r')
            time.sleep(0.2)

            #check art
            takeScreenshot()
            cropImage()
            artName = checkArtName()
            desc = checkArtDescription()

            #count art if logging enabled
            if logging == "enable":
                countArtPulls()

            #art confirmation
            if artName in arts:
                index = arts.index(artName)
                if description[index] == "n" and desc == "":
                    press(ser, 'l')
                    break
                if description[index] == "y" and desc != "":
                    press(ser, 'l')
                    break

            #exit from art menu
            press(ser, 'B')
            time.sleep(0.7)
        #sleep console after completion
        sleepConsole(ser)

    #write log file if enabled
    if logging == "enable":
        writeLogFile()


if __name__ == '__main__':
    main()
