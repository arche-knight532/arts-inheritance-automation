import pytesseract
import pyscreenshot as ImageGrab
from PIL import Image
#import schedule

import time
from configparser import ConfigParser


#TODO:
# - Add descriptionless art checker
# - Add actual code to control the Switch
# - Have code stop pulling after pullLimit art pulls
#Bonus features:
# - If logging is set to "enabled", log data on pulls into a dict object, load into a file at end of run

def loadConfig():
    #loads config file "config.ini"
    global x1, x2, x3, x4, y1, y2, y3, y4, arts, description, pullLimit, logging
    print("loading config")
    config = ConfigParser()
    config.read("config.ini")
    #print(config.sections())
    
    #grab positions of art name/description. 1/2 correspond to art name, 3/4 correspond to description
    x1 = int(config["DEFAULT"]["x1"])
    x2 = int(config["DEFAULT"]["x2"])
    x3 = int(config["DEFAULT"]["x3"])
    x4 = int(config["DEFAULT"]["x4"])
    y1 = int(config["DEFAULT"]["y1"])
    y2 = int(config["DEFAULT"]["y2"])
    y3 = int(config["DEFAULT"]["y3"])
    y4 = int(config["DEFAULT"]["y4"])
    
    #get art names and whether or not user wants art to be descriptionless
    #potentially strip each item in arts to user-proof this?
    arts = config["DEFAULT"]["arts"].split(",")
    description = config["DEFAULT"]["description"].split(",")
    
    #pull limit and logging config
    pullLimit = int(config["DEFAULT"]["pullLimit"])
    logging = config["DEFAULT"]["logging"]


def takeScreenshot():
    #takes screenshot, save to screenshot.png in current directory
    print("taking screenshot")
    image_name = "screenshot.png"
    screenshot = ImageGrab.grab()
    filepath = f".\\{image_name}"
    screenshot.save(filepath)
    #print("screenshot saved")


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
    #print("cropped image saved")


def checkArtName():
    #check the name of the art
    #TODO: change tesseract location to a config item?
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
    artPulled = pytesseract.image_to_string(Image.open('artName.png')).strip()
    print(f"Art pulled: '{artPulled}'")
    return artPulled


def checkArtDescription():
    #check if an art is descriptionless
    #TODO: change tesseract location to a config item?
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
    artDescription = pytesseract.image_to_string(Image.open('artDescription.png')).strip()
    print(f"Art description: '{artDescription}'")
    return artDescription


def countArtPulls():
    #count arts pulled for logging if enabled
    global artsPulledLog, artsPulledCounts, artName, description

    #handle prepending 'd.' for descriptionless arts
    if artName != "" and description == "":
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
    global artsPulledLog, artsPulledCounts, artName, description

    outputFilename = "artsLog.csv";
    #TODO: potentially sort arrays so that arts are in order of pull count?
    file = open(outputFilename, "w")
    index = 0
    length = len(artsPulledLog)
    while index < length:
        #print(f"art: '{artsPulledLog[index]}', count: '{artsPulledCounts[index]}'")
        file.write(f"{artsPulledLog[index]},{artsPulledCounts[index]}\n")
        index = index + 1
    file.close()
    print(f"Written to output file {outputFilename}")


def main():
    #artsPulledLog and artsPulledCounts to be used for tracking pulls if logging == "enabled"
    global artsPulledLog, artsPulledCounts, artName, description
    
    #initialize values
    loadConfig()
    artsPulledLog = []
    artsPulledCounts = []
    iteration = 1

    #loop for pullLimit iterations
    while iteration <= pullLimit:
        print(f"iteration = {iteration}")
        takeScreenshot()
        cropImage()
        artName = checkArtName()
        description = checkArtDescription()

        #TODO: logic for checking if art is requested needs to be updated for description checking
        #if artName in arts:
        #    print("Art pulled in requested arts")
        #else:
        #    print("Art pulled not in requested arts")

        #count art if logging enabled and update iteration counter
        if logging == "enable":
            countArtPulls()
        iteration += 1
        time.sleep(3)

    #write log file if enabled
    if logging == "enable":
        writeLogFile()


if __name__ == '__main__':
    main()





#print(pytesseract.image_to_string('test_image.png'))
#print(pytesseract.get_languages(config=''))
#print(pytesseract.image_to_boxes(Image.open('test.png')))

#schedule.every(5).seconds.do(takeScreenshot)
#while True:
#    schedule.run_pending()
#    time.sleep(1)
