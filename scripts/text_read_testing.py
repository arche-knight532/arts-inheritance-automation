import pytesseract
import pyscreenshot as ImageGrab
from PIL import Image

import time
from configparser import ConfigParser


#TODO:
# - Add actual code to control the Switch

def loadConfig():
    #loads config file "config.ini"
    global x1, x2, x3, x4, y1, y2, y3, y4, arts, description, pullLimit, logging, tesseractLocation
    print("loading config")
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


def takeScreenshot():
    #takes screenshot, save to screenshot.png in current directory
    print("taking screenshot")
    image_name = "screenshot.png"
    screenshot = ImageGrab.grab()
    filepath = f".\\{image_name}"
    screenshot.save(filepath)


def cropImage():
    #crops out the art name and description of the art, saves to corresponding files
    print("cropping image")
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
    print(f"Art pulled: '{artPulled}'")
    return artPulled


def checkArtDescription():
    #check if an art is descriptionless
    pytesseract.pytesseract.tesseract_cmd = tesseractLocation
    artDescription = pytesseract.image_to_string(Image.open('artDescription.png')).strip()
    print(f"Art description: '{artDescription}'")
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
    outputFilename = "artsLog.csv";
    file = open(outputFilename, "w")
    length = len(artsPulledLog)

    #bubble sort because I'm a lazy bitch, also it's really shitty, also I didn't want to deal with dictionaries
    for i in range(0, length):
        for j in range(i, length):
            if artsPulledCounts[i] < artsPulledCounts[j]:
                temp = artsPulledCounts[i]
                artsPulledCounts[i] = artsPulledCounts[j]
                artsPulledCounts[j] = temp

    for i in range(0, length):
        #print(f"art: '{artsPulledLog[i]}', count: '{artsPulledCounts[i]}'")
        file.write(f"{artsPulledLog[i]},{artsPulledCounts[i]}\n")
        i = i + 1
    file.close()
    print(f"Written to output file {outputFilename}")


def main():
    #artsPulledLog and artsPulledCounts to be used for tracking pulls if logging == "enabled"
    global artsPulledLog, artsPulledCounts, artName, desc

    #initialize values
    loadConfig()
    artsPulledLog = []
    artsPulledCounts = []

    #loop for pullLimit iterations
    for i in range(1, pullLimit):
        #TODO: code for controlling the switch goes here vvv

        #check art
        print(f"iteration = {i}")
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
                break
            if description[index] == "y" and desc != "":
                break

        time.sleep(1)

    #write log file if enabled
    if logging == "enable":
        writeLogFile()


if __name__ == '__main__':
    main()
